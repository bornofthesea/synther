import matplotlib.pyplot as plt
from typing import List, Optional
from pathlib import Path
from ..core import setxTicks
from ..utils import load_spectrum, save_figure
from ...config import Config

def plot_potassium(
    synthetic_files: List[str],
    observed_file: str,
    labels: List[str],
    starname: str = "",
    figsize=None,
    show: bool = True,
    save: bool = True,
    **kwargs
) -> Optional[Path]:
    """Plot potassium spectral features."""
    params = {
        "xlim1": Config.DEFAULT_XLIM["K"][0],
        "ylim1": Config.DEFAULT_YLIM,
        **Config.DEFAULT_OFFSETS,
        **kwargs
    }

    # Data loading
    obs_data = load_spectrum(observed_file, is_observed=True)
    syn_data = [load_spectrum(f) for f in synthetic_files]
    norm = obs_data[obs_data['Wavelength'].between(*params["xlim1"])]['Flux'].median()

    # Single panel plot
    figsize = figsize or Config.DEFAULT_FIGSIZE['K']
    fig, ax = plt.subplots(figsize=figsize, tight_layout=True)
    ax.set_title(f"Potassium Features - {starname}", pad=20)  # Add padding


    ax.plot(
        obs_data["Wavelength"] + params["xoffset1"],
        (obs_data["Flux"]/norm)/params["ncorr1"] + params["yoffset1"],
        color=Config.LINE_COLORS["obs"],
        label="Observed"
    )
    
    for data, label in zip(syn_data, labels):
        ax.plot(data["Wavelength"], data["Flux"], label=label)
        
    for line in Config.LINE_MARKERS["K"]["KI"]:
        ax.axvline(x=line, ymin=0.95, ymax=1.0, 
                  color="orange", linestyle="--", alpha=0.7)
        
    ax.set_xlim(*params["xlim1"])
    ax.set_ylim(*params["ylim1"])
    setxTicks(ax)
    ax.grid(True, alpha=0.3)
    ax.legend(
        loc='upper center',          # Center above plot
        bbox_to_anchor=(0.5, 1.15), # (horizontal, vertical) position
        ncol=3,                     # Number of columns
        frameon=False,              # Clean look
        fontsize=10
    )
    ax.set_xlabel("Wavelength (Å)")

    if save:
        saved_path = save_figure(fig, starname, "k")
    if show:
        plt.show()
    plt.close()

    return saved_path if save else None