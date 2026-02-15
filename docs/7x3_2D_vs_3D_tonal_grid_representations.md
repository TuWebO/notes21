# 2D vs 3D Tonal Grid Representations

## 1. Overview
In our system, pitch is represented using three intrinsic dimensions:
`(Diatonic Index, Relative Accidental, Octave)`

- **Diatonic Index (0–6)** → C, D, E, F, G, A, B.
- **Relative Accidental (-1, 0, +1)** → flat, diatonic, sharp relative to key (deviation from the key signature).
- **Octave** → vertical register (how high or low the note is).

This gives us a 3D tonal coordinate space.

However, not all musical tasks require all three dimensions.

The key design principle is:
> Use different representations depending on the musical question being asked.

## 2. The 2D Harmonic Representation

The tonal system is inherently 3D.
The 2D representation is not a limitation — it is a projection designed for harmonic abstraction.  

Shape: `(7, 3)`

This does NOT mean octave is unimportant in music — it means we are intentionally ignoring it for harmonic abstraction.

**Dimensions**:
- **Rows** → Diatonic Index (C–B).
- **Columns** → Relative Accidental (-1, 0, +1).
- **Octave** → intentionally collapsed (ignored).

**What It Represents**:
- **Harmonic function** → which notes belong to the current key.
- **Chromatic deviation** → how far each note is from the key signature.

This representation answers:
>What harmonic material exists, regardless of register?

It captures:
- Chord identity
- Harmonic density
- Tonal footprint
- Chromatic deviation from the key

**Mathematical Interpretation**:
The 2D grid is a projection:
`P_harmony: (i, j, k) → (i, j)`

- i = diatonic index
- j = relative accidental
- k = octave

This projection collapses the octave dimension, effectively treating all octaves as equivalent for harmonic purposes.


**Use Cases**:
- Chord detection.
- Harmonic analysis.
- Pattern matching.
- Key-relative operations.

**Example**:
In C major, the note G4 is represented as `(4, 0, 4)` in 3D, but as `(4, 0)` in 2D.

## 3. The 3D Register-Aware Representation

Shape: `(7, 3, N)` where N is the number of octaves.

This representation preserves all three dimensions and is used when octave information is important.

**Dimensions**:
- **Row (7)** → Diatonic pitch class (C–B).
- **Column (3)** → Relative accidental (flat, natural, sharp).
- **Depth (N)** → Octave.

**Use Cases**:
- Melodic generation.
- Voice leading.
- Pitch tracking.
- Full piano-roll representation.

## 4. Why This Matters

Harmony is largely octave-invariant.
Melody and voice leading are not octave-invariant.

- **Harmonic analysis** → 2D is sufficient.
- **Melody generation** → 3D is required.

This design gives us flexibility and efficiency.


## 5. Architectural Recommendation
Representation and neural embedding are separate concerns.

Instead of mixing both approaches in one structure:

**Create two explicit encoders.**
Example, Layer 1 — Pure Tonal Representation:
```python
class GridEncoder:
    def encode_harmonic(self, notes):
        # returns 7x3 matrix

    def encode_register(self, notes, octave_range):
        # returns O x 7 x 3 tensor
``` 
Example, Layer 2 — Tonal + Register Embedding:
```python
class TonalEmbedding(nn.Module):
    def __init__(self, input_shape, embed_dim):
        super().__init__()
        self.encoder = nn.Linear(np.prod(input_shape), embed_dim)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.encoder(x)
``` 


## 6. Summary

| Representation | Shape | Octave Preserved? | Use Cases |
|----------------|-------|------------|-----------|
| 2D Harmonic | (7, 3) | No | Chord detection, harmonic analysis |
| 3D Tonal | (O, 7, 3) | Yes | Melody generation, voice leading |

This design principle allows us to use the right tool for the job.

