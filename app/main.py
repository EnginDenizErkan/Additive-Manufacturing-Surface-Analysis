from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

# ---- Yol Kurulumu ----
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

# ---- CORS (gerekirse front-end'ten çağrı yapacaksan lazım) ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # üretimde kısıtla: ["http://localhost:3000", ...]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Statik Dosyalar ----
# /static/3DObjectViewer.css ve /static/3DObjectViewer.js şeklinde çağıracaksın
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# DOE tablosu ve profil verilerini doğrudan sun
app.mount("/doe_data", StaticFiles(directory=DOE_DATA_DIR), name="doe_data")
app.mount("/mahr_data", StaticFiles(directory=MAHR_DATA_DIR), name="mahr_data")

# Yüklenen dosyaları sunmak için (örn. STL’leri geri göstermek istersen)
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# ---- Ana Sayfa (HTML) - YENİ LANDING PAGE ----
@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    html_path = TEMPLATES_DIR / "index.html" # Serve new landing page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="index.html bulunamadı.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ---- 3D Viewer Sayfası - YENİ ROUTE ----
@app.get("/viewer", response_class=HTMLResponse)
def get_viewer(request: Request):
    html_path = TEMPLATES_DIR / "3DObjectViewer.html"  # Serve original viewer page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="3DObjectViewer.html bulunamadı.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ---- Data Sayfası - YENİ ROUTE ----
@app.get("/data", response_class=HTMLResponse)
def get_viewer(request: Request):
    html_path = TEMPLATES_DIR / "data_explorer.html"  # Serve original data page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="data_explorer.html bulunamadı.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ----  Results Sayfası - YENİ ROUTE ----
@app.get("/results", response_class=HTMLResponse)
def get_viewer(request: Request):
    html_path = TEMPLATES_DIR / "results.html"  # Serve original data page
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="results.html bulunamadı.")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

# ---- Sağlık Kontrolü ----
@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Örnek: Dosya Yükleme (STL/GLB/GLTF/OBJ/PLY) ----
@app.post("/api/upload")
async def upload_mesh(file: UploadFile = File(...)):
    allowed = (".stl", ".obj", ".ply", ".glb", ".gltf")
    suffix = Path(file.filename).suffix.lower()
    if suffix not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Desteklenmeyen dosya türü: {suffix}. İzin verilenler: {allowed}",
        )
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    # Frontend’in dosyayı geri çekebilmesi için bir URL dönüyoruz
    return {"filename": file.filename, "url": f"/files/{file.filename}"}

# ---- Örnek: Tahmin Uç Noktası (ileride model entegrasyonu için) ----
@app.post("/api/predict")
async def predict(payload: dict):
    """
    payload örneği:
    {
      "surface_params": {"area": 123.4, "inclination": 30, ...},
      "print_params": {"layer_height": 0.2, "nozzle": 0.4, ...}
    }
    """
    # TODO: Burada gerçek model çağrısı yap
    dummy_result = {"roughness_ra": 3.21, "roughness_rq": 4.56}
    return {"ok": True, "prediction": dummy_result}
