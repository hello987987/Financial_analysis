import json
import re
import unicodedata
from pathlib import Path

_CORP_SUFFIXES = {
    "inc", "inc.", "corp", "corp.", "corporation",
    "ltd", "ltd.", "limited", "plc", "sa", "ag", "nv"
}

def _normalize_entity(ent):
    ent = unicodedata.normalize("NFKC", ent)
    ent = ent.lower()

    ent = ent.replace("’s", "").replace("'s", "")

    ent = re.sub(r"[^\w\s]", "", ent)

    tokens = ent.split()

    while tokens and tokens[-1] in _CORP_SUFFIXES:
        tokens.pop()

    return " ".join(tokens)


class CompanyResolver:
    def __init__(self, json_path):
        self.alias_map = self._load_map(json_path)

    def _load_map(self, path):
        if not path.exists():
            raise FileNotFoundError(f"Company map not found: {path}")

        raw = json.loads(path.read_text(encoding="utf-8-sig"))

        return {
            _normalize_entity(k): v.lower()
            for k, v in raw.items()
        }

    def resolve(self, raw_entity):
        norm = _normalize_entity(raw_entity)
        return self.alias_map.get(norm)