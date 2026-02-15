from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from notes21.music.core import Note
from notes21.music.encoding import GridEncoder
from notes21.music.visualization import format_note_grid

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def homepage():
    return """
    <html>
        <head>
            <title>21notes Tonal Grid</title>
        </head>
        <body>
            <h1>21notes — 7×3 Tonal Grid</h1>

            <form action="/grid" method="get">
                <label>Note:</label>
                <input type="text" name="note" value="C" required><br><br>

                <label>Octave:</label>
                <input type="number" name="octave" value="4"><br><br>

                <label>Key:</label>
                <input type="text" name="key" value="C"><br><br>

                <label>Output format:</label>
                <select name="format">
                    <option value="json">JSON</option>
                    <option value="text">Plain Text</option>
                </select><br><br>

                <button type="submit">Compute Grid</button>
            </form>

            <p>
                API Docs: <a href="/docs">/docs</a>
            </p>
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