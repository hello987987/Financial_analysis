import yfinance as yf
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from pathlib import Path
import json
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]

class OrderFlowLiquidity:
    def __init__(self, company_name, stock_time):
        lookup_path = Path(__file__).parent / "company_tickers.json"
        with open(lookup_path, "r", encoding="utf-8") as f:
            self.COMPANY_TICKERS = json.load(f)
        self.company = self.COMPANY_TICKERS.get(company_name.lower())
        self.ticker = yf.Ticker(self.company)
        self.stocktime = stock_time
        self.sydney_tz = ZoneInfo("Australia/Sydney")

    def track_price(self) -> dict[str, any]:
        if self.stocktime.tzinfo is None:
            self.stocktime = self.stocktime.replace(tzinfo=self.sydney_tz)
        else:
            self.stocktime = self.stocktime.astimezone(self.sydney_tz)

        start_time = self.stocktime 
        end_time = self.stocktime + timedelta(hours = 24)

        frame = self.ticker.history(
            start = start_time.date(),
            end = end_time.date() + timedelta(days = 1),
            interval = "15m" 
        )

        if frame.empty:
            return frame 
        frame = frame.tz_convert(self.sydney_tz)

        price_window = frame.loc[start_time:end_time]
        initial_open = float(price_window.iloc[0]["Open"])
        final_close = float(price_window.iloc[-1]["Close"])

        return {
            #will be used if news article feature falls through
            "start_time": start_time,
            "end_time" : end_time,
            "ohlcv": price_window[["Open", "High", "Low", "Close", "Volume"]].copy(),
            "initial_open": initial_open,
            "final_close": final_close,
            "abs_change": final_close - initial_open,
            "return_pct": (final_close / initial_open) - 1,
            "rows": len(price_window),
        }
    
    def compute_order_flow_liquidity(self):
        frame = self.track_price()

        df = frame["ohlcv"].copy()
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["Close", "Volume"])
        if df.empty or len(df) < 2:
            return {}
        
        close = df["Close"].astype(float)
        vol = df["Volume"].astype(float)

        # log returns
        logret = np.log(close).diff()
        logret = logret.fillna(0.0)

        # total and dollar volume
        total_volume = float(vol.sum())
        dollar_volume_series = close * vol
        dollar_volume = float(dollar_volume_series.sum())
        avg_volume = float(vol.mean())

        # Volume weighted avg price
        typical_price = (df["High"].astype(float) + df["Low"].astype(float) + close) / 3.0
        typical_dollar = typical_price * vol

        if total_volume > 0:
            vwap = float(typical_dollar.sum() / total_volume)
        else:
            vwap = float(close.iloc[-1])

        final_close = float(close.iloc[-1])
        close_vs_vwap = (final_close / vwap) - 1.0 if vwap != 0 else 0.0

        # Realized volatility 
        realized_vol = float(logret.std(ddof=0))

        # Range% per bar 
        range_abs = (df["High"].astype(float) - df["Low"].astype(float))
        range_pct = (range_abs / close.replace(0.0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
        avg_range_pct = float(range_pct.mean())
        max_range_pct = float(range_pct.max())

        # Amihud illiquidity proxy
        per_bar_dollar = dollar_volume_series.replace(0.0, np.nan)
        amihud_series = (logret.abs() / per_bar_dollar).replace([np.inf, -np.inf], np.nan).dropna()
        amihud_illiq = float(amihud_series.mean()) if not amihud_series.empty else 0.0

        # Signed return volume
        signed_return_volume = float((np.sign(logret) * vol).sum())

        # Return-volume pressure 
        return_volume_pressure = float((logret * vol).sum())

        # Up-volume fraction 
        up_volume = float(vol[logret > 0].sum())
        up_volume_frac = (up_volume / total_volume) if total_volume > 0 else 0.0

        return {
            "start_time": frame["start_time"],
            "end_time": frame["end_time"],
            "rows": int(len(df)),

            # participation
            "total_volume": total_volume,
            "avg_volume": avg_volume,
            "dollar_volume": dollar_volume, 

            # liquidity / fragility
            "realized_vol": realized_vol, 
            "avg_range_pct": avg_range_pct, 
            "max_range_pct": max_range_pct, 
            "amihud_illiq": amihud_illiq,

            # order flow pressure proxies
            "signed_return_volume": signed_return_volume,
            "return_volume_pressure": return_volume_pressure, 
            "up_volume_frac": up_volume_frac, 

            # VWAP context
            "vwap": vwap,
            "close_vs_vwap": close_vs_vwap, 
        }
    
if __name__ == "__main__":
    #ODF = OrderFlowLiquidity()
    #print(ODF.compute_order_flow_liquidity)