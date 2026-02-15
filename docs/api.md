# API Documentation

The project includes a lightweight FastAPI service to compute and retrieve 7×3 tonal grid representations via HTTP.

## Running the API

You can run the API server using `uvicorn` from the project root:

```bash
uvicorn src.api.app:app --reload
```

The server will typically start at `http://127.0.0.1:8000`.

## Endpoints

### GET /grid

Computes the 7×3 tonal grid representation for a single note.

**URL**: `/grid`
**Method**: `GET`

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `note` | string | **Required** | The musical note name (e.g., `C`, `F#`, `Bb`, `Cx`). |
| `octave` | integer | `4` | The octave number. |
| `key` | string | `C` | The key signature context for the grid. |
| `format` | string | `null` | Optional format override. standard values: `json`, `text`. |

#### Response Formats

The API supports content negotiation via the `Accept` header or the `format` query parameter.

**1. JSON (Default)**

Returns a JSON object containing the input parameters and the computed grid as a list.

- **Header**: `Accept: application/json`
- **Query**: `?format=json`

**Example Request**:
```bash
curl "http://127.0.0.1:8000/grid?note=C&octave=4&key=C"
```

**Example Response**:
```json
{
  "note": "C",
  "octave": 4,
  "key": "C",
  "grid": [[0,1,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
}
```

**2. Plain Text**

Returns a text-based visualization of the grid.

- **Header**: `Accept: text/plain`
- **Query**: `?format=text`

**Example Request**:
```bash
curl "http://127.0.0.1:8000/grid?note=C&format=text"
```

**Example Response**:
```text
--- 7x3 Music Grid (Key: C) ---
-----------------------------------------------------------------
Row  | Flat (-1)          | Natural (0)        | Sharp (+1)        
-----------------------------------------------------------------
B    |                    |                    |                   
A    |                    |                    |                   
G    |                    |                    |                   
F    |                    |                    |                   
E    |                    |                    |                   
D    |                    |                    |                   
C    |                    | C4                 |                   
-----------------------------------------------------------------
```

