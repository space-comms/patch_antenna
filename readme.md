# Patch Antenna Design Library
Advanced rectangular patch antenna design with enhanced material database and automated Gerber generation.
---

## Project Overview

This library provides comprehensive tools for designing rectangular patch antennas with enhanced material database support, frequency band definitions, and automated manufacturing file generation. Built for aerospace and RF engineers who need professional-grade antenna design capabilities with minimal complexity.

### Key Features

- Advanced material database with loss tangent and thickness specifications
- Comprehensive frequency band definitions for common applications
- Automated design validation and optimization warnings
- Professional documentation export and manufacturing notes
- Direct Gerber file generation for PCB fabrication
- Design comparison tools for material and frequency analysis
- Impedance matching optimization algorithms

### Technical Capabilities

- Frequency range: 1 MHz to 100 GHz
- Material support: FR4, Rogers RO4003C/RO4350B, PTFE, Alumina
- Feed types: Normal edge feed and inset feed for impedance matching
- Export formats: Design summaries, manufacturing specifications, Gerber files
- Validation: Efficiency analysis, manufacturability checks, impedance matching

## Quick Start

### Installation

```bash
pip install patch-antenna-designer
```

Or install with development dependencies:
```bash
pip install patch-antenna-designer[dev]
```

### Basic Usage

```python
import patch_antenna as pa

# Quick design for WiFi applications
design = pa.quick_design('WIFI_2_4GHZ', 'FR4', 1.6)
print(f"Patch: {design.patch_width*1000:.1f} x {design.patch_length*1000:.1f} mm")

# Generate manufacturing files
pa.export_design_summary(design, 'antenna_summary.txt')
pa.write_gerber_design(design, 'antenna.gbr', 'inset')
```

### Material Optimization

```python
# Find optimal material for 50Ω matching
best_materials = pa.find_best_material(2.4e9, 1.6, target_impedance=50)
material_name = best_materials[0][0]

# Create optimized design
design = pa.design_with_material(2.4e9, material_name, 1.6)
```

## Documentation

Complete technical documentation and API reference available at: [patch-antenna.readthedocs.io](https://patch-antenna.readthedocs.io/)

## Applications

- Aerospace communication systems
- IoT and wireless sensor networks  
- Automotive radar and communication
- Medical device telemetry
- Military and defense applications
- Research and development platforms

## Authors

**Original Author:**  
**Bhanuchander Udhayakumar** ([@bhanuchander210](https://github.com/bhanuchander210))  
Original patch antenna design library implementation

**Enhanced by:**  
**Al-Musbahi** - Leeds SpaceComms  
Advanced features, material database, validation, and space communication enhancements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
