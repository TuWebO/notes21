from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from notes21 import __version__
from notes21.music.core import Note
from notes21.music.encoding import GridEncoder
from notes21.music.visualization import format_note_grid

app = FastAPI()

@app.get("/version")
def version():
    return {"version": __version__}


@app.get("/", response_class=HTMLResponse)
def homepage():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>21notes Tonal Grid</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f4f6f8;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 500px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }

        h1 {
            text-align: center;
            margin-bottom: 25px;
        }

        label {
            display: block;
            font-weight: 600;
            margin-bottom: 6px;
        }

        input, select {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ddd;
            margin-bottom: 18px;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            background-color: #2f80ed;
            color: white;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            background-color: #1c60c7;
        }

        .footer {
            margin-top: 25px;
            text-align: center;
            font-size: 14px;
            color: #666;
        }

        @media (max-width: 480px) {
            .container {
                margin: 20px;
                padding: 20px;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>21notes — 7×3 Tonal Grid</h1>

        <form action="/grid" method="get">

            <label for="note">Note</label>
            <input type="text" id="note" name="note" value="C" required>

            <label for="octave">Octave</label>
            <input type="number" id="octave" name="octave" value="4">

            <label for="key">Key</label>
            <input type="text" id="key" name="key" value="C">

            <label for="format">Output Format</label>
            <select id="format" name="format">
                <option value="json">JSON</option>
                <option value="text">Text Grid</option>
            </select>

            <button type="submit">Compute Grid</button>
        </form>

        <div class="footer">
            API Docs: <a href="/docs">/docs</a>
        </div>
    </div>
</body>
</html>
"""

@app.get(
    "/grid",
    summary="Return tonal grid (JSON or text)",
    description="""
Compute the 7×3 tonal grid representation of a single note.

You can control the output format via:

- Accept header:
    - application/json (default)
    - text/plain

OR

- Query parameter:
    - ?format=json
    - ?format=text
"""
)
async def get_grid(
    request: Request,
    note: str = Query(..., description="Musical note (e.g., C, F#, Bb, Cx or C##)"),
    octave: int = Query(4, description="Octave number"),
    key: str = Query("C", description="Key signature"),
    format: str = Query(None, description="Optional format override: json or text")
):
    try:
        n = Note(note, octave)
        encoder = GridEncoder(key)
        grid = encoder.encode_harmonic([n])

        # ---- Determine response format ----

        # Priority 1: explicit ?format=
        if format == "text":
            return PlainTextResponse(format_note_grid([n], key=key))

        if format == "json":
            return JSONResponse({
                "note": note,
                "octave": octave,
                "key": key,
                "grid": grid.tolist()
            })

        # Priority 2: Accept header
        accept = request.headers.get("accept", "")

        if "text/plain" in accept:
            return PlainTextResponse(format_note_grid([n], key=key))

        # Default → JSON
        return {
            "note": note,
            "octave": octave,
            "key": key,
            "grid": grid.tolist()
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))