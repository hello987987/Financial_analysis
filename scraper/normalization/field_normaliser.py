import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class FieldNormaliser:
    RE = re.compile(
        r'(\d+)\s*(min|mins|minute|minutes|hour|hours|day|days)\s*ago',
        re.I
    )

    def normalise(self, data: str):
        match = self.RE.search(data)
        if not match:
            return None

        value = int(match.group(1))
        unit = match.group(2).lower()

        tz = ZoneInfo("Australia/Sydney")
        now = datetime.now(tz)

        if unit.startswith("min"):
            return now - timedelta(minutes=value)
        elif unit.startswith("hour"):
            return now - timedelta(hours=value)
        elif unit.startswith("day"):
            return now - timedelta(days=value)

        return None


if __name__ == "__main__":
    ns = FieldNormaliser()
    p = ns.normalise("Engadget • 20 min ago")
    print(p)