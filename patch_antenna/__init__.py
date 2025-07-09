"""
Patch Antenna Design Library

Advanced rectangular patch antenna design with enhanced material database 
and automated Gerber generation. Provides comprehensive tools for designing 
professional-grade patch antennas with minimal complexity.

Originally developed by Bhanuchander Udhayakumar (github.com/bhanuchander210)
Enhanced by Al-Musbahi - Leeds SpaceComms
"""

__name__ = 'patch_antenna'
__version__ = '0.1.0'
__owner__ = 'Leeds SpaceComms'

from .designer import (
    design,
    design_result,
    design_string,
    design_with_material,
    design_for_band,
    quick_design,
    write_gerber,
    write_gerber_design,
    DesignPatch,
    FeedType,
    PatchGerberWriter,
    Result
)

from .materials import get_material, list_materials, MATERIALS
from .frequency_bands import get_frequency, list_bands, find_bands_in_range
from .validation import validate_design
from .comparison import compare_designs, find_best_material
from .export import export_design_summary, export_manufacturing_notes

__all__ = [
    'design',
    'design_result', 
    'design_string',
    'design_with_material',
    'design_for_band',
    'quick_design',
    'write_gerber',
    'write_gerber_design',
    'DesignPatch',
    'FeedType',
    'PatchGerberWriter',
    'Result',
    'get_material',
    'list_materials',
    'get_frequency',
    'list_bands',
    'validate_design',
    'compare_designs',
    'find_best_material',
    'export_design_summary',
    'export_manufacturing_notes'
]
