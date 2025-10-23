"""
stellar_analysis - A package for stellar spectral analysis
"""

# Explicit imports for better IDE support
from .config import Config
from .plotting import plot_phosphorus, plot_potassium, plot_sulfur, plot_cno, plot_nir, plot_ce

__version__ = "0.1.0"
__author__ = "Morgan Camargo <cmorgan@usp.br>"



__all__ = [
    'Config',
    'plot_phosphorus',
    'plot_potassium',
    'plot_sulfur',
    'plot_cno',
    'plot_nir',
    'plot_ce'
]

# Explicitly expose functions at package level
plot_phosphorus = plot_phosphorus
plot_potassium = plot_potassium
plot_sulfur = plot_sulfur
plot_cno = plot_cno
plot_nir = plot_nir
plot_ce = plot_ce