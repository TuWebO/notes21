from typing import Tuple, Dict

# Constants
NOTE_NAMES = ["C", "D", "E", "F", "G", "A", "B"]
DIATONIC_BASE = [0, 2, 4, 5, 7, 9, 11]

# Key shifts as defined in docs/7x3_music_representation.md
KEY_SHIFTS: Dict[str, list] = {
    "C":  [0, 0, 0, 0, 0, 0, 0],
    "G":  [0, 0, 0, 1, 0, 0, 0],
    "D":  [1, 0, 0, 1, 0, 0, 0],
    "A":  [1, 0, 0, 1, 1, 0, 0],
    "E":  [1, 1, 0, 1, 1, 0, 0],
    "B":  [1, 1, 0, 1, 1, 1, 0],
    "F#": [1, 1, 1, 1, 1, 1, 0],
    "C#": [1, 1, 1, 1, 1, 1, 1],
    "F":  [0, 0, 0, 0, 0, 0, -1],
    "Bb": [0, 0, -1, 0, 0, 0, -1],
    "Eb": [0, 0, -1, 0, 0, -1, -1],
    "Ab": [0, -1, -1, 0, 0, -1, -1],
    "Db": [0, 0, -1, -1, -1, -1, -1],
    "Gb": [0, -1, -1, -1, -1, -1, -1],
    "Cb": [-1, -1, -1, -1, -1, -1, -1]
}

ACCIDENTALS = {
    "#": 1,
    "b": -1,
    "x": 2,  # double sharp
    "bb": -2, # double flat
    "": 0,
    "n": 0 # natural explicitly
}

class Note:
    """
    Represents a musical note with pitch, accidental, and octave information.
    Capable of mapping to a 7x3 grid representation based on a key signature.
    """
    def __init__(self, name: str, octave: int = 4):
        """
        Initialize a Note.
        
        Args:
            name: The note name (e.g., 'C', 'F#', 'Bbb').
            octave: The octave number (default 4).
        """
        self.original_name = name
        self.octave = octave
        self.diatonic_index, self.accidental_val = self._parse_name(name)
        
    def _parse_name(self, name: str) -> Tuple[int, int]:
        """
        Parses a note string into diatonic index (0-6) and accidental value.
        
        Returns:
            Tuple of (diatonic_index, accidental_value)
        """
        if not name:
            raise ValueError("Note name cannot be empty")
            
        # The first character is always the base note name
        base_char = name[0].upper()
        if base_char not in NOTE_NAMES:
            raise ValueError(f"Invalid note base name: {base_char}")
            
        diatonic_index = NOTE_NAMES.index(base_char)
        
        # The rest is the accidental
        acc_str = name[1:]
        
        # Handle unicode/alternative symbols if necessary, but starting simple
        # Map common symbols to internal representation if needed, 
        # for now assuming standard 'b', '#', 'bb', 'x' or empty
        
        if acc_str in ACCIDENTALS:
            acc_val = ACCIDENTALS[acc_str]
        else:
            # Fallback for simple repeated accidentals if not in map (e.g. ###)
            # though standard notation usually stops at double.
            acc_val = 0
            for char in acc_str:
                if char == '#':
                    acc_val += 1
                elif char == 'b':
                    acc_val -= 1
                elif char == 'x': # double sharp
                    acc_val += 2
                else:
                    raise ValueError(f"Invalid accidental symbol: {char} in note name {name}")
        
        return diatonic_index, acc_val

    def to_grid(self, key: str = "C") -> Tuple[int, int, int]:
        """
        Maps the note to the 7x3 grid coordinate system for a given key.
        
        Args:
            key: The key signature (e.g., 'C', 'G', 'F#').
            
        Returns:
            Tuple of (row_index, relative_accidental, octave_index)
            row_index (i): 0-6 (C-B)
            relative_accidental (j): -1 (flat), 0 (natural), +1 (sharp) relative to key
            octave_index: integer
        """
        if key not in KEY_SHIFTS:
            # Default to C major shifts (all zeros) if key unknown, or raise error?
            # For robustness let's try to handle minor keys by converting to relative major if passed
            # But per requirements simple lookup first.
            if key.endswith('m'):
                 # extremely basic heuristic: a minor key has same sig as relative major
                 # This requires a proper circle of fifths logic to be robust. 
                 # For now, let's stick to the provided KEY_SHIFTS or error.
                 raise ValueError(f"Key {key} not found in KEY_SHIFTS. Please use Major keys for now.")
            raise ValueError(f"Key {key} not found in KEY_SHIFTS")

        # Get the shift for this note's diatonic position in the given key
        # KEY_SHIFTS[key] is a list of 7 integers corresponding to C, D, E, F, G, A, B
        key_shift = KEY_SHIFTS[key][self.diatonic_index]
        
        # j_rel = j_abs - m_k[i]
        j_rel = self.accidental_val - key_shift
        
        return (self.diatonic_index, j_rel, self.octave)

    def get_absolute_semitone(self) -> int:
        """
        Calculates the absolute semitone value (like MIDI note number).
        C-1 is usually 0, but here we can define C0 = 12, or just relative to C0=0.
        Standard MIDI: C4 = 60. 
        Formula: 12 * (octave + 1) + base + accidental (if C-1 is base 0)
        Or just 12 * octave + base + accidental (if C0 is base 0).
        Let's use 12 * (octave + 1) to align with typical MIDI C4=60.
        """
        base_pitch = DIATONIC_BASE[self.diatonic_index]
        # MIDI C4 is 60. C0 is 12. C-1 is 0.
        # If self.octave is 4, we want C4 to be 60.
        # 12 * (4 + 1) = 60.
        # + base (0 for C) + accidental (0) = 60. Correct.
        return 12 * (self.octave + 1) + base_pitch + self.accidental_val

    def __repr__(self):
        acc_symbol = ""
        if self.accidental_val == 1: acc_symbol = "#"
        elif self.accidental_val == 2: acc_symbol = "x"
        elif self.accidental_val == -1: acc_symbol = "b"
        elif self.accidental_val == -2: acc_symbol = "bb"
        # For complex/custom accidentals, maybe just show number? 
        # But this covers standard ones.
        
        return f"Note({NOTE_NAMES[self.diatonic_index]}{acc_symbol}, oct={self.octave})"
