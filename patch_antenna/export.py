"""
Enhanced export functionality for patch antenna designs.

This module provides comprehensive export capabilities for antenna designs including
design summaries, manufacturing specifications, and professional documentation.
Essential for design documentation and fabrication workflows.

Added by Al-Musbahi - Leeds SpaceComms
(Enhancement to original library by Bhanuchander Udhayakumar)
"""

def export_design_summary(design, filename):
    """
    Export a comprehensive design summary to text file.
    
    Creates a detailed summary document containing all key design parameters,
    dimensions, and electrical properties. Useful for design reviews and
    documentation purposes.
    
    Args:
        design: Antenna design object containing all parameters
        filename: Output filename for the summary document
    
    Returns:
        None (writes summary to specified file)
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Patch Antenna Design Summary\n")
        f.write("=" * 30 + "\n\n")
        
        f.write(f"Operating Frequency: {design.freq/1e9:.3f} GHz\n")
        f.write(f"Substrate Er: {design.er}\n")
        f.write(f"Substrate Thickness: {design.h*1000:.2f} mm\n\n")
        
        f.write("Patch Dimensions:\n")
        f.write(f"  Width: {design.patch_width*1000:.2f} mm\n")
        f.write(f"  Length: {design.patch_length*1000:.2f} mm\n\n")
        
        f.write("Feed Dimensions:\n")
        f.write(f"  Width: {design.feeder_width*1000:.2f} mm\n")
        f.write(f"  Length: {design.feeder_length*1000:.2f} mm\n")
        f.write(f"  Inset Length: {design.inset_length*1000:.2f} mm\n\n")
        
        f.write("Electrical Properties:\n")
        f.write(f"  Input Impedance: {design.input_impedance:.1f} Ohm\n")
        f.write(f"  Effective Dielectric: {design.e_eff:.2f}\n")

def export_manufacturing_notes(design, filename):
    """
    Export manufacturing guidelines and specifications.
    
    Creates a detailed manufacturing guide with PCB specifications, critical
    dimensions, and tolerances. Essential for ensuring proper fabrication
    and performance of the antenna design.
    
    Args:
        design: Antenna design object containing all parameters
        filename: Output filename for the manufacturing guide
    
    Returns:
        None (writes manufacturing notes to specified file)
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Manufacturing Guidelines\n")
        f.write("=" * 25 + "\n\n")
        
        f.write("PCB Specifications:\n")
        f.write(f"  Substrate: Er = {design.er}\n")
        f.write(f"  Thickness: {design.h*1000:.2f} mm\n")
        f.write(f"  Copper: 1 oz (35 micrometers)\n\n")
        
        f.write("Critical Dimensions:\n")
        f.write(f"  Patch: {design.patch_width*1000:.2f} x {design.patch_length*1000:.2f} mm\n")
        f.write(f"  Feed line: {design.feeder_width*1000:.2f} mm wide\n")
        f.write(f"  Inset: {design.inset_length*1000:.2f} mm deep\n\n")
        
        f.write("Tolerances:\n")
        f.write("  Patch dimensions: +/-0.05 mm\n")
        f.write("  Feed line width: +/-0.02 mm\n")
        f.write("  Inset depth: +/-0.02 mm\n")
