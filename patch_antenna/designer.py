"""
Patch Antenna Designer - Enhanced Edition

Originally developed by Bhanuchander Udhayakumar (github.com/bhanuchander210)
Enhanced by Al-Musbahi for Leeds SpaceComms

Advanced rectangular patch antenna design with material database integration,
frequency band definitions, and automated manufacturing file generation.
Supports professional RF design workflows with validation and optimization.
"""

import math
from math import cos, sin, sqrt, pi
from scipy import integrate
import json
from gerber_writer import DataLayer, Path, set_generation_software

# Physical constants and design parameters
light_velocity = 299792458  # Speed of light in m/s
impedance = 50              # Standard impedance for RF systems


class Result:
    """Data structure for antenna design results
    
    Stores all calculated parameters for easy access and export.
    Used by design_result() function for structured output.
    """
    def __init__(self):
        self.frequency = None
        self.patch_width = None
        self.patch_length = None
        self.feeder_width = None
        self.feeder_length = None
        self.inset_gap_width = None
        self.inset_length = None
        self.ground_length = None
        self.ground_width = None
        self.input_edge_impedance = None


def design_string(resonant_frequency, dielectric_constant, thickness):
    """Generate JSON string of antenna design parameters
    
    Convenience function for API integration and data export.
    Returns all design parameters as formatted JSON string.
    """
    return json.dumps(design_result(resonant_frequency, dielectric_constant, thickness).__dict__, indent=4)


def design_result(resonant_frequency, dielectric_constant, thickness):
    """Calculate antenna design and return structured result object
    
    Primary function for getting design parameters as Result object.
    Useful for programmatic access to individual parameters.
    """
    return design(resonant_frequency, dielectric_constant, thickness).get_result()


def design(resonant_frequency, dielectric_constant, thickness):
    """Calculate patch antenna dimensions from basic parameters
    
    Core design function using transmission line model.
    Returns DesignPatch object with all calculated parameters.
    
    Args:
        resonant_frequency: Operating frequency in Hz
        dielectric_constant: Substrate relative permittivity
        thickness: Substrate thickness in meters
    """
    return DesignPatch(resonant_frequency, dielectric_constant, thickness)


def design_with_material(frequency, material_name, thickness_mm=None):
    """Design antenna using material database"""
    from .materials import get_material, list_materials
    
    material = get_material(material_name)
    if not material:
        raise ValueError(f"Unknown material: {material_name}. Available: {list_materials()}")
    
    # Use provided thickness or first available option
    if thickness_mm is None:
        thickness_mm = material.thickness_options[0]
    elif thickness_mm not in material.thickness_options:
        print(f"Warning: {thickness_mm}mm not standard for {material_name}")
    
    thickness_m = thickness_mm / 1000  # Convert to meters
    design = DesignPatch(frequency, material.dielectric_constant, thickness_m)
    
    # Add material info to design
    design.material = material
    design.thickness_mm = thickness_mm
    
    return design


def design_for_band(band_name, material_name, thickness_mm=None):
    """Design antenna for specific frequency band"""
    from .frequency_bands import get_frequency, list_bands
    
    frequency = get_frequency(band_name)
    if not frequency:
        raise ValueError(f"Unknown band: {band_name}. Available: {list_bands()}")
    
    return design_with_material(frequency, material_name, thickness_mm)


def quick_design(band_name, material_name='FR4', thickness_mm=1.6):
    """Quick antenna design with common defaults"""
    from .validation import validate_design
    
    design = design_for_band(band_name, material_name, thickness_mm)
    warnings = validate_design(design)
    
    if warnings:
        print("Design Warnings:")
        for warning in warnings:
            print(f"  • {warning}")
    
    return design


class DesignPatch:
    """All parameter calculations"""
    freq = None
    er = None
    h = None
    patch_length = None
    patch_lengthl_eff = None
    patch_width = None
    feeder_length = None
    feeder_width = None
    inset_gap = None
    e_eff = None
    delta_l = None
    wavelength = None
    electrical_length = None
    ground_length = None
    ground_width = None
    inset_length = None
    input_impedance = None

    def __init__(self, freq, er, h):
        """
        Designs the patch parameters
        Parameters:
            freq (float): Resonant frequency in Hz.
            er (float): Dielectric constant of the cavity material.
            h (float): Thickness of the cavity in m.
        """
        if not 10 ** 6 <= freq <= 100 * 10 ** 9:
            raise ValueError("Frequency value should be in between 1MHz to 100 GHz")

        if not 0 < er <= 10**5:
            raise ValueError("Dielectric constant value should be in greater than 0 and smaller or equals 100,000")

        if not 0 < h <= 1:
            raise ValueError("Thickness value should be in greater than 0 and smaller or equals 1 meter")

        self.freq = freq
        self.er = er
        self.h = h
        self.set_wavelength()
        self.set_length_width_e_eff()
        self.set_feeder_width_length()

    def set_wavelength(self):
        self.wavelength = light_velocity / self.freq

    def set_length_width_e_eff(self):
        self.patch_width = (light_velocity / (2 * self.freq)) * sqrt(2 / (self.er + 1))
        temp = 1 + 12*(self.h / self.patch_width)
        self.e_eff = ((self.er + 1) / 2) + ((self.er - 1) / 2) * temp ** -0.5
        f1 = (self.e_eff + 0.3) * (self.patch_width / self.h + 0.264)
        f2 = (self.e_eff - 0.258) * (self.patch_width / self.h + 0.8)
        self.delta_l = self.h * 0.412 * (f1 / f2)
        self.patch_lengthl_eff = (self.wavelength / sqrt(self.e_eff)) / 2
        self.patch_length = self.patch_lengthl_eff - 2 * self.delta_l

    def set_feeder_width_length(self):
        self.feeder_length = (light_velocity / (4 * self.freq)) * (sqrt(1 / self.e_eff))
        self.feeder_width = self.patch_width / 5
        self.inset_gap = self.patch_width / 5
        self.set_input_impedance()
        self.inset_length = (self.patch_length / pi) * (math.acos(sqrt(impedance / self.input_impedance)))
        self.ground_length = self.patch_length + self.feeder_length + self.get_fringing_l()
        self.ground_width = self.patch_width + self.feeder_width + self.get_fringing_l()

    def get_result(self):
        result = Result()
        result.frequency = self.freq
        result.patch_width = self.patch_width
        result.patch_length = self.patch_length
        result.feeder_width = self.feeder_width
        result.feeder_length = self.feeder_length
        result.inset_gap_width = self.inset_gap
        result.inset_length = self.inset_length
        result.ground_length = self.ground_length
        result.ground_width = self.ground_width
        result.edge_impedance = self.input_impedance
        return result

    def get_fringing_l(self):
        return 6 * self.h

    def get_k(self):
        k0 = (2*pi)/self.wavelength
        return k0

    def S_i(self, a):
        temp = integrate.quad(lambda x: sin(x)/x, 0, a)
        return temp[0]

    def getG1(self):
        k0 = self.get_k()
        X = k0 * self.patch_width
        I1 = -2 + cos(X) + X * self.S_i(X) + sin(X)/X
        G1 = I1 / (120 * pi**2)
        return G1

    def J0(self, s):
        temp = integrate.quad(lambda x: cos(s*sin(x)), 0, pi)
        return (1/pi) * temp[0]

    def getG12(self):
        k0 = self.get_k()
        temp = integrate.quad(lambda x: (((sin(k0 * self.patch_width * cos(x) / 2) / cos(x)) ** 2) * self.J0(k0 * self.patch_length * sin(x)) * sin(x) ** 3), 0, pi)
        G12 = (1/(120*pi**2))*temp[0]
        return G12

    def set_input_impedance(self):
        G1, G12 = self.getG1(), self.getG12()
        self.input_impedance = 1 / (2 * (G1 + G12))


def m_to_mm(val):
    return val * 10**3


class FeedType:
    INSET = 'inset'
    NORMAL = 'normal'

    @staticmethod
    def check(_type: str):
        _valid_types = [FeedType.INSET, FeedType.NORMAL]
        if _type not in _valid_types:
            raise ValueError('Type should be : {}'.format(", ".join(_valid_types)))


class PatchGerberWriter:

    def __init__(self, pa_design: DesignPatch):
        self.pl = m_to_mm(pa_design.patch_length)
        self.pw = m_to_mm(pa_design.patch_width)
        self.fl = m_to_mm(pa_design.feeder_length)
        self.fw = m_to_mm(pa_design.feeder_width)
        self.frl = m_to_mm(pa_design.get_fringing_l())
        self.il = m_to_mm(pa_design.inset_length)
        self.ig = m_to_mm(pa_design.inset_gap)
        # Use static values to avoid circular import
        set_generation_software('Developed by: Leeds SpaceComms', 'pypi lib: patch_antenna', 'version: 0.1.0')

    def get_normal_feed_points(self):
        _st = (0, 0)
        pts = [
            (self.pl, 0),
            (self.pl, (self.pw / 2) - (self.fw / 2)),
            (self.pl + self.fl, (self.pw / 2) - (self.fw / 2)),
            (self.pl + self.fl, (self.pw / 2) - (self.fw / 2) + self.fw),
            (self.pl, (self.pw / 2) - (self.fw / 2) + self.fw),
            (self.pl, self.pw),
            (0, self.pw),
            _st
        ]
        return _st, pts

    def get_inset_feed_points(self):
        _st = (0, 0)
        pts = [
            (self.pl, 0),
            (self.pl, ((self.pw-self.fw)/2)-self.ig),
            (self.pl - self.il, ((self.pw-self.fw) / 2) - self.ig),
            (self.pl - self.il, ((self.pw-self.fw) / 2)),
            (self.pl - self.il + self.fl, ((self.pw-self.fw) / 2)),
            (self.pl - self.il + self.fl, ((self.pw + self.fw) / 2)),
            (self.pl - self.il, ((self.pw + self.fw) / 2)),
            (self.pl - self.il, ((self.pw + self.fw) / 2) + self.ig),
            (self.pl, ((self.pw + self.fw) / 2) + self.ig),
            (self.pl, self.pw),
            (0, self.pw),
            _st
        ]
        return _st, pts

    def get_border(self):
        _st = (0, 0)
        pts = [
            ((self.frl*2) + self.fl + self.pl, 0),
            ((self.frl*2) + self.fl + self.pl, (self.frl*2) + self.pw),
            (0, (self.frl*2) + self.pw),
            _st
        ]
        return _st, pts

    def write_gerber(self, path: str, _type: str = FeedType.NORMAL):
        __type_dict = {
            FeedType.NORMAL: self.get_normal_feed_points,
            FeedType.INSET: self.get_inset_feed_points
        }
        border_st, border_pts = self.get_border()
        (init_x, init_y), pts = __type_dict.get(_type)()

        profile_layer = DataLayer('Copper,L1,Top')
        _ant_prof = Path()
        _ant_prof.moveto((init_x + self.frl, init_y + self.frl))
        [_ant_prof.lineto((self.frl + x, self.frl + y)) for x, y in pts]
        profile_layer.add_region(_ant_prof, 'Other,Antenna')

        _bord_prof = Path()
        _bord_prof.moveto(border_st)
        [_bord_prof.lineto(_pts) for _pts in border_pts]
        profile_layer.add_traces_path(_bord_prof, 0.5, 'Profile')

        with open(path, 'w') as outfile:
            profile_layer.dump_gerber(outfile)


def write_gerber(resonant_frequency, dielectric_constant, thickness, file_name, feed_type):
    FeedType.check(feed_type)
    d = DesignPatch(resonant_frequency, dielectric_constant, thickness)
    write_gerber_design(d, file_name, feed_type)


def write_gerber_design(design_: DesignPatch, file_name, feed_type=FeedType.NORMAL):
    FeedType.check(feed_type)
    gw = PatchGerberWriter(design_)
    gw.write_gerber(file_name, feed_type)


"""Common substrate materials database"""

class SubstrateMaterial:
    def __init__(self, name, dielectric_constant, loss_tangent, thickness_options):
        self.name = name
        self.dielectric_constant = dielectric_constant
        self.loss_tangent = loss_tangent
        self.thickness_options = thickness_options  # in mm

# Common PCB materials
MATERIALS = {
    'FR4': SubstrateMaterial('FR4', 4.4, 0.02, [0.8, 1.6, 2.4, 3.2]),
    'ROGERS_RO4003C': SubstrateMaterial('Rogers RO4003C', 3.38, 0.0027, [0.508, 0.813, 1.524]),
    'ROGERS_RO4350B': SubstrateMaterial('Rogers RO4350B', 3.48, 0.0037, [0.508, 0.762, 1.524]),
    'PTFE': SubstrateMaterial('PTFE', 2.1, 0.0004, [0.5, 0.8, 1.6, 3.2]),
    'ALUMINA': SubstrateMaterial('Alumina', 9.8, 0.0001, [0.25, 0.635, 1.0])
}

def get_material(name):
    """Get material properties by name"""
    return MATERIALS.get(name.upper().replace(' ', '_'))

def list_materials():
    """List all available materials"""
    return list(MATERIALS.keys())

"""Common frequency bands for antenna design"""

FREQUENCY_BANDS = {
    'GPS_L1': 1.575e9,
    'GPS_L2': 1.227e9,
    'WIFI_2_4GHZ': 2.4e9,
    'WIFI_5GHZ': 5.0e9,
    'BLUETOOTH': 2.45e9,
    'ISM_433MHZ': 433e6,
    'ISM_868MHZ': 868e6,
    'ISM_915MHZ': 915e6,
    'LORA_EU': 868e6,
    'LORA_US': 915e6,
    'CELLULAR_GSM900': 900e6,
    'CELLULAR_GSM1800': 1.8e9,
    'CELLULAR_LTE_B1': 2.1e9,
    'CELLULAR_LTE_B3': 1.8e9,
    'CELLULAR_LTE_B7': 2.6e9,
    'ZIGBEE': 2.4e9,
    'UWB': 6.5e9
}

def get_frequency(band_name):
    """Get frequency for a specific band"""
    return FREQUENCY_BANDS.get(band_name.upper())

def list_bands():
    """List all available frequency bands"""
    return list(FREQUENCY_BANDS.keys())

def find_bands_in_range(min_freq, max_freq):
    """Find all bands within a frequency range"""
    return {k: v for k, v in FREQUENCY_BANDS.items() if min_freq <= v <= max_freq}

"""Design validation and optimization warnings"""

def validate_design(design):
    """Validate design parameters and provide warnings"""
    warnings = []
    
    # Check patch efficiency
    if design.patch_width / design.patch_length > 2.0:
        warnings.append("Warning: Patch width/length ratio > 2.0 may reduce efficiency")
    
    # Check substrate thickness
    wavelength_in_substrate = design.wavelength / (design.e_eff ** 0.5)
    if design.h > wavelength_in_substrate / 10:
        warnings.append("Warning: Substrate thickness > λ/10 may cause surface waves")
    
    # Check feeder width
    if design.feeder_width < 0.1e-3:  # 0.1mm
        warnings.append("Warning: Feeder width < 0.1mm may be difficult to manufacture")
    
    # Check impedance matching
    if abs(design.input_impedance - 50) > 10:
        warnings.append(f"Warning: Input impedance ({design.input_impedance:.1f}Ω) deviates significantly from 50Ω")
    
    return warnings
