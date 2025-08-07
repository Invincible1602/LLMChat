# utils/logging_utils.py
import sys
import os
from pathlib import Path
from loguru import logger
from config.settings import settings # Import settings to get LOG_LEVEL

# This global logger instance will be configured by setup_logging()
# and then directly used by other modules.

def setup_logging():
    """
    Configures application logging with loguru.
    This function should be called once at the application's startup (e.g., in app.py).
    It sets up console logging and an optional file logger.
    """
    # Clear any existing handlers to prevent duplicate logs if called multiple times
    logger.remove()
    
    # Define the log message format for both console and file output
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Add console handler (logs to standard error)
    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.LOG_LEVEL, # Use LOG_LEVEL from settings
        backtrace=True, # Show traceback for exceptions
        diagnose=True, # Provide detailed diagnostics in tracebacks
    )
    
    # Add file handler for persistent logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True) # Create 'logs' directory if it doesn't exist
    
    logger.add(
        log_dir / "app.log", # Log file path
        rotation="10 MB", # Rotate log file when it reaches 10 MB
        retention="1 week", # Keep log files for one week
        format=log_format,
        level=settings.LOG_LEVEL, # Use LOG_LEVEL from settings
        backtrace=True,
        diagnose=True,
        enqueue=True # Use a queue for non-blocking file logging (improves performance)
    )
    
    # Log startup information
    logger.info(f"Logging initialized at level {settings.LOG_LEVEL}")
    
    return logger # Return the configured logger instance

def get_logger(name: str = "chatbot_module"):
    """
    Returns the globally configured Loguru logger instance.
    This function is primarily for consistency and to allow modules to
    get a logger instance after setup_logging has been called.
    
    Args:
        name: An optional name for the logger, which will be bound to the messages.
              This helps identify the source module in logs.
    
    Returns:
        A Loguru logger instance.
    """
    # The logger is already configured by setup_logging, so we just return it.
    # Binding the name helps in identifying logs from different modules.
    return logger.bind(name=name)

