import sys
import os

# Add src to path to import music.core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from music.core import Note, KEY_SHIFTS

def test_note_creation():
    print("Testing Note Creation...")
    n = Note("C", 4)
    assert n.diatonic_index == 0
    assert n.accidental_val == 0
    assert n.octave == 4
    print("  Note('C', 4) -> (0, 0, 4) [PASS]")

    n2 = Note("F#", 3)
    assert n2.diatonic_index == 3 # F is index 3 (C=0, D=1, E=2, F=3)
    assert n2.accidental_val == 1
    assert n2.octave == 3
    print("  Note('F#', 3) -> (3, 1, 3) [PASS]")

    n3 = Note("Bbb", 5)
    assert n3.diatonic_index == 6 # B is index 6
    assert n3.accidental_val == -2
    assert n3.octave == 5
    print("  Note('Bbb', 5) -> (6, -2, 5) [PASS]")

def test_key_shifts():
    print("\nTesting Key Shifts (to_grid)...")
    
    # C Major Test
    # "C" -> (0, 0, o)
    n = Note("C", 4)
    grid = n.to_grid("C")
    assert grid == (0, 0, 4)
    print("  C in C Major -> (0, 0, 4) [PASS]")

    # G Major Test (F is sharp)
    # "F#" -> j_abs=1. m_k=1. j_rel = 1 - 1 = 0
    n = Note("F#", 4)
    grid = n.to_grid("G")
    assert grid == (3, 0, 4)
    print("  F# in G Major -> (3, 0, 4) [PASS]")

    # "F" (natural) -> j_abs=0. m_k=1. j_rel = 0 - 1 = -1
    n = Note("F", 4)
    grid = n.to_grid("G")
    assert grid == (3, -1, 4)
    print("  F in G Major -> (3, -1, 4) [PASS]")

    # F Major Test (B is flat)
    # "Bb" -> j_abs=-1. m_k=-1. j_rel = -1 - (-1) = 0
    n = Note("Bb", 4)
    grid = n.to_grid("F")
    assert grid == (6, 0, 4)
    print("  Bb in F Major -> (6, 0, 4) [PASS]")

    # "B" (natural) -> j_abs=0. m_k=-1. j_rel = 0 - (-1) = +1
    n = Note("B", 4)
    grid = n.to_grid("F")
    assert grid == (6, 1, 4)
    print("  B in F Major -> (6, 1, 4) [PASS]")
    
    # E Major Test (F# G# C# D#)
    # "D#" -> j_abs=1. m_k=1. j_rel = 0
    n = Note("D#", 4)
    grid = n.to_grid("E")
    # D is index 1. KEY_SHIFTS["E"][1] is 1.
    assert grid == (1, 0, 4)
    print("  D# in E Major -> (1, 0, 4) [PASS]")


if __name__ == "__main__":
    try:
        test_note_creation()
        test_key_shifts()
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
