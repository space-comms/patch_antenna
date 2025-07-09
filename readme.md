# Patch Antenna Designer
Advanced rectangular patch antenna design with enhanced material database and automated Gerber generation.

[![PyPI version](https://badge.fury.io/py/patch-antenna-designer.svg)](https://badge.fury.io/py/patch-antenna-designer)
[![Downloads](https://pepy.tech/badge/patch-antenna-designer)](https://pepy.tech/project/patch-antenna-designer)
[![Python](https://img.shields.io/pypi/pyversions/patch-antenna-designer.svg)](https://pypi.org/project/patch-antenna-designer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fspace-comms%2Fpatch_antenna&label=Visitors&countColor=%23263759)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Fspace-comms%2Fpatch_antenna)

---

## Project Overview

A **student-friendly** patch antenna design library created by students for students, hobbyists, and RF enthusiasts. This enhanced version of the original library provides comprehensive tools for designing rectangular patch antennas with an intuitive interface and educational focus.

**Perfect for**: Students learning RF design, hobbyists building antennas, makers exploring wireless projects, and anyone interested in understanding patch antenna fundamentals.

### Key Features

- **Student-Friendly Interface**: Simple functions like `quick_design()` for rapid prototyping
- **Educational Material Database**: Common PCB substrates with clear explanations
- **Comprehensive Frequency Bands**: Pre-defined bands for WiFi, Bluetooth, GSM, and more
- **Automated Design Validation**: Helpful warnings and optimization suggestions
- **Professional Documentation**: Clear examples and educational comments
- **Direct PCB Export**: Generate Gerber files for fabrication
- **Design Comparison Tools**: Compare materials and optimize designs
- **Manufacturing Support**: Export specifications for PCB fabrication

### Technical Capabilities

- **Frequency Range**: 1 MHz to 100 GHz (perfect for student projects)
- **Material Support**: FR4, Rogers substrates, PTFE, Alumina with educational notes
- **Feed Types**: Normal edge feed and inset feed with impedance matching
- **Export Formats**: Design summaries, manufacturing specs, Gerber files
- **Validation**: Efficiency analysis, manufacturability checks, student-friendly warnings

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

# Quick design for student WiFi projects
design = pa.quick_design('WIFI_2_4GHZ', 'FR4', 1.6)
print(f"Patch: {design.patch_width*1000:.1f} x {design.patch_length*1000:.1f} mm")

# Generate files for PCB fabrication
pa.export_design_summary(design, 'my_antenna_design.txt')
pa.write_gerber_design(design, 'my_antenna.gbr', 'inset')
```

### For Students & Hobbyists

```python
# Compare different materials for your project
materials = pa.find_best_material(2.4e9, 1.6, target_impedance=50)
print(f"Best material for your project: {materials[0][0]}")

# Design with specific material
design = pa.design_with_material(2.4e9, 'FR4', 1.6)

# Get helpful warnings and tips
warnings = pa.validate_design(design)
for warning in warnings:
    print(f"💡 Tip: {warning}")
```

## Documentation

Complete documentation and examples available in the [GitHub repository](https://github.com/space-comms/patch_antenna).

Educational tutorials and student guides coming soon!

## Student & Hobbyist Applications

- **University RF Labs**: Perfect for antenna design coursework
- **Maker Projects**: WiFi range extenders, IoT antennas, wireless sensors
- **Ham Radio**: Custom patch antennas for amateur radio projects  
- **Student Competitions**: Robotics competitions, satellite projects
- **DIY Electronics**: Home automation, wireless communication projects
- **Learning Platform**: Understanding antenna fundamentals and RF design

## Community & Support

This project is developed by **Space-Comms** student community and maintained by **Al-Musbahi**. 

- 🎓 **For Students**: Ask questions, share projects, learn together
- 🔧 **For Hobbyists**: Build cool antennas, experiment with designs
- 📚 **Educational Use**: Use in courses, workshops, and tutorials
- 🤝 **Contributions**: Students and hobbyists welcome to contribute!

## Authors

**Original Author:**  
**Bhanuchander Udhayakumar** ([@bhanuchander210](https://github.com/bhanuchander210))  
Original patch antenna design library implementation

**Enhanced by:**  
**Al-Musbahi** ([@al-musbahi](https://github.com/al-musbahi)) - Space-Comms Community  
Student-friendly enhancements, material database, validation, and educational features

**Community:**  
**Space-Comms** - Student community for space and wireless communication projects

---

*"By students, for students - making RF design accessible to everyone!"*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
