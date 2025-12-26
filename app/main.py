from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

# ---- Path Setup ----
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
UPLOAD_DIR = BASE_DIR / "uploads"
DOE_DATA_DIR = BASE_DIR / "doe_data"
MAHR_DATA_DIR = BASE_DIR / "mahr_data"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="EDE Object Viewer Backend",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---- CORS  ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # restrict in production: ["http://localhost:3000", ...]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Static Files ----
# EX: /static/3DObjectViewer.css and /static/3DObjectViewer.js
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# Serve DOE table and profile data directly
app.mount("/doe_data", StaticFiles(directory=DOE_DATA_DIR), name="doe_data")
app.mount("/mahr_data", StaticFiles(directory=MAHR_DATA_DIR), name="mahr_data")

# To serve uploaded files
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# ---- Home Page (HTML) - NEW LANDING PAGE ----
@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    html_path = TEMPLATES_DIR / "index.html"  # Serve new landing page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ---- 3D Viewer Page ----
@app.get("/viewer", response_class=HTMLResponse)
def get_viewer(request: Request):
    html_path = TEMPLATES_DIR / "3DObjectViewer.html"  # Serve original viewer page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="3DObjectViewer.html not found.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ---- Data Page ----
@app.get("/data", response_class=HTMLResponse)
def get_viewer(request: Request):
    html_path = TEMPLATES_DIR / "data_explorer.html"  # Serve original data page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="data_explorer.html not found.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ---- Results Page ----
@app.get("/results", response_class=HTMLResponse)
def get_viewer(request: Request):
    html_path = TEMPLATES_DIR / "results.html"  # Serve original results page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="results.html not found.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ---- Health Check ----
@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Example: File Upload (STL/GLB/GLTF/OBJ/PLY) ----
@app.post("/api/upload")
async def upload_mesh(file: UploadFile = File(...)):
    allowed = (".stl", ".obj", ".ply", ".glb", ".gltf")
    suffix = Path(file.filename).suffix.lower()
    if suffix not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}. Allowed: {allowed}",
        )
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    # Return a URL so the frontend can fetch the file back
    return {"filename": file.filename, "url": f"/files/{file.filename}"}
