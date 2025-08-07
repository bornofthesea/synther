from pathlib import Path
import pandas as pd
from ..config import Config

def load_spectrum(filename: str, is_observed: bool = False) -> pd.DataFrame:
    """Load spectrum file from appropriate directory."""
    path = Config.APOG_DIR / filename if is_observed else Config.SYNT_DIR / filename
    return pd.read_csv(path, sep='\s+', header=None, 
                      names=["Wavelength", "Flux"], comment="#")

def save_figure(fig, starname: str, element: str) -> Path:
    """Save figure to output directory with standardized naming."""
    Config.setup_directories()
    filename = Config.OUTPUT_DIR / f"{starname}_{element.lower()}.png"
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    return filename