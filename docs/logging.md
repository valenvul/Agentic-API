# Logging Setup with Loguru

## Overview

This project uses [Loguru](https://loguru.readthedocs.io/) as its logging library instead of Python's standard `logging` module. Loguru provides a simpler API, better formatting, and more powerful features out of the box.

The challenge is that many third-party libraries (e.g. FastAPI, uvicorn, sqlalchemy) use Python's standard `logging` internally. To get all logs flowing through Loguru with consistent formatting, we intercept those standard logs and redirect them.

---

## Dependencies

```
loguru
```

---

## Required Imports

```python
import logging
from types import FrameType
from typing import cast
from loguru import logger
```

---

## The InterceptHandler

This class is the bridge between standard `logging` and Loguru.

```python
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Step 1: Translate the log level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Step 2: Find the true caller in the original code
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1

        # Step 3: Log through Loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )
```

### What each step does

**Step 1 — Level translation**
`record.levelname` is a standard logging level string like `"INFO"` or `"WARNING"`.
We look up the matching Loguru level by name. If it doesn't exist (e.g. a custom level),
we fall back to its numeric value as a string.

**Step 2 — Caller discovery**
Without this, every log line would point to somewhere inside Python's `logging/__init__.py`
rather than your actual code. This walks up the call stack until it exits the logging
internals, tracking the depth so Loguru knows where the real caller is.
`cast(FrameType, ...)` is only for static type checkers — it does nothing at runtime.

**Step 3 — Emit via Loguru**
`logger.opt(depth=depth)` tells Loguru to skip the right number of frames when reporting
the source file and line number. `exception=record.exc_info` forwards any exception
so Loguru can format the traceback properly.

---

## Wiring It Up

After defining `InterceptHandler`, you need to attach it to Python's root logger and
to any specific loggers used by your libraries (e.g. uvicorn):

```python
def setup_app_logging(config: Settings) -> None:
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")

    # Attach InterceptHandler to the root logger — captures all standard logging
    logging.getLogger().handlers = [InterceptHandler()]

    # Optionally target specific library loggers with an explicit level
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    # Configure Loguru's output sink and level
    # logger.configure() replaces all existing Loguru handlers at once (preferred over logger.add())
    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    )
```

Call `setup_app_logging()` once at application startup, before the app starts serving
requests (e.g. in `main.py`).

---

## Usage in Code

Once set up, use Loguru's `logger` directly everywhere:

```python
from loguru import logger

logger.info("Server started")
logger.warning("Something looks off")
logger.error("Something failed")
logger.debug("Detailed debug info")
```

Third-party libraries that use standard `logging` internally will also have their logs
captured and formatted by Loguru automatically.

---

---

## Request Logging Middleware

To log every incoming HTTP request (method, path, status code, and duration), add a middleware to your FastAPI app in `main.py`.

```python
import time
from loguru import logger

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} ({duration_ms:.1f}ms)"
    )
    return response
```

**How it works:**
- `@app.middleware("http")` — registers the function to intercept every HTTP request
- `call_next(request)` — forwards the request to the actual route handler and waits for the response; code before this runs pre-request, code after runs post-response
- `time.perf_counter()` — high precision timer used to measure request duration in milliseconds
- The log line produced looks like: `POST /api/v1/prediction - 200 (12.3ms)`

This must be registered **after** `setup_app_logging()` is called so that Loguru is already configured when the first request arrives.

---

## References

- [Loguru documentation](https://loguru.readthedocs.io/)
- [Loguru — compatible with standard logging](https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging)
