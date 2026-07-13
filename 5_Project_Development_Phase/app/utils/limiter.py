import time
from functools import wraps

from flask import jsonify, request

# Simple in-memory rate limiter store: {ip: [timestamps]}
_rate_limits = {}


def rate_limit(limit_count: int = 60, period_seconds: int = 60):
    """
    Decorator to apply basic client IP rate limiting on endpoints.
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            from flask import current_app

            if current_app and current_app.testing:
                return f(*args, **kwargs)

            ip = request.remote_addr
            now = time.time()

            # Clean old timestamps
            if ip in _rate_limits:
                _rate_limits[ip] = [t for t in _rate_limits[ip] if now - t < period_seconds]
            else:
                _rate_limits[ip] = []

            if len(_rate_limits[ip]) >= limit_count:
                return jsonify({"error": "Rate limit exceeded. Too many requests."}), 429

            _rate_limits[ip].append(now)
            return f(*args, **kwargs)

        return wrapped

    return decorator
