import sys
import os

# Add src to path to import music
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Demo will use text output.")

from music.core import Note, KEY_SHIFTS
from music.visualization import plot_note_grid

def main():
    print("Generating demo visualization...")
    
    # 1. C Major Scale - Simple
    c_major_scale = [
        Note("C", 4), Note("D", 4), Note("E", 4), 
        Note("F", 4), Note("G", 4), Note("A", 4), Note("B", 4),
        Note("C", 5)
    ]
    
    fig = plot_note_grid(c_major_scale, key="C", title="C Major Scale (Key: C)")
    if MATPLOTLIB_AVAILABLE and fig:
        out_path = "c_major_demo.png"
        fig.savefig(out_path)
        print(f"Saved {out_path}")
        plt.close(fig)

    # 2. G Major Scale - F# is default
    g_major_notes = [
        Note("G", 4), Note("A", 4), Note("B", 4), 
        Note("C", 5), Note("D", 5), Note("E", 5), 
        Note("F#", 5), Note("G", 5)
    ]
    
    fig2 = plot_note_grid(g_major_notes, key="G", title="G Major Scale (Key: G)")
    # F# should appear at relative 0 column in Key G
    if MATPLOTLIB_AVAILABLE and fig2:
        out_path2 = "g_major_demo.png"
        fig2.savefig(out_path2)
        print(f"Saved {out_path2}")
        plt.close(fig2)

    # 3. Chromatic / Accidentals in C
    chromatic = [Note("C", 4), Note("C#", 4), Note("D", 4), Note("Eb", 4), Note("E", 4)]
    fig3 = plot_note_grid(chromatic, key="C", title="Chromatic Fragment (Key: C)")
    if MATPLOTLIB_AVAILABLE and fig3:
        out_path3 = "chromatic_demo.png"
        fig3.savefig(out_path3)
        print(f"Saved {out_path3}")
        plt.close(fig3)

if __name__ == "__main__":
    main()
