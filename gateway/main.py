from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import uvicorn
from datetime import datetime
import time

app = FastAPI(
    title="Bioinformatics ML Platform",
    description="""
    Unified platform exposing 4 production bioinformatics ML models:
    - DNA Variant Pathogenicity Classifier
    - scRNA-seq Cell Type Classifier  
    - Drug Toxicity Predictor
    - Genomics Pipeline Status
    """,
    version="1.0.0"
)

# Service registry
SERVICES = {
    "dna_classifier":   "http://localhost:8000",
    "scrna_classifier": "http://localhost:8001",
    "drug_toxicity":    "http://localhost:8002",
}

# Simple in-memory metrics
metrics = {
    "total_requests":    0,
    "requests_by_model": {k: 0 for k in SERVICES},
    "errors":            0,
    "start_time":        datetime.utcnow().isoformat(),
}

# ── Request models ──────────────────────────────────────────
class VariantRequest(BaseModel):
    chromosome: str
    ref_allele: str
    alt_allele: str

class CellRequest(BaseModel):
    expression: List[float]

class MoleculeRequest(BaseModel):
    smiles: str

# ── Health ──────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "platform":  "Bioinformatics ML Platform v1.0",
        "author":    "Rosemary James",
        "models":    list(SERVICES.keys()),
        "status":    "healthy",
        "uptime":    metrics["start_time"],
    }

@app.get("/health")
async def health():
    """Check health of all downstream services"""
    results = {}
    async with httpx.AsyncClient(timeout=3.0) as client:
        for name, url in SERVICES.items():
            try:
                r = await client.get(f"{url}/")
                results[name] = "healthy" if r.status_code == 200 else "degraded"
            except:
                results[name] = "unreachable"
    return {"gateway": "healthy", "services": results}

@app.get("/metrics")
def get_metrics():
    """Prometheus-style metrics endpoint"""
    return {
        "total_requests":    metrics["total_requests"],
        "requests_by_model": metrics["requests_by_model"],
        "errors":            metrics["errors"],
        "uptime_since":      metrics["start_time"],
    }

# ── Model endpoints ─────────────────────────────────────────
@app.post("/v1/variant/predict")
async def predict_variant(req: VariantRequest):
    """Route to DNA variant pathogenicity classifier"""
    metrics["total_requests"] += 1
    metrics["requests_by_model"]["dna_classifier"] += 1
    start = time.time()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(
                f"{SERVICES['dna_classifier']}/predict",
                json=req.dict()
            )
            result = r.json()
            result["latency_ms"] = round((time.time() - start) * 1000, 2)
            result["model"]      = "dna_variant_classifier_v1"
            return result
        except Exception as e:
            metrics["errors"] += 1
            raise HTTPException(503, f"DNA classifier unavailable: {str(e)}")

@app.post("/v1/cell/predict")
async def predict_cell(req: CellRequest):
    """Route to scRNA-seq cell type classifier"""
    metrics["total_requests"] += 1
    metrics["requests_by_model"]["scrna_classifier"] += 1
    start = time.time()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(
                f"{SERVICES['scrna_classifier']}/predict",
                json=req.dict()
            )
            result = r.json()
            result["latency_ms"] = round((time.time() - start) * 1000, 2)
            result["model"]      = "scrna_classifier_v1"
            return result
        except Exception as e:
            metrics["errors"] += 1
            raise HTTPException(503, f"scRNA classifier unavailable: {str(e)}")

@app.post("/v1/molecule/predict")
async def predict_molecule(req: MoleculeRequest):
    """Route to drug toxicity predictor"""
    metrics["total_requests"] += 1
    metrics["requests_by_model"]["drug_toxicity"] += 1
    start = time.time()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(
                f"{SERVICES['drug_toxicity']}/predict",
                json=req.dict()
            )
            result = r.json()
            result["latency_ms"] = round((time.time() - start) * 1000, 2)
            result["model"]      = "drug_toxicity_v1"
            return result
        except Exception as e:
            metrics["errors"] += 1
            raise HTTPException(503, f"Drug toxicity predictor unavailable: {str(e)}")

@app.post("/v1/analyze/full")
async def full_analysis(
    variant: Optional[VariantRequest] = None,
    molecule: Optional[MoleculeRequest] = None
):
    """Run multiple models in parallel — the platform's superpower"""
    results = {}
    metrics["total_requests"] += 1

    async with httpx.AsyncClient(timeout=30.0) as client:
        if variant:
            try:
                r = await client.post(
                    f"{SERVICES['dna_classifier']}/predict",
                    json=variant.dict()
                )
                results["variant_analysis"] = r.json()
            except:
                results["variant_analysis"] = {"error": "unavailable"}

        if molecule:
            try:
                r = await client.post(
                    f"{SERVICES['drug_toxicity']}/predict",
                    json=molecule.dict()
                )
                results["toxicity_analysis"] = r.json()
            except:
                results["toxicity_analysis"] = {"error": "unavailable"}

    results["platform"] = "bioinformatics-ml-platform-v1"
    results["timestamp"] = datetime.utcnow().isoformat()
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
