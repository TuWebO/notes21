import unittest
import numpy as np
from src.music.core import Note
from src.music.encoding import GridEncoder

class TestGridEncoder(unittest.TestCase):
    def test_c_major_scale_in_c(self):
        """Test basic diatonic notes in C Major mapped to C Major grid."""
        encoder = GridEncoder("C")
        notes = [
            Note("C"), Note("D"), Note("E"), Note("F"), 
            Note("G"), Note("A"), Note("B")
        ]
        grid = encoder.encode(notes)
        
        # In Key of C, all these are natural (0 relative accidental).
        # Col 0 -> Flat (-1 relative)
        # Col 1 -> Natural (0 relative)
        # Col 2 -> Sharp (+1 relative)
        # We expect all notes to fall in Column 1.
        
        expected_col = 1
        for i in range(7):
            self.assertEqual(grid[i, expected_col], 1, f"Note at index {i} should be in center column")
            
        # Ensure other columns are empty
        self.assertTrue(np.all(grid[:, 0] == 0))
        self.assertTrue(np.all(grid[:, 2] == 0))

    def test_g_major_scale_in_g(self):
        """Test G Major scale notes mapped to G Major grid."""
        # G Major: G A B C D E F#
        # Key Sig: F#
        encoder = GridEncoder("G")
        notes = [
            Note("G"), Note("A"), Note("B"), Note("C"), 
            Note("D"), Note("E"), Note("F#")
        ]
        grid = encoder.encode(notes)
        
        # In Key of G:
        # G is natural -> relative 0
        # A is natural -> relative 0
        # ...
        # F# is the diatonic 7th. In Key G, F# is the "natural" state of that degree.
        # So F# should also have relative accidental 0 (center column).
        
        # Let's verify manual calc for F#:
        # F# diatonic index (F) = 3
        # F# accidental = +1
        # Key Shift for F in G Major = +1 (from KEY_SHIFTS["G"])
        # Relative = (+1) - (+1) = 0. Correct.
        
        expected_col = 1
        # All 7 diatonic degrees should be in center column
        self.assertTrue(np.all(grid[:, 1] == 1))
        self.assertTrue(np.all(grid[:, 0] == 0))
        self.assertTrue(np.all(grid[:, 2] == 0))

    def test_chromatic_alteration(self):
        """Test a sharp note in C Major (chromatic)."""
        encoder = GridEncoder("C")
        # F# in C Major
        # F is index 3.
        # F# in C: accidental=+1. KeyShift(F in C)=0. Rel = +1 - 0 = +1.
        # Should be in Column 2 (Right).
        notes = [Note("F#")]
        grid = encoder.encode(notes)
        
        self.assertEqual(grid[3, 2], 1)
        self.assertEqual(grid[3, 1], 0)

    def test_flat_alteration(self):
        """Test a flat note in C Major."""
        encoder = GridEncoder("C")
        # Bb in C.
        # B is index 6.
        # Bb accidental=-1. KeyShift(B in C)=0. Rel = -1.
        # Should be in Column 0 (Left).
        notes = [Note("Bb")]
        grid = encoder.encode(notes)
        
        self.assertEqual(grid[6, 0], 1)

    def test_context_g_major_chromatic(self):
        """Test F natural in G Major (mixolydian/chromatic)."""
        # In G Major, F is normally F# (+1).
        # F natural (acc=0).
        # KeyShift(F in G) = +1.
        # Rel = 0 - 1 = -1.
        # Should be in Column 0 (Left).
        encoder = GridEncoder("G")
        notes = [Note("F")]  # Natural F
        grid = encoder.encode(notes)
        
        self.assertEqual(grid[3, 0], 1) # F is index 3

    def test_accumulation(self):
        """Test multiple notes mapping to same cell."""
        encoder = GridEncoder("C")
        # Two C4s and one C5. All map to C, rel 0.
        notes = [Note("C", 4), Note("C", 5), Note("C", 4)]
        grid = encoder.encode(notes)
        
        self.assertEqual(grid[0, 1], 3) # C is index 0

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            GridEncoder("InvalidKey")

    def test_key_shift_f_sharp(self):
        # F# Major has 6 sharps: F# C# G# D# A# E#
        # Let's test E# (diatonic 7th) mapping to center.
        encoder = GridEncoder("F#")
        # E# -> E index (2). Acc +1.
        # KeyShift E in F# = +1.
        # Rel = 1 - 1 = 0.
        notes = [Note("E#")]
        grid = encoder.encode(notes)
        self.assertEqual(grid[2, 1], 1)

if __name__ == "__main__":
    unittest.main()
