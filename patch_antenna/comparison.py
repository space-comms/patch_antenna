"""
Design comparison tools for patch antenna analysis.

This module provides functions to compare multiple antenna designs and find optimal 
materials for specific design constraints. Essential for design optimization and 
material selection workflows.

Added by Al-Musbahi - Leeds SpaceComms
(Enhancement to original library by Bhanuchander Udhayakumar)
"""

def compare_designs(designs, labels=None):
    """
    Compare multiple antenna designs in a formatted table.
    
    Displays key design parameters side-by-side for easy comparison including
    frequency, dimensions, impedance, and total area. Useful for evaluating
    different design options and trade-offs.
    
    Args:
        designs: List of antenna design objects to compare
        labels: Optional list of labels for each design (default: "Design 1", "Design 2", etc.)
    
    Returns:
        None (prints comparison table to console)
    """
    if labels is None:
        labels = [f"Design {i+1}" for i in range(len(designs))]
    
    print(f"{'Parameter':<20} " + " ".join(f"{label:<15}" for label in labels))
    print("-" * (20 + 16 * len(designs)))
    
    # Display comparison table with key parameters
    params = [
        ('Frequency (GHz)', lambda d: d.freq / 1e9),
        ('Patch Width (mm)', lambda d: d.patch_width * 1000),
        ('Patch Length (mm)', lambda d: d.patch_length * 1000),
        ('Feeder Width (mm)', lambda d: d.feeder_width * 1000),
        ('Feeder Length (mm)', lambda d: d.feeder_length * 1000),
        ('Input Impedance (Ohm)', lambda d: d.input_impedance),
        ('Total Area (mm²)', lambda d: (d.ground_width * d.ground_length) * 1e6)
    ]
    
    for param_name, getter in params:
        values = [getter(design) for design in designs]
        print(f"{param_name:<20} " + " ".join(f"{val:>14.2f}" for val in values))

def find_best_material(frequency, thickness_mm, target_impedance=50):
    """
    Find the best material for given design constraints.
    
    Evaluates all available materials to find the best match for impedance
    requirements. Designs are tested with each material and ranked by how
    closely they match the target impedance.
    
    Args:
        frequency: Operating frequency in Hz
        thickness_mm: Substrate thickness in millimeters
        target_impedance: Target input impedance in Ohms (default: 50)
    
    Returns:
        List of tuples: (material_name, design_object, impedance_error)
        sorted by impedance matching quality (best first)
    """
    from .materials import MATERIALS
    from .designer import design_with_material
    
    # Test each material that supports the required thickness
    results = []
    for name, material in MATERIALS.items():
        if thickness_mm in material.thickness_options:
            try:
                design = design_with_material(frequency, name, thickness_mm)
                impedance_error = abs(design.input_impedance - target_impedance)
                results.append((name, design, impedance_error))
            except:
                continue
    
    # Sort by impedance matching accuracy (lower error is better)
    results.sort(key=lambda x: x[2])
    return results
