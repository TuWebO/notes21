# 7×3 Music Representation – Structural and Computational Significance

## 1. Core Concept

The 7×3 matrix represents pitch as a structured coordinate system rather than as a single absolute integer (e.g., MIDI).

Each note is decomposed into three independent components:
- Diatonic index (0–6) → C, D, E, F, G, A, B
- Relative accidental (-1, 0, +1) → flat, diatonic, sharp relative to key
- Octave → vertical register

Formally:  
`Pitch = (Diatonic Index) + (Relative Accidental) + (Octave)`.  
This factorization preserves tonal structure while separating pitch dimensions.

## 2. Role of KEY_SHIFTS (Key Signature)
KEY_SHIFTS is the tonal normalization operator of the system.
The key equation is:  
`j_rel = j_abs - m_k[i]`
where :
- `j_rel` is the relative accidental in the 7×3 grid.
- `j_abs` is the absolute accidental (0 for natural, +1 for sharp, -1 for flat).
- `m_k[i]` is the key shift for the diatonic note `i`.

This means:
- Column 0 represents diatonic with respect to the key.
- Columns ±1 represent chromatic deviation from the key.  

Without KEY_SHIFTS, the system would encode absolute accidentals only and lose tonal invariance.
With KEY_SHIFTS, the grid becomes:
> A key-relative tonal coordinate system.


## 3. Why This Is Music-Theoretically Strong
The representation:
- Encodes functional harmony.
- Distinguishes diatonic notes from chromatic alterations.
- Aligns with circle-of-fifths logic.
- Preserves spelling (C# ≠ Db at symbolic level).

It separates:
- Scale membership.
- Chromatic tension.

This mirrors how tonal music is conceptualized in theory.

## 4. Why This Is Strong for Machine Learning

### 4.1 Reduced Entropy
Instead of modeling 128 MIDI pitches, the system models:
- 7 diatonic classes.
- 3 relative accidental states.
- Octave separately.

This reduces categorical complexity.

### 4.2 Transposition Invariance
In raw MIDI:
- C major and D major look completely different numerically.

In the 7×3 system:
- Diatonic notes always map to column 0.
- Functional harmony remains structurally similar across keys.

This gives tonal invariance, which significantly simplifies learning.

### 4.3 Factorized Representation
Instead of one monolithic pitch token:  
`Embedding = E_diatonic + E_accidental + E_octave`

Factorized representations:
- Are easier to embed.
- Are more interpretable.
- Generalize better.

## 5. Why This Is Efficient for Algorithms
The grid size is constant:  
`7 × 3 = 21 cells`. 

Operations such as:
- Harmonic detection.
- Chromatic deviation analysis.
- Scale membership checks.
- Interval classification.
- Pattern matching.

Can be computed in constant time relative to grid size.  
This is computationally compact compared to piano-roll (128×T) representations.

Become simple grid operations:
- Neighborhood lookups.
- Distance calculations.
- Masking.
- Pattern matching.

This is much faster than working with raw MIDI numbers.

## 6. Pitch-Class Sets and Sets in Harmonic Analysis
Sets are useful for harmonic abstraction.
Example: pitch-class set
`pitch_classes = {note.get_absolute_semitone() % 12 for note in notes}` 

Advantages:
- Removes octave duplication.
- Collapses enharmonic equivalents at pitch-class level.
- Enables chord detection via interval templates.

The 7×3 grid encodes symbolic spelling, while pitch-class sets encode harmonic equivalence.

These representations are complementary.

## 7. Conceptual Interpretation
The 7×3 matrix is:
- A structured tonal coordinate system.
- A normalized representation relative to key.
- A low-dimensional symbolic encoding.  

KEY_SHIFTS transforms the matrix from:
> Absolute notation  

into:
> Tonally intelligent representation.

## 8. Limitations
The system is optimized for:
- Western tonal music.
- Major-key harmony (currently implemented).

It is less naturally suited for:

- Atonal music.
- Microtonal systems.
- Highly chromatic post-tonal contexts.

All representations introduce bias. This one is intentionally tonal.

## 9. Final Conclusion
The 7×3 system is:
- Music-theoretically grounded.
- Tonally normalized.
- Computationally efficient.
- Structurally well-suited for ML.
- Factorized and interpretable.

Its strength comes not from being smaller than MIDI, but from embedding tonal grammar directly into the coordinate system.  
The key signature (KEY_SHIFTS) is the critical component that makes this possible.

If desired, this section can later be extended with:
- Tensor encoding formalization.
- Modulation-aware extensions .
- Minor key support.
- Transformer tokenization strategy.






