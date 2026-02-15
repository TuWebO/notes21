from typing import List, Optional, Tuple

try:
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib import animation
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from .core import Note, NOTE_NAMES

def print_note_grid(notes: List[Note], key: str = "C", title: Optional[str] = None):
    """
    Prints a text-based 7x3 grid representation of notes.
    """
    if title:
        print(f"\n--- {title} ---")
    else:
        print(f"\n--- 7x3 Music Grid (Key: {key}) ---")
        
    # Initialize grid: 7 rows (C-B), 3 columns (-1, 0, 1)
    # We'll store lists of note strings at each cell
    grid = [[[] for _ in range(3)] for _ in range(7)]
    
    for note in notes:
        row, rel_acc, octave = note.to_grid(key)
        # rel_acc is -1, 0, 1. Map to index 0, 1, 2
        # rel_acc is grid relative accidental.
        # -1 = Flat relative to key
        # 0 = Natural relative to key
        # +1 = Sharp relative to key
        
        col_idx = rel_acc + 1
        if 0 <= col_idx <= 2:
            grid[row][col_idx].append(f"{note.original_name}{note.octave}")
            
    # Print header
    # 7 rows. 0=C, 6=B.
    # Usually graphs have Y going up. So let's print B (6) first down to C (0).
    
    print("-" * 65)
    print(f"{'Row':<4} | {'Flat (-1)':<18} | {'Natural (0)':<18} | {'Sharp (+1)':<18}")
    print("-" * 65)
    
    for i in range(6, -1, -1):
        row_name = NOTE_NAMES[i]
        flat_notes = ", ".join(grid[i][0])
        nat_notes = ", ".join(grid[i][1])
        sharp_notes = ", ".join(grid[i][2])
        print(f"{row_name:<4} | {flat_notes:<18} | {nat_notes:<18} | {sharp_notes:<18}")
    print("-" * 65)


def plot_note_grid(notes: List[Note], key: str = "C", title: Optional[str] = None):
    """
    Plots a list of Notes on a 7x3 grid using matplotlib.
    If matplotlib is not available, prints a text representation.
    
    Args:
        notes: List of Note objects to plot.
        key: Key signature for grid mapping.
        title: Optional title for the plot.
    """
    if not MATPLOTLIB_AVAILABLE:
        print(f"Warning: Matplotlib not available. Printing text grid for '{title or 'Grid'}' instead.")
        print_note_grid(notes, key, title)
        return None
    
    # Grid configuration
    # Rows: 0-6 (C-B)
    # Cols: -1 (Flat), 0 (Natural/Default), +1 (Sharp)
    
    # Prepare data points
    x_coords = []
    y_coords = []
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for note in notes:
        row, rel_acc, octave = note.to_grid(key)
        
        # x-axis: relative accidental (-1, 0, 1)
        # y-axis: diatonic index (0-6)
        
        x_coords.append(rel_acc)
        y_coords.append(row)
        
        # Annotation text: Note name + octave
        # Reconstruct note name for display if needed or use original
        label = f"{note.original_name}{note.octave}"
        
        # Slight jitter or offset if multiple notes? 
        # For now, just plot.
        
        ax.annotate(label, (rel_acc, row), 
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=9, alpha=0.8)

    # Plot the points
    ax.scatter(x_coords, y_coords, c='blue', alpha=0.6, s=100, edgecolors='black')
    
    # Configure Axes
    
    # Y-Axis: Note names
    ax.set_yticks(range(7))
    ax.set_yticklabels(NOTE_NAMES)
    ax.set_ylabel("Diatonic Root")
    
    # X-Axis: Relative Accidental
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["Flat (-1)", "Natural (0)", "Sharp (+1)"])
    ax.set_xlabel(f"Relative Accidental (Key: {key})")
    
    # Grid limits with some padding
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 6.5)
    
    # Add grid lines
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Title
    if title:
        ax.set_title(title)
    else:
        ax.set_title(f"7x3 Music Grid (Key: {key})")
        
    plt.tight_layout()
    
    return fig

def format_note_grid(notes: List[Note], key: str = "C", title: Optional[str] = None) -> str:
    """
    Returns a text-based 7x3 grid representation of notes as a string.
    """

    lines = []

    if title:
        lines.append(f"\n--- {title} ---")
    else:
        lines.append(f"\n--- 7x3 Music Grid (Key: {key}) ---")

    grid = [[[] for _ in range(3)] for _ in range(7)]

    for note in notes:
        row, rel_acc, octave = note.to_grid(key)
        col_idx = rel_acc + 1
        if 0 <= col_idx <= 2:
            grid[row][col_idx].append(f"{note.original_name}{note.octave}")

    lines.append("-" * 65)
    lines.append(f"{'Row':<4} | {'Flat (-1)':<18} | {'Natural (0)':<18} | {'Sharp (+1)':<18}")
    lines.append("-" * 65)

    for i in range(6, -1, -1):
        row_name = NOTE_NAMES[i]
        flat_notes = ", ".join(grid[i][0])
        nat_notes = ", ".join(grid[i][1])
        sharp_notes = ", ".join(grid[i][2])
        lines.append(
            f"{row_name:<4} | {flat_notes:<18} | {nat_notes:<18} | {sharp_notes:<18}"
        )

    lines.append("-" * 65)

    return "\n".join(lines) + "\n"

def plot_note_grid_3d(notes: List[Note], key: str = "C",
                      octave_range: Optional[Tuple[int, int]] = None,
                      title: Optional[str] = None):
    """
    Visualize notes in 3D tonal space.

    This function plots musical notes in the full 3D tonal coordinate system:

        (Relative Accidental, Diatonic Degree, Octave)

    Axes:
        X-axis → Relative accidental (-1 = flat, 0 = natural, +1 = sharp)
        Y-axis → Diatonic degree (0–6 corresponding to C–B)
        Z-axis → Octave (register)

    Conceptual Meaning:
        - The X/Y plane represents the 2D harmonic tonal grid (7×3).
        - The Z dimension represents register (octave).
        - The 2D harmonic representation is equivalent to collapsing this
          3D space along the octave axis.

    This visualization is useful for:
        - Inspecting melody contour
        - Analyzing register distribution
        - Observing chromatic deviation across octaves
        - Debugging 3D tonal encodings

    Parameters
    ----------
    notes : List[Note]
        List of Note objects to visualize.

    key : str, optional
        Key signature used for relative accidental normalization.
        Must exist in KEY_SHIFTS.

    octave_range : Optional[Tuple[int, int]], optional
        Inclusive (min_octave, max_octave) range.
        Notes outside this range are ignored.
        If None, all octaves present in `notes` are shown.

    title : Optional[str], optional
        Custom plot title. If None, a default title is generated.

    Raises
    ------
    ValueError
        If a note contains a relative accidental outside the supported
        range [-1, 0, +1].

    Returns
    -------
    matplotlib.figure.Figure
        The generated matplotlib figure object.
        Returns None if matplotlib is unavailable.

    Notes
    -----
    This function is a visualization tool only. It does not modify or
    encode musical data. For tensor-based representations, use GridEncoder.
    """ 
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available.")
        return None

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    x_vals = []
    y_vals = []
    z_vals = []

    for note in notes:
        row, rel_acc, octave = note.to_grid(key)

        if octave_range is not None:
            min_oct, max_oct = octave_range
            if not (min_oct <= octave <= max_oct):
                continue

        if rel_acc not in [-1, 0, 1]:
            raise ValueError(
                f"Relative accidental {rel_acc} out of supported range [-1, 0, +1]"
            )

        x_vals.append(rel_acc)
        y_vals.append(row)
        z_vals.append(octave)

        label = f"{note.original_name}{note.octave}"
        ax.text(rel_acc, row, octave, label, fontsize=8)

    ax.scatter(x_vals, y_vals, z_vals,
               c=z_vals,
               cmap="viridis",
               s=80,
               alpha=0.7)

    ax.set_xlabel("Relative Accidental")
    ax.set_ylabel("Diatonic Degree")
    ax.set_zlabel("Octave")

    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["Flat (-1)", "Natural (0)", "Sharp (+1)"])

    ax.set_yticks(range(7))
    ax.set_yticklabels(NOTE_NAMES)

    if octave_range is not None:
        ax.set_zlim(min_oct - 0.5, max_oct + 0.5)

    if title:
        ax.set_title(title)
    else:
        ax.set_title(f"3D Tonal Grid (Key: {key})")

    fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
    return fig

def animate_tonal_trajectory(
    notes: List[Note],
    key: str = "C",
    octave_range: Optional[Tuple[int, int]] = None,
    interval: int = 600,
    title: Optional[str] = None
):
    """
    Animate notes as a trajectory through 3D tonal space.

    Shows sequential motion in:
        X → Relative accidental
        Y → Diatonic index
        Z → Octave

    Args:
        notes: Ordered list of Note objects
        key: Key signature
        octave_range: Optional (min_oct, max_oct)
        interval: Time between frames (ms)
        title: Optional plot title

    Returns:
        matplotlib.animation.FuncAnimation
    """

    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib not available.")
        return None

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    xs, ys, zs = [], [], []

    for note in notes:
        row, rel_acc, octave = note.to_grid(key)

        if rel_acc not in [-1, 0, 1]:
            raise ValueError(
                f"Relative accidental {rel_acc} out of supported range [-1, 0, +1]"
            )

        if octave_range is not None:
            min_oct, max_oct = octave_range
            if not (min_oct <= octave <= max_oct):
                continue

        xs.append(rel_acc)
        ys.append(row)
        zs.append(octave)

    line, = ax.plot([], [], [], lw=2)
    points = ax.scatter([], [], [], s=80)

    ax.set_xlabel("Relative Accidental")
    ax.set_ylabel("Diatonic Degree")
    ax.set_zlabel("Octave")

    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(["Flat (-1)", "Natural (0)", "Sharp (+1)"])

    ax.set_yticks(range(7))
    ax.set_yticklabels(NOTE_NAMES)

    if octave_range is not None:
        ax.set_zlim(min_oct - 0.5, max_oct + 0.5)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 6.5)

    if title:
        ax.set_title(title)
    else:
        ax.set_title("Animated Tonal Trajectory")

    def update(frame):
        line.set_data(xs[:frame], ys[:frame])
        line.set_3d_properties(zs[:frame])
        points._offsets3d = (xs[:frame], ys[:frame], zs[:frame])
        return line, points

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(xs) + 1,
        interval=interval,
        blit=False,
        repeat=False
    )

    plt.close(fig)

    return ani
