from .utils.converter_class import Converter
from .utils.unit_class import Unit
from .utils.units_class import Units

# Collect all unit groups inside this class instance
_UNITS = Units()

#################################################################################################
#   ADD YOUR OWN UNIT GROUPS BELOW                                                              #
#################################################################################################

# GUIDELINES:
# 1. GROUP NAMES MUST BE UNIQUE
# 2. ALL UNIT NAMES AND SYNONYMNS MUST BE UNIQUE
# 3. EACH UNIT GROUP MUST HAVE EXACTLY ONE DEFAULT (SI) UNIT
# 4. CONVERTER FUNCTIONS MUST HAVE ONE ARGUMENT AND RETURN A SCALAR
# (Automatic tests will be run to check that all unit groups and unit names/synonyms are unique.)


_UNITS.add_group(
    group_name="time",
    units=[
        Unit("sec", synonyms=["second", "seconds", "s"], is_si_unit=True),
        Unit("min", synonyms=["minute", "minutes"]),
        Unit("hr", synonyms=["hour", "hours"]),
    ],
    converters=[
        Converter("sec", "hr", lambda sec: sec / 60 / 60),
        Converter("hr", "sec", lambda hr: hr * 60 * 60),
        Converter("sec", "min", lambda sec: sec / 60),
        Converter("min", "sec", lambda min: min * 60),
        Converter("hr", "min", lambda sec: sec * 60),
        Converter("min", "hr", lambda min: min / 60),
    ],
)


_UNITS.add_group(
    group_name="length",
    units=[
        Unit("m", synonyms=["meter", "meters"], is_si_unit=True),
        Unit("mm", synonyms=["milli meter", "millimeter"]),
        Unit("cm", synonyms=["centi meter", "centimeter"]),
        Unit("ft", synonyms=["foot", "feet"]),
        Unit("in", synonyms=["inch", "inches"]),
    ],
    converters=[
        Converter("mm", "m", lambda mm: mm / 1000.0),
        Converter("cm", "m", lambda cm: cm / 100.0),
        Converter("ft", "m", lambda ft: ft * 0.3048),
        Converter("in", "m", lambda inch: inch * 0.0254),
        Converter("m", "mm", lambda m: m * 1000.0),
        Converter("m", "cm", lambda m: m * 100.0),
        Converter("m", "ft", lambda m: m / 0.3048),
        Converter("m", "in", lambda m: m / 0.0254),
    ],
)


_UNITS.add_group(
    group_name="mass",
    units=[Unit("kg", is_si_unit=True), Unit("lb", synonyms=["lbs"]), Unit("g")],
    converters=[
        Converter("kg", "lb", lambda kg: kg * 2.20462),
        Converter("lb", "kg", lambda lb: lb / 2.20462),
        Converter("g", "kg", lambda g: g / 1000),
        Converter("kg", "g", lambda kg: kg * 1000),
    ],
)


_UNITS.add_group(
    group_name="temperature",
    units=[
        Unit("k", synonyms=["kelvin"], is_si_unit=True),
        Unit("c", synonyms=["celsius", "°c"]),
        Unit("f", synonyms=["fahrenheit", "°f"]),
    ],
    converters=[
        Converter("k", "f", lambda k: (k - 273.15) * (9 / 5) + 32),
        Converter("k", "c", lambda k: k - 273.15),
        Converter("c", "k", lambda c: c + 273.15),
        Converter("c", "f", lambda c: c * (9 / 5) + 32),
        Converter("f", "k", lambda f: (f - 32) * (5 / 9) + 273.15),
        Converter("f", "c", lambda f: (f - 32) * (5 / 9)),
    ],
)


_UNITS.add_group(
    group_name="pressure",
    units=[Unit("pa", synonyms=["pascal"], is_si_unit=True), Unit("psi")],
    converters=[Converter("psi", "pa", lambda psi: psi * 6894.76), Converter("pa", "psi", lambda pa: pa / 6894.76)],
)


_UNITS.add_group(
    group_name="flow rate",
    units=[
        Unit("m3s", synonyms=["m3/s", "m³/s"], is_si_unit=True),
        Unit("m3min", synonyms=["m3/min"]),
        Unit("m3hrs", synonyms=["m3/hrs", "m3/hr", "m3hr"]),
        Unit("mmscfd", synonyms=["mmscf/d"]),
        Unit("usgpm"),
        Unit("usgpd"),
        Unit("mbpd", synonyms=["mbod"]),
        Unit("bpd", synonyms=["bbl/d", "bbld", "bopd", "bwpd"]),
    ],
    converters=[
        Converter("m3s", "m3min", lambda m3s: m3s * 60.0),
        Converter("m3s", "m3hrs", lambda m3s: m3s * 3600.0),
        Converter("m3s", "mmscfd", lambda m3s: m3s / 0.32774128),
        Converter("m3s", "mbpd", lambda m3s: m3s / 0.00184013),
        Converter("m3s", "usgpm", lambda m3s: m3s * 15850),
        Converter("m3s", "usgpd", lambda m3s: m3s * 15850 * 1440),
        Converter("m3s", "bpd", lambda m3s: m3s / 0.0000018401307),
        Converter("m3min", "m3s", lambda m3min: m3min / 60.0),
        Converter("m3hrs", "m3s", lambda m3hrs: m3hrs / 3600.0),
        Converter("mmscfd", "m3s", lambda mmscf: mmscf * 0.32774128),
        Converter("mbpd", "m3s", lambda mbpd: mbpd * 0.00184013),
        Converter("usgpm", "m3s", lambda usgpm: usgpm / 15850),
        Converter("usgpd", "m3s", lambda usgpd: usgpd / (15850 * 1440)),
        Converter("bpd", "m3s", lambda bpd: bpd * 0.0000018401307),
    ],
)


_UNITS.add_group(
    group_name="density",
    units=[
        Unit("kgm3", synonyms=["kg/m3", "kg/m³"], is_si_unit=True),
        Unit("lbft3", synonyms=["lb/ft3", "lb/ft³"]),
        Unit("sg", synonyms=["s.g.", "sp.gr."]),
    ],
    converters=[
        Converter("kgm3", "sg", lambda kgm3: kgm3 / 1000),
        Converter("sg", "kgm3", lambda sg: sg * 1000),
        Converter("kgm3", "lbft3", lambda kgm3: kgm3 / 16.01846),
        Converter("lbft3", "kgm3", lambda lbft3: lbft3 * 16.01846),
    ],
)


_UNITS.add_group(
    group_name="viscosity",
    units=[Unit("pas", synonyms=["pascalseconds"], is_si_unit=True), Unit("cp", synonyms=["centipoise"])],
    converters=[Converter("cp", "pas", lambda cp: cp * 0.001), Converter("pas", "cp", lambda pas: pas / 0.001)],
)


_UNITS.add_group(
    group_name="surface tension",
    units=[
        Unit("nm", synonyms=["n/m", "newton/m", "newton/meter"], is_si_unit=True),
        Unit("dyncm", synonyms=["dyn/cm", "dyne/cm", "dynes/cm"]),
    ],
    converters=[Converter("nm", "dyncm", lambda nm: nm * 1000), Converter("dyncm", "nm", lambda dyncm: dyncm / 1000)],
)


_UNITS.add_group(
    group_name="flow coefficient",
    units=[
        Unit("m3spa", synonyms=["(m3/s)/pa", "m3s/pa", "m3/spa"], is_si_unit=True),
        Unit("usgpmpsi", synonyms=["usgpm/psi"], is_si_unit=False),
        Unit("m3hbar", synonyms=["(m3/h)/bar", "m3h/bar", "m3/hbar"], is_si_unit=False),
    ],
    converters=[
        Converter("usgpmpsi", "m3hbar", lambda cv: cv * 0.865),
        Converter("usgpmpsi", "m3spa", lambda cv: cv * 3.2113 ** (-9)),
        Converter("m3hbar", "usgpmpsi", lambda cv: cv * 1.156),
        Converter("m3spa", "usgpmpsi", lambda cv: cv / 3.2113 ** (-9)),
    ],
)
