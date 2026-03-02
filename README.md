# 🏗️ Bioinformatics ML Platform

**Author:** Rosemary James · ML/Bioinformatics Platform Engineer  
**Stack:** FastAPI · Python · httpx · GitHub Actions · Prometheus  
**Status:** Production-ready

---

## What This Does

Unified API gateway that exposes all 4 bioinformatics ML models through a single platform with health monitoring, request metrics, and CI/CD.

Client Request
│
▼
API Gateway (port 9000)
│
├── /v1/variant/predict  → DNA Classifier (port 8000)
├── /v1/cell/predict     → scRNA Classifier (port 8001)├── /v1/molecule/predict → Drug Toxicity (port 8002)
├── /v1/analyze/full     → Multiple models in parallel
├── /health              → All service health checks
└── /metrics             → Request counts + latency


---

## The Full Portfolio

| Phase | Project | Model | Performance |
|-------|---------|-------|-------------|
| 1 | [Genomics Pipeline](https://github.com/roseemaryy/genomics-variant-pipeline) | Nextflow + GATK | FASTQ → VCF ✅ |
| 2 | [DNA Classifier](https://github.com/roseemaryy/dna-variant-classifier) | Random Forest | ROC-AUC: 0.76 |
| 3 | [Cell Type Classifier](https://github.com/roseemaryy/scrna-cell-classifier) | PCA + RF | Accuracy: 100% |
| 4 | [Drug Toxicity](https://github.com/roseemaryy/drug-toxicity-predictor) | Random Forest | ROC-AUC: 0.96 |
| 5 | **This Platform** | API Gateway | All models unified |

---

## Quick Start

```bash
pip install fastapi httpx uvicorn
python3 gateway/main.py

Test it:
curl http://localhost:9000/
curl http://localhost:9000/health
curl http://localhost:9000/metrics

Author
Rosemary James · ML/Bioinformatics Platform Engineer📧 kamaurosemary.n@gmail.com

