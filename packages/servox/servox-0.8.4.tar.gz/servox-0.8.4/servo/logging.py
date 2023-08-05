"""The `servo.logging` module provides standard logging capabilities to the
servo package and its dependencies.

Logging is implemented on top of the
[loguru](https://loguru.readthedocs.io/en/stable/) library.
"""
from __future__ import annotations

import asyncio
import functools
import logging
import pathlib
import sys
import time
import traceback
from typing import Any, Awaitable, Callable, Dict, Optional, Union

import loguru

import servo.events

__all__ = (
    "Mixin",
    "Filter",
    "ProgressHandler",
    "logger",
    "log_execution",
    "log_execution_time",
    "reset_to_defaults",
    "set_level",
)

# Alias the loguru default logger
logger = loguru.logger


class Mixin:
    """The `servo.logging.Mixin` class is a convenience class for adding
    logging capabilities to arbitrary classes through multiple inheritance.
    """

    @property
    def logger(self) -> loguru.Logger:
        """Returns the servo package logger"""
        global logger
        return logger


class Filter:
    """
    NOTE: The level on the sink needs to be set to 0.
    """

    def __init__(self, level="INFO") -> None:
        self.level = level

    def __call__(self, record) -> bool:
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


class ProgressHandler:
    """
    The ProgressHandler class provides transparent integration between logging events and
    API based reporting to Opsani. Log messages annotated with a "progress" attribute are
    automatically picked up by the handler and reported back to the API via a callback.

    NOTE: We call the logger re-entrantly for misconfigured progress logging attempts. The
        `progress` must be excluded on logger calls to avoid recursion.
    """

    def __init__(
        self,
        progress_reporter: Callable[[Dict[Any, Any]], Union[None, Awaitable[None]]],
        error_reporter: Optional[Callable[[str], Union[None, Awaitable[None]]]] = None,
        exception_handler: Optional[
            Callable[[Exception], Union[None, Awaitable[None]]]
        ] = None,
    ) -> None:
        self._progress_reporter = progress_reporter
        self._error_reporter = error_reporter
        self._exception_handler = exception_handler
        self._queue = asyncio.Queue()
        self._queue_processor = None

    async def sink(self, message: loguru.Message) -> None:
        """An asynchronous loguru sink handling the progress reporting.
        Implemented as a sink versus a `logging.Handler` because the Python stdlib logging package isn't async.
        """
        if self._queue_processor is None:
            self._queue_processor = asyncio.create_task(self._process_queue())

        record = message.record
        extra = record["extra"]
        progress = extra.get("progress", None)
        if not progress:
            return

        # Favor explicit connector in extra (see Mixin) else use the context var
        connector = extra.get("connector", servo.events._connector_context_var.get())
        if not connector:
            return await self._report_error(
                "declining request to report progress for record without a connector attribute",
                record,
            )

        event_context: Optional[
            servo.events.EventContext
        ] = servo.events._event_context_var.get()
        operation = extra.get("operation", None)
        if not operation:
            if not event_context:
                return await self._report_error(
                    "declining request to report progress for record without an operation parameter or inferrable value from event context",
                    record,
                )
            operation = event_context.operation()

        started_at = extra.get("started_at", None)
        if not started_at:
            if event_context:
                started_at = event_context.created_at
            else:
                return await self._report_error(
                    "declining request to report progress for record without a started_at parameter or inferrable value from event context",
                    record,
                )

        connector_name = connector.name if hasattr(connector, "name") else connector

        self._queue.put_nowait(
            dict(
                operation=operation,
                progress=progress,
                connector=connector_name,
                event_context=event_context,
                started_at=started_at,
                message=message,
            )
        )

    async def shutdown(self) -> None:
        """Shutdown the progress handler by emptying the queue and releasing the queue processor."""
        await self._queue.join()
        self._queue_processor.cancel()
        await asyncio.gather(self._queue_processor, return_exceptions=True)

    async def _process_queue(self) -> None:
        while True:
            try:
                progress = await self._queue.get()
                if progress is None:
                    break

                if asyncio.iscoroutinefunction(self._progress_reporter):
                    await self._progress_reporter(**progress)
                else:
                    self._progress_reporter(**progress)
            except asyncio.CancelledError:
                pass  # Task cancellation should not be logged as an error.
            except Exception as error:  # pylint: disable=broad-except
                if self._exception_handler:
                    if asyncio.iscoroutinefunction(self._exception_handler):
                        await self._exception_handler(error)
                    else:
                        self._exception_handler(error)
            finally:
                self._queue.task_done()

    async def _report_error(self, message: str, record) -> None:
        """
        Report an error message about rocessing a log message annotated with a `progress` attribute.
        """
        message = f"!!! WARNING: {record['name']}:{record['file'].name}:{record['line']} | servo.logging.ProgressHandler - {message}"
        if self._error_reporter:
            if asyncio.iscoroutinefunction(self._error_reporter):
                await self._error_reporter(message)
            else:
                self._error_reporter(message)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <magenta>{extra[component]}</magenta> - <level>{message}</level>"
    "{extra[traceback]}"
)


class Formatter:
    def __call__(self, record: dict) -> str:
        """
        Formats a log message with contextual information from the servo assembly.
        """
        extra = record["extra"]

        # Add optional traceback
        if extra.get("with_traceback", False):
            extra["traceback"] = "\n" + "".join(traceback.format_stack())
        else:
            extra["traceback"] = ""

        # Respect an explicit component
        if not "component" in record["extra"]:
            # Favor explicit connector from the extra dict or use the context var
            if connector := extra.get(
                "connector", servo.events._connector_context_var.get()
            ):
                component = connector.name
            else:
                component = "servo"

            # Append event context if available
            event_context = servo.events._event_context_var.get()
            if event_context:
                component += f"[{event_context}]"

            extra["component"] = component

        return DEFAULT_FORMAT + "\n{exception}"


DEFAULT_FILTER = Filter("INFO")
DEFAULT_FORMATTER = Formatter()


DEFAULT_STDERR_HANDLER = {
    "sink": sys.stderr,
    "filter": DEFAULT_FILTER,
    "level": 0,
    "format": DEFAULT_FORMATTER,
    "backtrace": True,
    "diagnose": True,
}


# Persistent disk logging to logs/
root_path = pathlib.Path(__file__).parents[1]
logs_path = root_path / "logs" / f"servo.log"


DEFAULT_FILE_HANDLER = {
    "sink": logs_path,
    "colorize": False,
    "filter": DEFAULT_FILTER,
    "level": 0,
    "format": DEFAULT_FORMATTER,
    "backtrace": True,
    "diagnose": False,
}

DEFAULT_HANDLERS = [
    DEFAULT_STDERR_HANDLER,
    DEFAULT_FILE_HANDLER,
]


def set_level(level: str) -> None:
    """
    Sets the logging threshold to the given level for all log handlers.
    """
    DEFAULT_FILTER.level = level


def set_colors(colors: bool) -> None:
    """Sets whether ANSI colored output will be emitted to the logs.

    Args:
        colors (bool): Whether or not to color log output.
    """
    DEFAULT_STDERR_HANDLER["colorize"] = colors
    loguru.logger.remove()
    loguru.logger.configure(handlers=DEFAULT_HANDLERS)


def reset_to_defaults() -> loguru.Logger:
    """
    Resets the logging subsystem to the default configuration and returns the logger instance.
    """
    DEFAULT_FILTER.level = "INFO"
    DEFAULT_STDERR_HANDLER["colorize"] = None

    loguru.logger.remove()
    loguru.logger.configure(handlers=DEFAULT_HANDLERS)

    # Intercept messages from backoff library
    logging.getLogger("backoff").addHandler(InterceptHandler())

    return logger


def friendly_decorator(f):
    """
    Returns a "decorator decorator" that wraps a decorator function such that it can be invoked
    with or without parentheses such as:

        @decorator(with, arguments, and=kwargs)
        or
        @decorator
    """

    @functools.wraps(f)
    def decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)

    return decorator


@friendly_decorator
def log_execution(func, *, entry=True, exit=True, level="DEBUG"):
    """
    Log the execution of the decorated function.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        name = func.__name__
        logger_ = logger.opt(depth=1)
        if entry:
            logger_.log(level, f"Entering '{name}' (args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        if exit:
            logger_.log(level, f"Exiting '{name}' (result={result})")
        return result

    return wrapped


@friendly_decorator
def log_execution_time(func, *, level="DEBUG"):
    """
    Log the execution time upon exit from the decorated function.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        from servo.types import Duration

        name = func.__name__
        logger_ = logger.opt(depth=1)

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        duration = Duration(end - start)
        logger_.log(level, f"Function '{name}' executed in {duration}")
        return result

    return wrapped


# Alias the loguru logger to hide implementation details
logger = reset_to_defaults()
