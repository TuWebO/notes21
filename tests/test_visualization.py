from notes21.music.core import Note
from notes21.music.visualization import format_note_grid


def test_format_note_grid_basic():
    notes = [
        Note("C", 4),
        Note("E", 4),
        Note("G", 4),
    ]

    output = format_note_grid(notes, key="C")

    assert isinstance(output, str)
    assert "C4" in output
    assert "E4" in output
    assert "G4" in output
    assert "7x3 Music Grid" in output


def test_format_note_grid_with_key():
    notes = [Note("F#", 4)]
    output = format_note_grid(notes, key="C")

    # In C major, F# is relative sharp
    assert "F#4" in output


def test_format_note_grid_with_key():
    notes = [Note("Bb", 4)]
    output = format_note_grid(notes, key="F")

    # In F major, Bb is natural
    assert "Bb4" in output