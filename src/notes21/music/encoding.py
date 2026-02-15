import numpy as np
from typing import List, Tuple
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

    def _map_note_to_grid(self, note: Note) -> Tuple[int, int, int]:
        """
        Helper to map a note to grid coordinates (row, col, octave).
        
        Returns:
            row: 0-6 (diatonic index)
            col: 0-2 (relative accidental column index)
            octave: integer octave
        """
        row, rel_acc, octave = note.to_grid(self.key)
        # Map relative accidental (-1, 0, 1) to column index (0, 1, 2)
        col = rel_acc + 1
        if not (0 <= col <= 2):
            raise ValueError(
                f"Relative accidental {rel_acc} out of supported range [-1, 0, +1]"
            )
        return row, col, octave

    def encode_harmonic(self, notes: List[Note]) -> np.ndarray:
        """
        Returns a 7x3 matrix representation of the notes (2D Harmonic Representation).
        
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
            row, col, _ = self._map_note_to_grid(note)
            grid[row, col] += 1

        return grid

    def encode(self, notes: List[Note]) -> np.ndarray:
        """
        Alias for encode_harmonic for backward compatibility.
        """
        return self.encode_harmonic(notes)

    def encode_register(self, notes: List[Note], octave_range: Tuple[int, int]) -> np.ndarray:
        """
        Returns a (D, 7, 3) tensor representation of the notes (3D Register-Aware Representation).
        
        Dimensions:
        - Depth (D): Octaves (from min_octave to max_octave inclusive)
        - Rows (7): Diatonic scale degrees
        - Columns (3): Relative accidentals
        
        Args:
            notes: List of Note objects.
            octave_range: Tuple (min_octave, max_octave).
            
        Returns:
            np.ndarray: shape (D, 7, 3)
        """
        min_oct, max_oct = octave_range

        if min_oct > max_oct:
            raise ValueError("min_octave must be <= max_octave")
        num_octaves = max_oct - min_oct + 1
        
        # Shape: (Octaves, 7 diatonic, 3 accidentals)
        grid = np.zeros((num_octaves, 7, 3), dtype=int)
        
        for note in notes:
            row, col, oct_val = self._map_note_to_grid(note)
            
            # Check if note is within the requested octave range
            if min_oct <= oct_val <= max_oct:
                oct_idx = oct_val - min_oct
                grid[oct_idx, row, col] += 1
                
        return grid