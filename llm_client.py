from __future__ import annotations

import os
import random
import threading
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

PRIMARY_MODEL = "gemini-3.1-flash-lite"
FALLBACK_MODEL = "gemini-3.1-flash-lite"   # model ổn định, đổi tùy bạn

KEY_ENV_NAMES = ("GOOGLE_API_KEY", "GOOGLE_API_KEY_2")
RETRYABLE = {429, 500, 503, 504}   # quá tải / hết quota -> đổi key
BAD_KEY = {401, 403}               # key sai / bị khóa -> bỏ qua key đó


def load_api_keys() -> list[str]:
    keys: list[str] = []
    for name in KEY_ENV_NAMES:
        v = (os.getenv(name) or "").strip()
        if v and v not in keys:
            keys.append(v)
    return keys


class GeminiPool:
    def __init__(self, keys: list[str]):
        if not keys:
            raise RuntimeError("Chưa có GOOGLE_API_KEY nào trong .env / st.secrets")
        self.clients = [genai.Client(api_key=k) for k in keys]
        self._idx = 0
        self._lock = threading.Lock()

    def _next_start(self) -> int:
        # round-robin: mỗi lần gọi bắt đầu từ key kế tiếp -> chia đều tải cho 2 key
        with self._lock:
            i = self._idx
            self._idx = (self._idx + 1) % len(self.clients)
            return i

    def generate(self, *, contents, config, models=(PRIMARY_MODEL, FALLBACK_MODEL), rounds: int = 2):
        last_err = None
        start = self._next_start()
        n = len(self.clients)
        for model in models:
            for r in range(rounds):
                for step in range(n):
                    client = self.clients[(start + step) % n]
                    try:
                        return client.models.generate_content(
                            model=model, contents=contents, config=config
                        )
                    except errors.APIError as e:
                        code = getattr(e, "code", None)
                        if code in RETRYABLE or code in BAD_KEY:
                            last_err = e
                            continue          # thử key kế tiếp
                        raise                 # lỗi 400... là lỗi request, không retry
                time.sleep(min(2 ** r + random.random(), 8))  # cả 2 key đều lỗi -> chờ rồi thử lại
        raise last_err


_pool: GeminiPool | None = None
_pool_lock = threading.Lock()


def get_pool() -> GeminiPool:
    global _pool
    with _pool_lock:
        if _pool is None:
            _pool = GeminiPool(load_api_keys())
        return _pool
