# 21notes

A tonal computation engine based on a structured **7×3 grid representation** of music.

21notes provides:

- A formal note abstraction (`Note`)
- Key-aware grid projection
- 2D harmonic encoding (octave-collapsed)
- 3D register-aware encoding (octave-preserving)
- Text and graphical visualization
- A FastAPI-based HTTP API
- Full test coverage

---

## 🧠 Concept

The system models pitch using a **7×3 tonal grid**:

- **7 rows** → Diatonic degrees (C, D, E, F, G, A, B)
- **3 columns** → Relative accidental (flat, natural, sharp)
- Optional **3rd dimension** → Octave (register)

This creates a structured tonal geometry suitable for:

- Harmonic analysis
- Tonal fingerprinting
- Register-aware modeling
- Algorithmic processing
- ML embedding experiments

---

## 📦 Project Structure

```text
src/notes21/
    music/
        core.py
        encoding.py
        visualization.py
    api/
        app.py
```

---

## ⚙️ Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project (runtime dependencies included):

```bash
pip install -e .
```

Install development dependencies:

```bash
pip install -e .[dev]
``` 

---

## 🚀 Running the API

Start the FastAPI server:

```bash
uvicorn notes21.api.app:app
```

Then open:

```text
http://127.0.0.1:8000/docs
```

to access the interactive API documentation.

---

## 🎵 Example API Usage

### JSON grid response

```bash
curl "http://127.0.0.1:8000/grid?note=Db&key=C"
```

### Plain text grid response

```bash
curl "http://127.0.0.1:8000/grid?note=Db&key=C&format=text"
```

---

## 🧪 Testing

Run the test suite:

```bash
pytest
```

---

## 🏗 Representations

### 2D Harmonic Grid

Octave-collapsed tonal distribution:

```text
shape → (7, 3)
```

Use case:
- Harmony analysis
- Chord density
- Tonal fingerprinting

---

### 3D Register-Aware Grid

Octave-preserving tonal tensor:

```text
shape → (D, 7, 3)
```

Where `D` = number of octaves in the selected range.

Use case:
- Melody modeling
- Voice leading
- Register-sensitive analysis
- Expressive structure modeling

---

## 📚 Documentation

- `docs/7x3_music_representation.md`
- `docs/7x3_2D_vs_3D_tonal_grid_representations.md`
- `docs/7x3_structural_and_computational_significance.md`
- `docs/api.md`

---

## 🧩 Status

Early-stage tonal computation framework.

Designed for experimentation, research, and computational music modeling.