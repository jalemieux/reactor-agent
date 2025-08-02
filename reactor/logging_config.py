import logging
import sys
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log messages for better terminal readability.
    """
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        # Add color to the level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        
        # Add color to the message based on level
        if record.levelno >= logging.ERROR:
            record.msg = f"{Fore.RED}{record.msg}{Style.RESET_ALL}"
        elif record.levelno >= logging.WARNING:
            record.msg = f"{Fore.YELLOW}{record.msg}{Style.RESET_ALL}"
        
        return super().format(record)


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    use_colors: bool = True,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration with terminal-friendly formatting.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Optional file path to write logs to
        use_colors: Whether to use colored output (default: True)
        format_string: Custom format string (optional)
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('reactor')
    logger.setLevel(level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Default format string
    if format_string is None:
        format_string = (
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )
    
    # Create formatter
    if use_colors:
        formatter = ColoredFormatter(format_string)
    else:
        formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        # Use non-colored formatter for file output
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance with the current configuration.
    
    Args:
        name: Logger name (defaults to 'reactor')
    
    Returns:
        Logger instance
    """
    if name is None:
        name = 'reactor'
    return logging.getLogger(name)


# Convenience function for quick setup
def quick_setup(level: int = logging.INFO) -> logging.Logger:
    """
    Quick setup for basic terminal-friendly logging.
    
    Args:
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    return setup_logging(level=level, use_colors=True) 