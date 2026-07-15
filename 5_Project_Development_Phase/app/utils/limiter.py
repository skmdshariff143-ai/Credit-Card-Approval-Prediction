import os
import time
import logging
from functools import wraps
from flask import jsonify, request

# Configure logger
logger = logging.getLogger("cg_limiter")

# Simple in-memory rate limiter store fallback: {ip: [timestamps]}
_rate_limits = {}

# Initialize Redis client if REDIS_URL is present
_redis_client = None
redis_url = os.getenv("REDIS_URL")

if redis_url:
    try:
        import redis

        # Set short socket timeout to prevent blocking Flask thread if Redis is slow/down
        _redis_client = redis.Redis.from_url(redis_url, socket_timeout=3, decode_responses=True)
        # Test connection ping
        _redis_client.ping()
        logger.info("Rate limiter successfully initialized with shared Redis store.")
    except Exception as e:
        logger.warning(f"Failed to connect to Redis for rate limiting. Falling back to in-memory store. Error: {e}")
        _redis_client = None


def _is_redis_limited(ip: str, path: str, limit_count: int, period_seconds: int) -> bool:
    """Helper to execute rate limit checks in Redis."""
    if _redis_client is None:
        return False
    key = f"rate_limit:{ip}:{path}"
    try:
        current = _redis_client.incr(key)
        if current == 1:
            _redis_client.expire(key, period_seconds)
        return current > limit_count
    except Exception as e:
        logger.error(f"Redis rate limiting failed. Error: {e}")
        return False


def _is_memory_limited(ip: str, limit_count: int, period_seconds: int) -> bool:
    """Helper to execute rate limit checks in memory."""
    now = time.time()
    if ip not in _rate_limits:
        _rate_limits[ip] = []
    _rate_limits[ip] = [t for t in _rate_limits[ip] if now - t < period_seconds]
    if len(_rate_limits[ip]) >= limit_count:
        return True
    _rate_limits[ip].append(now)
    return False


def rate_limit(limit_count: int = 60, period_seconds: int = 60):
    """
    Decorator to apply client IP rate limiting on endpoints.
    Uses Upstash Redis store if configured, otherwise falls back to local in-memory store.
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            from flask import current_app

            # Bypass rate limit checks during testing
            if current_app and current_app.testing:
                return f(*args, **kwargs)

            ip = request.remote_addr
            path = request.path

            # Attempt Redis-backed rate limiting
            if _redis_client is not None:
                if _is_redis_limited(ip, path, limit_count, period_seconds):
                    logger.warning(f"Rate limit exceeded for IP {ip} on path {path} (Redis store).")
                    return jsonify({"error": "Rate limit exceeded. Too many requests."}), 429
                return f(*args, **kwargs)

            # Fallback to local in-memory store
            if _is_memory_limited(ip, limit_count, period_seconds):
                logger.warning(f"Rate limit exceeded for IP {ip} on path {path} (In-memory store).")
                return jsonify({"error": "Rate limit exceeded. Too many requests."}), 429

            return f(*args, **kwargs)

        return wrapped

    return decorator
