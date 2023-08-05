"""Python interface to the SRS CG635 Clock Generator"""
import pyvisa
from srs_cg635.version import __version__
from srs_cg635.common import get_idn
from srs_cg635.instrument import CG635

__all__ = ["CommChannel"]


class CommChannel:
    """Connect to a Stanford Research Systems CG635 using GPIB

    Attributes
    ----------
        address : int
            instrument's GPIB address, e.g. 23
        controller : int
            GPIB controller primary address, e.g. 0

    Returns:
        CommChannel or Lightning
    """

    def __init__(self, address=23, controller=0):
        self._address = address
        self._controller = controller
        self._rm = pyvisa.ResourceManager()
        self._visa = self._rm.open_resource(f"GPIB{controller}::{address}::INSTR")
        self._visa.read_termination = "\n"

    def __enter__(self):
        idn = get_idn(self._visa)
        if idn.manufacturer.lower() != "stanford research systems":
            raise ValueError(f"Device at {self._address} is a not a SRS instrument")
        return CG635(self._visa)

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._visa.close()
        self._rm.close()

    def get_instrument(self):
        """Return the PowerMeter instrument object"""
        return self.__enter__()

    def close(self):
        """Close the CommChannel"""
        self.__exit__(None, None, None)


def __dir__():
    return ["CommChannel", "__version__"]
