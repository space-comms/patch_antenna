"""
Design validation and optimization warnings for patch antennas.

This module provides comprehensive validation functions to check design parameters
and identify potential issues before fabrication. Essential for ensuring optimal
antenna performance and manufacturability.

Added by Al-Musbahi - Leeds SpaceComms
(Enhancement to original library by Bhanuchander Udhayakumar)
"""

def validate_design(design):
    """
    Validate design parameters and provide optimization warnings.
    
    Performs comprehensive checks on antenna design parameters including
    efficiency, manufacturability, and impedance matching. Provides actionable
    warnings to help optimize the design before fabrication.
    
    Args:
        design: Antenna design object containing all parameters
    
    Returns:
        List of warning strings describing potential issues
    """
    warnings = []
    
    # Check patch aspect ratio for optimal efficiency
    if design.patch_width / design.patch_length > 2.0:
        warnings.append("Warning: Patch width/length ratio > 2.0 may reduce efficiency")
    
    # Check substrate thickness relative to wavelength
    wavelength_in_substrate = design.wavelength / (design.e_eff ** 0.5)
    if design.h > wavelength_in_substrate / 10:
        warnings.append("Warning: Substrate thickness > λ/10 may cause surface waves")
    
    # Check manufacturability constraints
    if design.feeder_width < 0.1e-3:  # 0.1mm minimum feature size
        warnings.append("Warning: Feeder width < 0.1mm may be difficult to manufacture")
    
    # Check impedance matching quality
    if abs(design.input_impedance - 50) > 10:
        warnings.append(f"Warning: Input impedance ({design.input_impedance:.1f}Ohm) deviates significantly from 50Ohm")
    
    return warnings
