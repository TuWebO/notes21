import numpy as np
from typing import List
from .core import Note, KEY_SHIFTS

class GridEncoder:
    """
    Encoder for converting musical notes into a 7x3 grid representation
    based on a specific key signature.
    """
    def __init__(self, key: str = "C"):
        if key not in KEY_SHIFTS:
            raise ValueError(f"Unknown key: {key}. Available keys: {list(KEY_SHIFTS.keys())}")
        self.key = key

    def encode(self, notes: List[Note]) -> np.ndarray:
        """
        Returns a 7x3 matrix representation of the notes.
        
        The grid dimensions corresponding to:
        - Rows (0-6): Diatonic scale degrees (C, D, E, F, G, A, B)
        - Columns (0-2): Relative accidental (-1, 0, +1)
          - Column 0: Flat relative to key (-1)
          - Column 1: Natural relative to key (0)
          - Column 2: Sharp relative to key (+1)
          
        Note: This representation collapses octave information, aggregating counts
        of pitch classes relative to the key.

        Args:
            notes: List of Note objects to encode.

        Returns:
            np.ndarray: A 7x3 integer matrix where each cell contains the count
            of notes matching that diatonic index and relative accidental.
        """
        # Shape: (7 diatonic steps, 3 accidental positions)
        grid = np.zeros((7, 3), dtype=int)

        for note in notes:
            row, rel_acc, _ = note.to_grid(self.key)
            # Map relative accidental (-1, 0, 1) to column index (0, 1, 2)
            col = rel_acc + 1
            
            # Identify valid column range [0, 2]
            # This handles cases where relative accidental might be out of
            # the standard -1/0/+1 range (e.g. double sharps in some keys),
            # though standard theory usage within this system aims to keep it within.
            # We strictly clip or ignore? 
            # For now, let's only count if it fits the 3-slot window.
            if 0 <= col <= 2:
                grid[row, col] += 1
            # else:
            #     # Optionally log or handle out-of-bounds accidentals if we want strictness.
            #     pass

        return grid