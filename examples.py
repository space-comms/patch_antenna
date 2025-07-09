"""
PATCH ANTENNA LIBRARY - STEP-BY-STEP EXAMPLES
=============================================

Example 1: Design a WiFi 2.4GHz Antenna
---------------------------------------
"""

import patch_antenna as pa

print("=== EXAMPLE 1: WiFi 2.4GHz Antenna ===")

# Step 1: Quick design with default FR4
wifi_design = pa.quick_design('WIFI_2_4GHZ', 'FR4', 1.6)

# Step 2: Check the dimensions
print(f"Patch: {wifi_design.patch_width*1000:.2f} x {wifi_design.patch_length*1000:.2f} mm")
print(f"Ground plane: {wifi_design.ground_width*1000:.2f} x {wifi_design.ground_length*1000:.2f} mm")
print(f"Input impedance: {wifi_design.input_impedance:.1f} Ω")

# Step 3: Generate files
pa.export_design_summary(wifi_design, 'wifi_antenna_summary.txt')
pa.write_gerber_design(wifi_design, 'wifi_antenna.gbr', 'inset')

print("Files generated: wifi_antenna_summary.txt, wifi_antenna.gbr\n")

"""
Example 2: Compare Materials for GPS Antenna
-------------------------------------------
"""

print("=== EXAMPLE 2: GPS L1 Antenna Material Comparison ===")

# Step 1: Get GPS L1 frequency
gps_freq = pa.get_frequency('GPS_L1')
print(f"GPS L1 frequency: {gps_freq/1e9:.3f} GHz")

# Step 2: Compare different materials
materials = ['FR4', 'ROGERS_RO4003C', 'PTFE']
gps_designs = []

for material in materials:
    try:
        design = pa.design_with_material(gps_freq, material, 1.0)
        gps_designs.append(design)
        print(f"{material}: {design.patch_width*1000:.2f} x {design.patch_length*1000:.2f} mm, Z={design.input_impedance:.1f}Ω")
    except Exception as e:
        print(f"{material}: Error - {e}")

# Step 3: Compare designs
if len(gps_designs) >= 2:
    print("\nDesign Comparison:")
    pa.compare_designs(gps_designs, materials)

print()

"""
Example 3: Find Best Material for 50Ω Matching
---------------------------------------------
"""

print("=== EXAMPLE 3: Find Best Material for 50Ω Matching ===")

# Step 1: Define requirements
target_freq = 2.4e9  # 2.4 GHz
target_thickness = 1.6  # 1.6 mm
target_impedance = 50  # 50 Ω

# Step 2: Find best materials
best_materials = pa.find_best_material(target_freq, target_thickness, target_impedance)

print("Best materials for 50Ω matching:")
for i, (name, design, error) in enumerate(best_materials[:3]):
    print(f"{i+1}. {name}: {design.input_impedance:.1f}Ω (error: {error:.1f}Ω)")

# Step 3: Use the best material
if best_materials:
    best_name = best_materials[0][0]
    best_design = pa.design_with_material(target_freq, best_name, target_thickness)
    
    print(f"\nUsing {best_name}:")
    print(f"Dimensions: {best_design.patch_width*1000:.2f} x {best_design.patch_length*1000:.2f} mm")
    
    # Generate complete documentation
    pa.export_design_summary(best_design, f'best_material_{best_name.lower()}_summary.txt')
    pa.export_manufacturing_notes(best_design, f'best_material_{best_name.lower()}_manufacturing.txt')

print()

"""
Example 4: Design for Different Frequency Bands
----------------------------------------------
"""

print("=== EXAMPLE 4: Multi-band Design ===")

# Step 1: Define bands of interest
bands = ['ISM_915MHZ', 'WIFI_2_4GHZ', 'WIFI_5GHZ']

# Step 2: Design for each band
multiband_designs = []
for band in bands:
    design = pa.design_for_band(band, 'FR4', 1.6)
    multiband_designs.append(design)
    
    freq = pa.get_frequency(band)
    print(f"{band} ({freq/1e9:.3f} GHz): {design.patch_width*1000:.2f} x {design.patch_length*1000:.2f} mm")

# Step 3: Compare all designs
print("\nMulti-band Comparison:")
pa.compare_designs(multiband_designs, bands)

print()

"""
Example 5: Custom Design with Validation
---------------------------------------
"""

print("=== EXAMPLE 5: Custom Design with Validation ===")

# Step 1: Create custom design
custom_design = pa.design(5.8e9, 3.38, 0.8e-3)  # 5.8 GHz, Rogers-like, 0.8mm

# Step 2: Validate design
warnings = pa.validate_design(custom_design)
print(f"Design: {custom_design.patch_width*1000:.2f} x {custom_design.patch_length*1000:.2f} mm")
print(f"Impedance: {custom_design.input_impedance:.1f} Ω")

if warnings:
    print("Validation warnings:")
    for warning in warnings:
        print(f"  - {warning}")
else:
    print("No validation warnings!")

# Step 3: Export if design is good
if len(warnings) <= 1:  # Accept minor warnings
    pa.export_design_summary(custom_design, 'custom_design_summary.txt')
    pa.write_gerber_design(custom_design, 'custom_design.gbr', 'inset')
    print("Design exported successfully!")

print()

"""
Example 6: Complete Professional Workflow
----------------------------------------
"""

print("=== EXAMPLE 6: Complete Professional Workflow ===")

# Step 1: Requirements
print("Requirements: 2.4 GHz WiFi antenna for IoT device")
print("Constraints: Thin PCB (0.8mm), 50Ω matching preferred")

# Step 2: Find optimal solution
target_freq = 2.4e9
target_thickness = 0.8

# Find best material for thin PCB
best_materials = pa.find_best_material(target_freq, target_thickness, 50)
if best_materials:
    chosen_material = best_materials[0][0]
    print(f"Chosen material: {chosen_material}")
    
    # Create final design
    final_design = pa.design_with_material(target_freq, chosen_material, target_thickness)
    
    # Validate
    warnings = pa.validate_design(final_design)
    
    # Generate complete documentation package
    pa.export_design_summary(final_design, 'iot_antenna_summary.txt')
    pa.export_manufacturing_notes(final_design, 'iot_antenna_manufacturing.txt')
    pa.write_gerber_design(final_design, 'iot_antenna_normal.gbr', 'normal')
    pa.write_gerber_design(final_design, 'iot_antenna_inset.gbr', 'inset')
    
    print("Complete design package generated:")
    print("  - iot_antenna_summary.txt")
    print("  - iot_antenna_manufacturing.txt")
    print("  - iot_antenna_normal.gbr")
    print("  - iot_antenna_inset.gbr")
    
    if warnings:
        print("Design notes:")
        for warning in warnings:
            print(f"  - {warning}")

print("\n=== ALL EXAMPLES COMPLETE ===")
print("Check the generated files to see the detailed outputs!")
