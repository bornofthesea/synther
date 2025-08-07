import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from pathlib import Path
from ..core import setxTicks
from ..utils import load_spectrum, save_figure
from ...config import Config

def plot_nir(
    synthetic_files: List[str],
    observed_file: str,
    labels: List[str],
    starname: str = "",
    figsize=None,
    show: bool = True,
    save: bool = True,
    **kwargs
) -> Optional[Path]:
    """Plot CNO molecular features across three wavelength regions."""
    # Merge defaults with user parameters
    params = {
        "xlim1": Config.DEFAULT_XLIM["nir"][0],
        "xlim2": Config.DEFAULT_XLIM["nir"][1],
        "xlim3": Config.DEFAULT_XLIM["nir"][2],
        "ylim1": Config.DEFAULT_YLIM,
        "ylim2": Config.DEFAULT_YLIM,
        "ylim3": Config.DEFAULT_YLIM,
        **Config.DEFAULT_OFFSETS,
        **kwargs
    }

    # Load data
    obs_data = load_spectrum(observed_file, is_observed=True)
    syn_data = [load_spectrum(f) for f in synthetic_files]

    # Calculate normalization for each region
    norm = [
        obs_data[obs_data['Wavelength'].between(*params["xlim1"])]['Flux'].median(),
        obs_data[obs_data['Wavelength'].between(*params["xlim2"])]['Flux'].median(),
        obs_data[obs_data['Wavelength'].between(*params["xlim3"])]['Flux'].median()
    ]

    # Create figure
    figsize = figsize or Config.DEFAULT_FIGSIZE['all']
    fig, axes = plt.subplots(3, figsize=figsize, tight_layout=True)
    fig.suptitle(f"NIR Spectra - {starname}", y=1.05)
    # Single legend for all panels

    
    # Adjust subplot spacing
    fig.subplots_adjust(top=0.85)  # Make room for legend
    # Plot each region
    for i, (ax, xlim, ylim) in enumerate(zip(
        axes,
        [params["xlim1"], params["xlim2"], params["xlim3"]],
        [params["ylim1"], params["ylim2"], params["ylim3"]]
    ), 1):
        ax.plot(
            obs_data["Wavelength"] + params[f"xoffset{i}"],
            (obs_data["Flux"]/norm[i-1])/params[f"ncorr{i}"] + params[f"yoffset{i}"],
            color=Config.LINE_COLORS["obs"],
            label="Observed"
        )

        # Plot synthetic spectra
        for data, label in zip(syn_data, labels):
            ax.plot(data["Wavelength"], data["Flux"], label=label)

        # Add molecular markers
        

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        setxTicks(ax)
        ax.grid(True, alpha=0.3)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.02),  # Right below title
        ncol=len(labels),             # Horizontal layout
        frameon=False,
        fontsize=9
    )
    #axes[0].legend(loc="upper right")
    axes[-1].set_xlabel("Wavelength (Å)")

    if save:
        saved_path = save_figure(fig, starname, "all")
    if show:
        plt.show()
    plt.close()

    return saved_path if save else None