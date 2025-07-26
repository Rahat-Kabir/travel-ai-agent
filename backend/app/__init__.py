"""
Travel Agent API application package.
"""

from .main import app, create_app

__version__ = "1.0.0"

__all__ = [
    "app",
    "create_app",
    "__version__",
]
