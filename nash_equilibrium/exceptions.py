"""
Custom exceptions for Nash Equilibrium Finder

This module defines custom exception classes for better error handling.
"""


class NashEquilibriumError(Exception):
    """Base exception class for Nash Equilibrium Finder errors."""

    pass


class GameValidationError(NashEquilibriumError):
    """Raised when game validation fails."""

    pass


class StrategyValidationError(NashEquilibriumError):
    """Raised when strategy validation fails."""

    pass


class PayoffCalculationError(NashEquilibriumError):
    """Raised when payoff calculation fails."""

    pass


class MixedStrategyError(NashEquilibriumError):
    """Raised when mixed strategy calculation fails."""

    pass
