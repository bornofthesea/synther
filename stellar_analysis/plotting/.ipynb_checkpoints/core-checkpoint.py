import numpy as np
import matplotlib.pyplot as plt

def setxTicks(ax, N: int = 5) -> None:
    """Set custom x-axis ticks with integer spacing.
    
    Args:
        ax: Matplotlib axis object
        N: Number of ticks to generate
    """
    xmin, xmax = ax.get_xlim()
    custom_ticks = np.linspace(xmin, xmax, N, dtype=int)
    ax.set_xticks(custom_ticks)
    ax.set_xticklabels(custom_ticks)