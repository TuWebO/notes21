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
    from notes21.music.core import NOTE_NAMES, ACCIDENTALS, KEY_SHIFTS

    note_options = "".join(
        f'<option value="{n}">{n}</option>' for n in NOTE_NAMES
    )

    accidental_options = "".join(
        f'<option value="{a}">{a if a else "natural"}</option>'
        for a in ACCIDENTALS.keys()
    )

    key_options = "".join(
        f'<option value="{k}">{k}</option>' for k in KEY_SHIFTS.keys()
    )

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>notes21 — Tonal Calculator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 0;
            position: relative;
        }}

        .container {{
            max-width: 520px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}

        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .row {{
            display: flex;
            gap: 10px;
            margin-bottom: 18px;
        }}

        select, input {{
            flex: 1;
            padding: 12px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ddd;
        }}

        button {{
            width: 100%;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            background-color: #2f80ed;
            color: white;
            cursor: pointer;
        }}

        button:hover {{
            background-color: #1c60c7;
        }}

        .footer {{
            margin-top: 25px;
            text-align: center;
            font-size: 14px;
            color: #666;
        }}

    </style>
</head>

<body>
    <div class="container">
        <h1>🎹 notes21 Tonal Calculator</h1>

        <form action="/grid/view" method="get">

            <div class="row">
                <label for="note">Note</label>
                <select name="note" id="note">
                    {note_options}
                </select>

                <label for="acc">Accidental</label>
                <select name="acc" id="acc">
                    {accidental_options}
                </select>

                <label for="octave">Octave</label>  
                <input name="octave" type="number" value="4" min="-1" max="8">
            </div>

            <div class="row">
                <label for="key">Key Signature</label>
                <select name="key" id="key">
                    {key_options}
                </select>
            </div>

            <button type="submit">Compute Grid</button>
        </form>

        <div class="footer">
            API Docs: <a href="/docs">/docs</a><br>
            <div style="margin-top:10px;">
                <a href="https://github.com/TuWebO/notes21"
                   target="_blank"
                   aria-label="GitHub Repository"
                   style="display:inline-block;">
                    <svg viewBox="0 0 16 16" width="22" height="22" fill="#333"
                         xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 0C3.58 0 0 3.58 0 8a8 8 0 0 0 5.47 7.59c.4.07.55-.17.55-.38
                        0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
                        -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66
                        .07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95
                        0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12
                        0 0 .67-.21 2.2.82a7.66 7.66 0 0 1 2-.27c.68 0 1.36.09 2 .27
                        1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12
                        .51.56.82 1.27.82 2.15
                        0 3.07-1.87 3.75-3.65 3.95
                        .29.25.54.73.54 1.48
                        0 1.07-.01 1.93-.01 2.2
                        0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>
                    </svg>
                </a>
            </div>
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
    octave: str | None = Query("4", description="Octave number"),
    key: str = Query("C", description="Key signature"),
    format: str = Query(None, description="Optional format override: json or text")
):
    try:
        # ---- Normalize octave ----
        if octave is None or octave.strip() == "":
            octave_int = 4
        else:
            octave_int = int(octave)

        # ---- Core logic ----
        n = Note(note, octave_int)
        encoder = GridEncoder(key)
        grid = encoder.encode_harmonic([n])

        # ---- Determine response format ----

        # Priority 1: explicit ?format=
        if format == "text":
            return PlainTextResponse(format_note_grid([n], key=key))

        if format == "json":
            return JSONResponse({
                "note": note,
                "octave": octave_int,
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
            "octave": octave_int,
            "key": key,
            "grid": grid.tolist()
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/grid/view", response_class=HTMLResponse)
def grid_view(
    note: str,
    octave: str | None = "4",
    key: str = "C",
    acc: str = ""
):
    try:
        # ---- Normalize octave ----
        if octave is None or octave.strip() == "":
            octave = 4
        else:
            octave = int(octave)

        # ---- Combine accidental ----
        note_full = note + (acc if acc else "")

        n = Note(note_full, octave)
        encoder = GridEncoder(key)
        grid_text = format_note_grid([n], key=key)

        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>notes21 Result</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f4f6f8;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        h1 {{
            text-align: center;
        }}
        pre {{
            background: #f7f7f7;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .btn {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 18px;
            background: #2f80ed;
            color: white;
            text-decoration: none;
            border-radius: 8px;
        }}
        .btn:hover {{
            background: #1c60c7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>7×3 Tonal Grid</h1>
        <pre>{grid_text}</pre>
        <a href="/" class="btn">← Back</a>
    </div>
</body>
</html>
"""

    except ValueError as e:
        return render_error_html(str(e))


def render_error_html(message: str):
    from notes21.music.core import KEY_SHIFTS

    if "Unknown key" in message:
        title = "Invalid Key"
    elif "Invalid note base name" in message:
        title = "Invalid Note"
    elif "Octave" in message:
        title = "Invalid Octave"
    else:
        title = "Invalid Input"

    available_keys = ", ".join(KEY_SHIFTS.keys())

    return HTMLResponse(
        content=f"""
<!DOCTYPE html>
<html>
<head>
    <title>notes21 Error</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #f4f6f8;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            text-align: center;
        }}
        h1 {{
            color: #d32f2f;
        }}
        p {{
            font-size: 16px;
            margin: 15px 0;
        }}
        .keys {{
            font-size: 14px;
            color: #555;
            margin-top: 10px;
        }}
        .btn {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 18px;
            background: #2f80ed;
            color: white;
            text-decoration: none;
            border-radius: 8px;
        }}
        .btn:hover {{
            background: #1c60c7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p>{message}</p>
        <div class="keys">
            Supported keys: {available_keys}
        </div>
        <a href="/" class="btn">← Back</a>
    </div>
</body>
</html>
""",
        status_code=400
    )