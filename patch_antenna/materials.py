"""
PCB Material Database for Patch Antenna Design

Added by Al-Musbahi for Leeds SpaceComms
(Enhancement to original library by Bhanuchander Udhayakumar)

Comprehensive database of common PCB substrates with electrical properties
and standard thickness options. Enables material-based design optimization
for professional RF applications.
"""

class SubstrateMaterial:
    """Data structure for PCB substrate material properties
    
    Stores electrical and physical characteristics needed for antenna design.
    Includes standard thickness options for each material type.
    """
    def __init__(self, name, dielectric_constant, loss_tangent, thickness_options):
        self.name = name
        self.dielectric_constant = dielectric_constant
        self.loss_tangent = loss_tangent
        self.thickness_options = thickness_options  # Available thicknesses in mm

# Professional PCB materials for RF applications
MATERIALS = {
    'FR4': SubstrateMaterial('FR4', 4.4, 0.02, [0.8, 1.6, 2.4, 3.2]),
    'ROGERS_RO4003C': SubstrateMaterial('Rogers RO4003C', 3.38, 0.0027, [0.508, 0.813, 1.524]),
    'ROGERS_RO4350B': SubstrateMaterial('Rogers RO4350B', 3.48, 0.0037, [0.508, 0.762, 1.524]),
    'PTFE': SubstrateMaterial('PTFE', 2.1, 0.0004, [0.5, 0.8, 1.6, 3.2]),
    'ALUMINA': SubstrateMaterial('Alumina', 9.8, 0.0001, [0.25, 0.635, 1.0])
}

def get_material(name):
    """Retrieve material properties by name
    
    Case-insensitive lookup with space-to-underscore conversion.
    Returns SubstrateMaterial object or None if not found.
    """
    return MATERIALS.get(name.upper().replace(' ', '_'))

def list_materials():
    """Get list of available material names
    
    Returns list of all materials in the database.
    Use with get_material() to access properties.
    """
    return list(MATERIALS.keys())
