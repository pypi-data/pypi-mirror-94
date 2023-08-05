"""CG635 Instrument"""
from functools import wraps
from srs_cg635.common import get_idn, InstrumentBase, Error

ERRORMSG = {
    "0": "No Error",
    "10": "Illegal Value",
    "20": "Frequency Error",
    "30": "Phase Error",
    "31": "Phase Step Error",
    "40": "Voltage Error",
    "51": "Q/Q~ Low Changed",
    "52": "Q/Q~ High Changed",
    "61": "CMOS Low Changed",
    "62": "CMOS High Changed",
    "71": "No PRBS",
    "72": "Failed Self Test",
    "100": "Lost Data",
    "102": "No Listener",
    "110": "Illegal Command",
    "111": "Undefined Command",
    "112": "Illegal Query",
    "113": "Illegal Set",
    "114": "Null Parameter",
    "115": "Extra Parameters",
    "116": "Missing Parameters",
    "117": "Parameter Overflow",
    "118": "Invalid Floating Point Number",
    "120": "Invalid Integer",
    "122": "Invalid Hexadecimal",
    "126": "Syntax Error",
    "151": "Failed ROM Check",
    "152": "Failed 24 V Out of Range",
    "153": "Failed 19.44 MHz Low Rail",
    "154": "Failed 19.44 MHz High Rail",
    "155": "Failed 19.40 MHz Low Rail",
    "156": "Failed 19.40 MHz High Rail",
    "157": "Failed RF at 2 GHz",
    "158": "Failed RF at 1 GHz",
    "159": "Failed CMOS Low Spec.",
    "160": "Failed CMOS High Spec.",
    "161": "Failed Q/Q~ Low Spec.",
    "162": "Failed Q/Q~ High Spec.",
    "163": "Failed Optional Timebase",
    "164": "Failed Clock Symmetry",
    "254": "Too Many Errors",
}

DISPLAYTYPE = {
    "0": "Frequency",
    "Frequency": "0",
    "1": "Phase",
    "Phase": "1",
    "2": "Q/Q~ high",
    "3": "Q/Q~ low",
    "4": "CMOS high",
    "5": "CMOS low",
    "6": "Frequency step",
    "Frequency step": "6",
    "7": "Phase step",
    "Phase step": "7",
    "8": "Q/Q~ high step",
    "9": "Q/Q~ low step",
    "10": "CMOS high step",
    "11": "CMOS low step",
    "-1": "Status display",
}

TIMEBASE = {"0": "Internal", "1": "OCXO", "2": "Rubidium", "3": "External"}

STOPLEVEL = {
    "0": "low",
    "low": "0",
    "1": "high",
    "high": "1",
    "2": "toggle",
    "toggle": "2",
}

STANDARDCMOS = {"1.2 V": "0", "1.8 V": "1", "2.5 V": "2", "3.3 V": "3", "5.0 V": "4"}
STANDARDQ = {
    "ECL": "0",
    "+7 dBm": "1",
    "LVDS": "2",
    "3.3 V PECL": "3",
    "5.0 V PECL": "4",
}

LOCKSTATUS = [
    "RF unlock",
    "19 MHz unlock",
    "10 MHz unlock",
    "Rubidium unlock",
    "Output disabled",
    "Phase shift",
]


def validate(func):
    """Decorator to check for error when setting a parameter"""

    @wraps(func)
    def inner(*args, **kwargs):
        # pylint:disable=protected-access
        self = args[0]
        self._visa.write("*CLS;*ESE 61;*SRE 32")
        func(*args, **kwargs)
        self._visa.write("*OPC")
        self._visa.wait_for_srq()
        if self._visa.stb & 32 and int(self._visa.query("*ESR?")) > 1:
            raise Error(ERRORMSG[self._visa.query("LERR?")])
        self._visa.write("*ESE 0;*SRE 0")

    return inner


class CG635(InstrumentBase):
    """CG635"""

    def __init__(self, visa):
        super().__init__(visa)
        self._visa.write("*CLS;*ESE 0")
        self._visa.read_termination = "\n"
        self._idn = get_idn(visa)

    @property
    def model(self):
        """Return model number

        Returns
        ----------
        model : str
        """
        return self._idn.model

    @property
    def serial_number(self):
        """Return serial number

        Returns
        -------
        serial_number : str
        """
        return self._idn.serial_number

    @property
    def firmware_version(self):
        """Return firmware version

        Returns
        -------
        firmware_version : str
        """
        return self._idn.firmware_version

    def __repr__(self):
        return f"<SRS {self.model} at {self._visa.resource_name}>"

    def reset(self):
        """Reset the instrument"""
        self._visa.write("*RST;*WAI")

    @property
    def frequency(self):
        """Output frequency

        Parameters
        ----------
        value : float in hertz

        Returns
        -------
        value : float in hertz
        """
        return float(self._visa.query("FREQ?"))

    @frequency.setter
    @validate
    def frequency(self, value):
        self._visa.write(f"FREQ {value}")

    def _query(self, value):
        return self._visa.query(value)

    def _write(self, value):
        self._visa.write(value)

    @property
    def _stb(self):
        return self._visa.stb

    @property
    def cmos_levels(self):
        """CMOS output voltage levels

        Parameters
        ----------
        value : tuple of floats (low, high) or str
            low : float in volts
            high : float in volts
            standard : str {'1.2 V', '1.8 V', '2.5 V', '3.3 V', '5.0 V'}

        Returns
        -------
        (low, high) : tuple of floats
        """
        high = float(self._visa.query("CMOS? 1"))
        low = float(self._visa.query("CMOS? 0"))
        return (low, high)

    @cmos_levels.setter
    @validate
    def cmos_levels(self, value):
        if isinstance(value, tuple):
            low, high = value
            self._visa.write(f"CMOS 0,{low};CMOS 1,{high}")
        else:
            self._visa.write(f"STDC {STANDARDCMOS[value]}")

    @property
    def q_qbar_levels(self):
        """Q/Q~ output voltage levels

        Parameters
        ----------
        value : tuple of floats (low, high) or str
            low : float in volts
            high : float in volts
            standard : str {'ECL', '+7 dBm', 'LVDS', '3.3 V PECL', '5.0 V PECL'}

        Returns
        -------
        (low, high) : tuple of floats
        """
        high = float(self._visa.query("QOUT? 1"))
        low = float(self._visa.query("QOUT? 0"))
        return (low, high)

    @q_qbar_levels.setter
    @validate
    def q_qbar_levels(self, value):
        if isinstance(value, tuple):
            low, high = value
            self._visa.write(f"QOUT 0,{low};QOUT 1,{high}")
        else:
            self._visa.write(f"STDQ {STANDARDQ[value]}")

    @property
    def display_type(self):
        """Display type

        Parameters
        ----------
        value : str {'Frequency', 'Frequency step', 'Phase', 'Phase step'}

        Returns
        -------
        displaytype : str
        """
        return DISPLAYTYPE[self._visa.query("DISP?")]

    @display_type.setter
    @validate
    def display_type(self, value):
        self._visa.write(f"DISP {DISPLAYTYPE[value]}")

    @property
    def phase(self):
        """Phase

        Parameters
        ----------
        value : float in degrees

        Returns
        -------
        phase : float in degrees
        """
        return float(self._visa.query("PHAS?"))

    @phase.setter
    @validate
    def phase(self, value):
        self._visa.write(f"PHAS {value}")

    @property
    def timebase(self):
        """Return the current timebase"""
        return TIMEBASE[self._visa.query("TIMB?")]

    def run(self):
        """Generate output clock signals"""
        self._visa.write("RUNS 1")

    def stop(self, level="low"):
        """Stop clock generation

        Parameters
        ----------
        level : str {'low', 'high', 'toggle'}
        """
        self._visa.write(f"SLVL {STOPLEVEL[level]};RUNS 0")

    @property
    def display_state(self):
        """Display state

        Parameters
        ----------
        value : str {'ON', 'OFF'}

        Returns
        -------
        state : str
        """
        shdp = bool(int(self._visa.query("SHDP?")))
        return "ON" if shdp else "OFF"

    @display_state.setter
    @validate
    def display_state(self, value):
        shdp = 0 if value == "OFF" else 1
        self._visa.write(f"SHDP {shdp}")

    def self_test(self):
        """Perform self test

        Raises Error if unsuccessful
        """
        original_timeout = self._visa.timeout
        self._visa.timeout = 10000  # ms
        error = int(self._visa.query("*TST?"))
        if error:
            raise Error(self._visa.query("LERR?"))
        self._visa.timeout = original_timeout
        # clear lock status since self test unlocks timebase
        self.lock_status  # pylint:disable=pointless-statement

    @property
    def lock_status(self):
        """Return PLL lock status

        The lock status register is sticky and requires reading it to
        clear a previous status."""
        msg = []
        status = int(self._visa.query("LCKR?"))
        for i in range(6):
            if status & 2 ** i:
                msg.append(LOCKSTATUS[i])
        return ", ".join(msg)
