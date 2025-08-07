from pathlib import Path
from typing import Dict, List, Tuple

class Config:
    # Directory paths
    BASE_DIR = Path.home() / "stellar_analysis"
    SYNT_DIR = Path("/home/morgan/Turbospectrum2019/COM-v19.1/syntspec/")
    APOG_DIR = Path("/home/morgan/PhD/Data/apogee/")
    OUTPUT_DIR = BASE_DIR / "plots"

    DEFAULT_FIGSIZE = {
        'P': (12, 6),     # Phosphorus (2 panels)
        'K': (10, 5),      # Potassium (1 panel)
        'S': (12, 6),      # Sulfur (2 panels)
        'CNO': (14, 12),    # CNO (3 panels)
        'nir': (14, 12)    # all (3 panels)
    }
    
    # Default plotting parameters
    DEFAULT_XLIM: Dict[str, List[Tuple[float, float]]] = {
        'P': [(15702, 15720), (16480, 16488)],
        'K': [(15160, 15170)],
        'S': [(15465, 15473), (15472, 15482)],
        'CNO': [(15520, 15555), (15555, 15575), (15575, 15590)],
        'nir': [(15100, 15600), (15600, 16600), (15500, 15600)]
    }
    
    DEFAULT_YLIM: Tuple[float, float] = (0.75, 1.05)
    
    # Add this new section for offsets
    DEFAULT_OFFSETS: Dict[str, float] = {
        'xoffset1': 0, 'yoffset1': 0, 'ncorr1': 1,
        'xoffset2': 0, 'yoffset2': 0, 'ncorr2': 1,
        'xoffset3': 0, 'yoffset3': 0, 'ncorr3': 1
    }
    
    # Line markers
    LINE_MARKERS: Dict[str, Dict[str, List[float]]] = {
        'P': {"PI": [15711.6, 16482.9]},
        'K': {"KI": [15163.067, 15168.376]},
        'S': {"SI": [15469.8036, 15475.604, 15478.469]},
        'CNO': {
            "CN": [15528.063, 15528.734, 15529.9, 15530.8, 15534.4, 15540.23, 15541.40, 15542.20, 15542.20, 15542.90, 15544.5, 15550.45, 15550.9, 15552.6, 15553.5, 15554.5, 15555.435, 15557.9, 15558.7, 155561.4, 15562.2, 15563.4, 15573.2, 15579.8, 15580.2, 15581.0],
            "OH": [15535.46, 15536.7, 15560.24, 15565.91, 15568.78],
            "CO": [15572.1, 15577.6, 15577.4, 15578.4, 155578.8, 155579.3, 15579.8, 15581.8, 15582.6, 15583.5, 15584.4, 15586.4, 15586.716, 155586.4]
        }
    }
    
    # Plot styling
    LINE_COLORS = {
        "obs": "red",
        "CN": "red",
        "OH": "green",
        "CO": "purple",
        "default": "blue"
    }

    @classmethod
    def setup_directories(cls):
        """Ensure all directories exist"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)