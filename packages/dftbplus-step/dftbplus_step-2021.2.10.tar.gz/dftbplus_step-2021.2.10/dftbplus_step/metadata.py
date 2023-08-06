"""This file contains metadata to help describe the results of DFTB+
calculations, etc.
"""
"""Properties that DFTB+ produces, depending on the type of calculation.
"""
properties = {
    "total_energy":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The total energy",
            "dimensionality": "scalar",
            "methods": [],
            "type": "float",
            "units": "hartree"
        },
    "fermi_level":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The Fermi level",
            "dimensionality": [2],
            "methods": [],
            "type": "float",
            "units": "hartree"
        },
    "number_of_electrons":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The number of electrons",
            "dimensionality": [2],
            "methods": [],
            "type": "float",
            "units": ""
        },
    "mermin_energy":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The Mermin energy",
            "dimensionality": "scalar",
            "methods": [],
            "type": "float",
            "units": "hartree"
        },
    "extrapolated0_energy":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The energy extrapolated to no smearing",
            "dimensionality": "scalar",
            "methods": [],
            "type": "float",
            "units": "hartree"
        },
    "forcerelated_energy":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The force-related energy",
            "dimensionality": "scalar",
            "methods": [],
            "type": "float",
            "units": "hartree"
        },
    "eigenvalues":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The eigenvalues",
            "dimensionality": ["norbitals"],
            "methods": [],
            "type": "float",
            "units": "hartree"
        },
    "filling":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The orbital occupancy",
            "dimensionality": ["norbitals"],
            "methods": [],
            "type": "float",
            "units": ""
        },
    "orbital_charges":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The orbital charges",
            "dimensionality": ["natoms", "natoms"],
            "methods": [],
            "type": "float",
            "units": ""
        },
    "gross_atomic_charges":
        {
            "calculation": [
                "energy",
                "optimization",
            ],
            "description": "The charges on the atoms",
            "dimensionality": ["natoms"],
            "methods": [],
            "type": "float",
            "units": ""
        },
    "forces":
        {
            "calculation": ["optimization"],
            "description": "The forces on the atoms",
            "dimensionality": [3, "natoms"],
            "methods": [],
            "type": "float",
            "units": "hartree/bohr"
        },
}
