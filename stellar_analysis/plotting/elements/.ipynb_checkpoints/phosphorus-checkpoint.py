import matplotlib.pyplot as plt
from typing import List, Optional
from pathlib import Path
from ..core import setxTicks
from ..utils import load_spectrum, save_figure
from ...config import Config

def plot_phosphorus(
    synthetic_files: List[str],
    observed_file: str,
    labels: List[str],
    starname: str = "",
    figsize = None,
    show: bool = True,
    save: bool = True,
    **kwargs
) -> Optional[Path]:
    """Plot phosphorus spectral features."""
    params = {
        "xlim1": Config.DEFAULT_XLIM["P"][0],
        "xlim2": Config.DEFAULT_XLIM["P"][1],
        "ylim1": Config.DEFAULT_YLIM,
        "ylim2": Config.DEFAULT_YLIM,
        **Config.DEFAULT_OFFSETS,
        **kwargs
    }

    # Data loading
    obs_data = load_spectrum(observed_file, is_observed=True)
    syn_data = [load_spectrum(f) for f in synthetic_files]
    norm = [
        obs_data[obs_data['Wavelength'].between(*params["xlim1"])]['Flux'].median(),
        obs_data[obs_data['Wavelength'].between(*params["xlim2"])]['Flux'].median()
    ]

    # Create figure
    figsize = figsize or Config.DEFAULT_FIGSIZE['P']
    fig, axes = plt.subplots(2, figsize=figsize, tight_layout=True)
    fig.suptitle(f"Phosphorus Features - {starname}", y=1.02)
    # Get handles from either subplot


    # Plot both regions
    for i, (ax, xlim, ylim) in enumerate(zip(
        axes,
        [params["xlim1"], params["xlim2"]],
        [params["ylim1"], params["ylim2"]]
    ), 1):
        ax.plot(
            obs_data["Wavelength"] + params[f"xoffset{i}"],
            (obs_data["Flux"]/norm[i-1])/params[f"ncorr{i}"] + params[f"yoffset{i}"],
            color=Config.LINE_COLORS["obs"],
            label="Observed"
        )
        
        for data, label in zip(syn_data, labels):
            ax.plot(data["Wavelength"], data["Flux"], label=label)
            
        for line in Config.LINE_MARKERS["P"]["PI"]:
            ax.axvline(x=line, ymin=0.95, ymax=1.0, 
                      color="purple", linestyle="--", alpha=0.7)
            
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        setxTicks(ax)
        ax.grid(True, alpha=0.3)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles, labels,
        loc='upper center',
        bbox_to_anchor=(0.5, 0.98),  # Between title and plots
        ncol=len(labels),
        frameon=True,
        fancybox=True,
        shadow=False,
        fontsize=9
    )
    
    fig.subplots_adjust(top=0.82)
    axes[-1].set_xlabel("Wavelength (Å)")

    if save:
        saved_path = save_figure(fig, starname, "p")
    if show:
        plt.show()
    plt.close()

    return saved_path if save else None