import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from pathlib import Path
from ..core import setxTicks
from ..utils import load_spectrum, save_figure
from ...config import Config

def plot_ce(
    synthetic_files: List[str],
    observed_file: str,
    labels: List[str],
    starname: str = "",
    figsize=None,
    show: bool = True,
    save: bool = True,
    **kwargs
) -> Optional[Path]:
    """
    Plot Cerium (CeII) spectral features across six wavelength regions.
    
    Args:
        synthetic_files: List of synthetic spectrum files
        observed_file: Observed spectrum file
        labels: Legend labels for synthetic spectra
        starname: Star identifier for plot title
        show: Whether to display the plot
        save: Whether to save the plot
        **kwargs: Override default plot parameters
        
    Returns:
        Path to saved figure if save=True, else None
    """
    # Merge defaults with user parameters
    params = {
        "xlim1": Config.DEFAULT_XLIM["Ce"][0],
        "xlim2": Config.DEFAULT_XLIM["Ce"][1],
        "xlim3": Config.DEFAULT_XLIM["Ce"][2],
        "xlim4": Config.DEFAULT_XLIM["Ce"][3],
        "xlim5": Config.DEFAULT_XLIM["Ce"][4],
        "xlim6": Config.DEFAULT_XLIM["Ce"][5],
        "ylim1": Config.DEFAULT_YLIM,
        "ylim2": Config.DEFAULT_YLIM,
        "ylim3": Config.DEFAULT_YLIM,
        "ylim4": Config.DEFAULT_YLIM,
        "ylim5": Config.DEFAULT_YLIM,
        "ylim6": Config.DEFAULT_YLIM,
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
        obs_data[obs_data['Wavelength'].between(*params["xlim3"])]['Flux'].median(),
        obs_data[obs_data['Wavelength'].between(*params["xlim4"])]['Flux'].median(),
        obs_data[obs_data['Wavelength'].between(*params["xlim5"])]['Flux'].median(),
        obs_data[obs_data['Wavelength'].between(*params["xlim6"])]['Flux'].median()
    ]

    # Create figure
    figsize = figsize or Config.DEFAULT_FIGSIZE['Ce']
    fig, axes = plt.subplots(2, 3, figsize=Config.DEFAULT_FIGSIZE['Ce'], tight_layout=True)
    axes = axes.flatten()  # Flatten to 1D array for easy iteration
    fig.suptitle(f"Ce Lines - {starname}", y=1.02, fontsize=16)
    # Single legend for all panels

    
    # Adjust subplot spacing
    fig.subplots_adjust(top=0.85)  # Make room for legend
    # Plot each region
    for i, (ax, xlim, ylim) in enumerate(zip(
        axes,
        [params["xlim1"], params["xlim2"], params["xlim3"], 
         params["xlim4"], params["xlim5"], params["xlim6"]],
        [params["ylim1"], params["ylim2"], params["ylim3"],
         params["ylim4"], params["ylim5"], params["ylim6"]]
    ), 1):
        ax.plot(
            obs_data["Wavelength"] + params[f"xoffset{i}"],
            (obs_data["Flux"]/norm[i-1])/params[f"ncorr{i}"] + params[f"yoffset{i}"], '--',                linewidth = 0.7,
            color=Config.LINE_COLORS["obs"],
            label="Observed"
        )

        # Plot synthetic spectra
        for j, (data, label) in enumerate(zip(syn_data, labels)):
            ax.plot(
                data["Wavelength"], 
                data["Flux"], 
                label=label if i == 1 else ""  # Label only once
            )


        # Add CeII line markers
        ce_lines = Config.LINE_MARKERS["Ce"]["CeII"]
        if i <= len(ce_lines):  # Match regions to lines
            line_wavelength = ce_lines[i-1]
            ax.axvline(
                x=line_wavelength,
                ymin=0.10, ymax=0.25,
                color='darkred',
                linestyle="-",
                alpha=0.8,
                linewidth=2
            )
            # Add wavelength label
            ax.text(
                x=0.01,
                y=0.01,
                s=f"CeII - {line_wavelength}",
                ha='left',
                va='bottom',
                fontsize=14,
                transform=ax.transAxes
            )

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        setxTicks(ax, N=4)  # Fewer ticks for smaller panels
        ax.grid(True, alpha=0.3)
        
    # Add subplot labels (A, B, C, ...)
        ax.text(0.02, 0.98, f"({chr(64+i)})", transform=ax.transAxes, 
                fontsize=12, fontweight='bold', va='top')

    # Single legend for all subplots
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.0),
        ncol=len(labels) + 1,  # +1 for observed
        frameon=True,
        fancybox=True,
        shadow=True,
        fontsize=14
    )
    # Add x-labels to bottom row only
    for ax in axes[3:]:
        ax.set_xlabel("Wavelength (Å)")

    # Add y-label to left column only  
    for ax in axes[::3]:
        ax.set_ylabel("Normalized Flux")

    if save:
        saved_path = save_figure(fig, starname, "ce")
    if show:
        plt.show()
    plt.close()

    return saved_path if save else None