import json
import threading
from typing import List, Dict, Optional
import random
import os

class QuoteManager:
    def __init__(self, filepath: str = "quotes.json"):
        self.filepath = filepath
        self._lock = threading.Lock()
        self._quotes = [] 
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.filepath):
            self._quotes = []
            return
        with open(self.filepath, "r", encoding="utf-8") as f:
            self._quotes = json.load(f)

    def _save(self) -> None:
        with self._lock:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._quotes, f, indent=2, ensure_ascii=False)

    def list_quotes(self) -> List[Dict]:
        return list(self._quotes)  

    def get_random(self) -> Optional[Dict]:
        if not self._quotes:
            return None
        return random.choice(self._quotes)

    def get_by_id(self, qid: int) -> Optional[Dict]:
        for q in self._quotes:
            if q.get("id") == qid:
                return q
        return None

    def _next_id(self) -> int:
        if not self._quotes:
            return 1
        return max(q["id"] for q in self._quotes) + 1

    def add_quote(self, text: str, author: str = "") -> Dict:
        with self._lock:
            new = {"id": self._next_id(), "text": text.strip(), "author": author.strip()}
            self._quotes.append(new)
            self._save()
            return new



