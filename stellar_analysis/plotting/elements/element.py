import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from pathlib import Path
from ..core import setxTicks
from ..utils import load_spectrum, save_figure
from ...config import Config

def plot_spectra(
    element: str,
    synthetic_files: List[str],
    observed_file: str,
    labels: List[str],
    regions: Optional[List[List[float]]] = None,
    starname: str = "",
    nrows = None,
    figsize = None,
    show: bool = True,
    save: bool = True,
    **kwargs
) -> Optional[Path]:
    """
    Plot spectral features for any element across multiple wavelength regions.
    
    Args:
        element: Element name (e.g., 'Ce', 'Fe', 'Ba')
        synthetic_files: List of synthetic spectrum files
        observed_file: Observed spectrum file
        labels: Legend labels for synthetic spectra
        regions: List of [min, max] wavelength regions to plot. If None, uses defaults from Config
        nrows: Number of rows for subplots (auto-calculated if None)
        ncols: Number of columns for subplots (auto-calculated if None)
        starname: Star identifier for plot title
        show: Whether to display the plot
        save: Whether to save the plot
        **kwargs: Override default plot parameters
        
    Returns:
        Path to saved figure if save=True, else None
    """
    # Get default configuration for element
    default_xlims = Config.DEFAULT_XLIM.get(element, [])
    default_ylim = Config.DEFAULT_YLIM
    default_offsets = Config.DEFAULT_OFFSETS


    ###------### BUILDING THE GRID ###------###
    # Use provided regions or defaults
    if regions is None:
        if not default_xlims:
            raise ValueError(f"No default regions found for element '{element}' and no regions provided")
        regions = default_xlims

    n_regions = len(regions)
    # Auto-calculate grid layout if not specified
    if nrows is None and ncols is None:
        ncols = min(3, n_regions)  # Max 3 columns
        nrows = (n_regions + ncols - 1) // ncols  # Ceiling division
    elif nrows is None:
        nrows = (n_regions + ncols - 1) // ncols
    elif ncols is None:
        ncols = (n_regions + nrows - 1) // nrows

    if nrows * ncols < n_regions:
        raise ValueError(f"Grid {nrows}x{ncols} ({nrows*ncols} subplots) too small for {n_regions} regions")



    ###------### LIMITS, NORMALIZATION AND OFFSETS ###------###
    # Merge defaults with user parameters
    params = {}
    
    # Add xlims for each region
    for i, region in enumerate(regions, 1):
        params[f"xlim{i}"] = region
    
    # Add ylims (use defaults or custom)
    for i in range(1, n_regions + 1):
        params[f"ylim{i}"] = kwargs.get(f"ylim{i}", default_ylim)
    
    # Add offsets
    params.update(default_offsets)
    params.update(kwargs)



    
    
    # Load data
    obs_data = load_spectrum(observed_file, is_observed=True)
    syn_data = [load_spectrum(f) for f in synthetic_files]

    # Calculate normalization for each region
    norm = []
    for i in range(1, n_regions + 1):
        xlim = params[f"xlim{i}"]
        region_norm = obs_data[obs_data['Wavelength'].between(*xlim)]['Flux'].median()
        norm.append(region_norm)

    # Create figure
    default_figsize = Config.DEFAULT_FIGSIZE.get(element, Config.DEFAULT_FIGSIZE.get('default', (12, 8)))
    figsize = figsize or default_figsize
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, tight_layout=True)

    # Handle single subplot case
    if n_regions == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    
    fig.suptitle(f"{element} Lines - {starname}", y=1.02, fontsize=16)
    fig.subplots_adjust(top=0.85)

    # Get line markers for this element
    line_markers = Config.LINE_MARKERS.get(element, {})
    
    # Plot each region
    for i, ax in enumerate(axes):
        if i >= n_regions:
            ax.set_visible(False)  # Hide unused subplots
            continue
            
        xlim = params[f"xlim{i+1}"]
        ylim = params[f"ylim{i+1}"]
        
        # Plot observed spectrum
        ax.plot(
            obs_data["Wavelength"] + (params.get("rvoffset", 0)/299792.458 * obs_data["Wavelength"]),
            (obs_data["Flux"]/norm[i])/params.get(f"ncorr{i+1}", 1.0) + params.get(f"yoffset{i+1}", 0), 
            '--', 
            linewidth=0.7,
            color=Config.LINE_COLORS["obs"],
            label="Observed" if i == 0 else ""
        )
        
        # Plot synthetic spectra
        for j, (data, label) in enumerate(zip(syn_data, labels)):
            ax.plot(
                data["Wavelength"], 
                data["Flux"], 
                label=label if i == 0 else ""
            )
        
        # Add element line markers if available
        for ion_type, lines in line_markers.items():
            if i < len(lines):
                line_wavelength = lines[i]
                ax.axvline(
                    x=line_wavelength,
                    ymin=0.10, ymax=0.25,
                    color=Config.LINE_COLORS.get(element, 'blue'),
                    linestyle="-",
                    alpha=0.8,
                    linewidth=2
                )
                # Add wavelength label
                ax.text(
                    x=0.01,
                    y=0.01,
                    s=f"{ion_type} - {line_wavelength}",
                    ha='left',
                    va='bottom',
                    fontsize=14,
                    transform=ax.transAxes
                )
        
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        setxTicks(ax, N=4)
        ax.grid(True, alpha=0.3)
        
        # Add subplot labels (A, B, C, ...)
        ax.text(0.02, 0.98, f"({chr(65+i)})", transform=ax.transAxes, 
                fontsize=12, fontweight='bold', va='top')
    
    # Single legend for all subplots
    handles, labels_legend = axes[0].get_legend_handles_labels()
    if handles:  # Only create legend if there are handles
        fig.legend(
            handles, labels_legend,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.0),
            ncol=len(labels_legend),
            frameon=True,
            fancybox=True,
            shadow=True,
            fontsize=14
        )
    
    # Add x-labels to bottom row only
    for ax in axes[-(ncols):]:
        ax.set_xlabel("Wavelength (Å)")
    
    # Add y-label to left column only  
    for ax in axes[::ncols]:
        ax.set_ylabel("Normalized Flux")
    
    if save:
        saved_path = save_figure(fig, starname, element.lower())
    if show:
        plt.show()
    plt.close()
    
    return saved_path if save else None
