"""Represents error classes related to chatbot flow structure and analysis.

Classes:
  * FlowError - Represents general chatbot flow structure error.
  * FlowParameterError - Represents parameter error in flow structure.
"""

from __future__ import annotations

__all__ = [
    "FlowError",
    "FlowParameterError",
    "FlowTypeError",
    "LongScriptError",
    "LongScriptParameterError",
]

from .flow_error import (
    FlowError,
    FlowParameterError,
    FlowTypeError,
)
from .long_script_error import (
    LongScriptError,
    LongScriptParameterError,
)
