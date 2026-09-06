"""Unit tests for RedisCacheManager fail-safe caching behavior."""

import json
from unittest.mock import MagicMock

from ai_workforce_backend.redis_cache import RedisCacheManager


def test_redis_cache_fallback_when_unconfigured():
    """Verify RedisCacheManager operates in pass-through fallback mode when REDIS_URL is empty."""
    cache = RedisCacheManager(redis_url="")
    assert not cache.is_available
    assert cache.get("kb:test_key") is None
    assert cache.set("kb:test_key", {"data": 123}) is False
    assert cache.delete("kb:test_key") is False
    assert cache.invalidate_tenant("staging-tenant") == 0


def test_redis_cache_mocked_operations():
    """Verify RedisCacheManager get, set, delete, and invalidate operations with a mocked client."""
    cache = RedisCacheManager(redis_url="")
    mock_client = MagicMock()
    cache._client = mock_client
    cache._connected = True

    # Test set
    assert cache.set("kb:key1", {"topic": "Pricing"}, ttl_seconds=60) is True
    mock_client.setex.assert_called_once_with("kb:key1", 60, json.dumps({"topic": "Pricing"}).encode("utf-8"))

    # Test get hit
    mock_client.get.return_value = json.dumps({"topic": "Pricing"}).encode("utf-8")
    result = cache.get("kb:key1")
    assert result == {"topic": "Pricing"}
    mock_client.get.assert_called_once_with("kb:key1")

    # Test get miss
    mock_client.get.return_value = None
    assert cache.get("kb:key2") is None

    # Test delete
    assert cache.delete("kb:key1") is True
    mock_client.delete.assert_called_with("kb:key1")

    # Test invalidate tenant
    mock_client.keys.return_value = [b"kb:articles:tenant-1:draft", b"kb:health:tenant-1"]
    mock_client.delete.return_value = 2
    count = cache.invalidate_tenant("tenant-1")
    assert count == 2
    mock_client.keys.assert_called_once_with("kb:*:tenant-1:*")
