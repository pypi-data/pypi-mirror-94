class InvalidPoint(Exception):
    def __str__(self):
        return "point's dimension must be 2."


class InvalidLinearRing(Exception):
    """invalid linear ring."""


class EnclosingBothPoles(Exception):
    """not support linear ring enclosing north and south poles."""


class InvalidLinearRingEnclosingPole(Exception):
    """invalid linear ring enclosing the pole."""


class InvalidBounds(Exception):
    """invalid bounds."""


class NotAllowedWarpBounds(Exception):
    """not support warpping bounds."""


class NotAllowedCwLinearRing(Exception):
    """not support cw linear ring."""


class InvalidSelfintersection(Exception):
    """invalid selfintersection."""


class FalidCuttingAntimeridian(Exception):
    """falid cutting antimeridian."""
