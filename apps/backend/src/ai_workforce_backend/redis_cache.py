"""Fail-safe in-memory cache manager powered by Redis with automatic DB fallback."""

from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

try:
    import redis
    _REDIS_AVAILABLE = True
except ImportError:
    redis = None  # type: ignore[assignment]
    _REDIS_AVAILABLE = False


class RedisCacheManager:
    """Provides key-value JSON caching with TTL and automatic fail-safe fallback."""

    def __init__(self, redis_url: str | None = None) -> None:
        self._url = redis_url or os.getenv("REDIS_URL", "")
        self._client: redis.Redis[bytes] | None = None
        self._connected = False
        
        if _REDIS_AVAILABLE and self._url:
            try:
                self._client = redis.Redis.from_url(
                    self._url,
                    socket_connect_timeout=1.5,
                    socket_timeout=1.5,
                    decode_responses=False,
                )
                # Test connectivity
                self._client.ping()
                self._connected = True
                logger.info("RedisCacheManager connected to %s", self._url)
            except Exception as err:
                logger.warning("Redis connection failed (%s). Operating in pass-through fallback mode.", err)
                self._client = None
                self._connected = False
        else:
            if not _REDIS_AVAILABLE:
                logger.info("redis package not installed. RedisCacheManager operating in pass-through fallback mode.")
            else:
                logger.info("REDIS_URL not configured. RedisCacheManager operating in pass-through fallback mode.")

    @property
    def is_available(self) -> bool:
        return self._connected and self._client is not None

    def get(self, key: str) -> Any | None:
        if not self.is_available or self._client is None:
            return None
        try:
            raw = self._client.get(key)
            if raw is None:
                return None
            return json.loads(raw.decode("utf-8"))
        except Exception as err:
            logger.debug("Redis get error for key %s: %s", key, err)
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> bool:
        if not self.is_available or self._client is None:
            return False
        try:
            payload = json.dumps(value).encode("utf-8")
            self._client.setex(key, ttl_seconds, payload)
            return True
        except Exception as err:
            logger.debug("Redis set error for key %s: %s", key, err)
            return False

    def delete(self, key: str) -> bool:
        if not self.is_available or self._client is None:
            return False
        try:
            self._client.delete(key)
            return True
        except Exception as err:
            logger.debug("Redis delete error for key %s: %s", key, err)
            return False

    def invalidate_tenant(self, tenant_ref: str) -> int:
        """Deletes all cached knowledge keys matching tenant_ref."""
        if not self.is_available or self._client is None:
            return 0
        try:
            pattern = f"kb:*:{tenant_ref}:*"
            keys = self._client.keys(pattern)
            if not keys:
                return 0
            count = self._client.delete(*keys)
            logger.info("Invalidated %d Redis cache keys for tenant %s", count, tenant_ref)
            return count
        except Exception as err:
            logger.debug("Redis invalidate error for tenant %s: %s", tenant_ref, err)
            return 0
