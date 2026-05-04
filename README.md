# Walmart Retail Intelligence — Azure AI + MLOps End-to-End Demo

> Caso de uso retail que demuestra un sistema completo en Azure: ingesta con ADF, entrenamiento de modelos con Azure Machine Learning, agente conversacional con Azure OpenAI + Semantic Kernel, y CI/CD con GitHub Actions.

**Autor:** José Felipe Castellot Del Razo

---

## El problema de negocio

Walmart opera miles de tiendas con datos históricos de ventas semanales por tienda y departamento, indicadores macroeconómicos (desempleo, CPI, precio de combustible) y eventos promocionales. Dos preguntas operativas recurrentes:

1. **¿Cuántas unidades vamos a vender la próxima semana por tienda/departamento?** → problema de predicción.
2. **¿Qué tiendas se comportan parecido entre sí y cuáles son atípicas?** → problema de segmentación.

Este repositorio construye ambas capacidades y las expone a través de un **agente conversacional** al que los gerentes de categoría pueden preguntarle en lenguaje natural.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USUARIO DE NEGOCIO                             │
│             "¿Qué tiendas de cluster 2 están en riesgo?"                │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│   AGENTE CONVERSACIONAL (Semantic Kernel + Azure OpenAI gpt-4o)         │
│   Plugins: ForecastPlugin, ClusterPlugin                                │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ (invoca plugins como herramientas)
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│             AZURE ML — Managed Online Endpoint                          │
│   Modelo de forecast (Random Forest) + modelo de clustering (KMeans)   │
└───────────────────────────────▲─────────────────────────────────────────┘
                                │ (entrenado por)
                                │
┌───────────────────────────────┴─────────────────────────────────────────┐
│             AZURE ML — Training Pipeline (SDK v2 / Python)              │
│   prep → train_forecast → train_clustering → register → deploy         │
└───────────────────────────────▲─────────────────────────────────────────┘
                                │ (disparado por)
                                │
┌───────────────────────────────┴─────────────────────────────────────────┐
│                  AZURE DATA FACTORY (ADF)                               │
│   Ingesta CSV → Blob Storage → invoca Azure ML pipeline                 │
└───────────────────────────────▲─────────────────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────────────────┐
│              GITHUB ACTIONS (CI/CD)                                     │
│   Push a main → lint → tests → trigger ADF → notifica                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Lenguaje principal | Python 3.11 |
| ML | scikit-learn, MLflow |
| Cloud ML | Azure Machine Learning (SDK v2) |
| Ingesta | Azure Data Factory + Azure Blob Storage |
| GenAI | Azure OpenAI Service (gpt-4o) |
| Orquestación de agentes | Semantic Kernel (Python) |
| Bot conversacional | Azure Bot Framework SDK |
| CI/CD | GitHub Actions |
| IaC | Azure CLI + YAML |
| Desarrollo | VS Code + asistentes de codificación con IA |

---

## Cómo reproducir

### Prerrequisitos

1. Cuenta Azure con suscripción activa (Free Trial $200 USD sirve)
2. Azure CLI instalado (`az --version` >= 2.50)
3. Python 3.11
4. Git + cuenta GitHub

### Setup

```bash
# 1. Clonar
git clone https://github.com/jfcastellot/walmart-ai-azure-demo.git
cd walmart-ai-azure-demo

# 2. Ambiente Python
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
pip install -r requirements.txt

# 3. Login a Azure
az login

# 4. Copiar config de ejemplo
cp config/.env.example config/.env
# Editar config/.env con tus valores

# 5. Crear infraestructura base
bash scripts/00_setup_infra.sh
```

### Ejecutar

```bash
# Entrenar modelos localmente (smoke test)
python -m src.ml.train_forecast
python -m src.ml.train_clustering

# Ejecutar pipeline completo en Azure ML
python pipelines/azureml/submit_pipeline.py

# Probar el agente
python -m src.agent.chat

# Arrancar el bot
python -m src.agent.app
```

---

## Progreso del desarrollo

- [x] Día 1: Azure Storage + dataset (421,570 filas · 3 CSV)
- [x] Día 2: Azure ML Pipeline + modelos forecast y clustering
- [x] Día 3: Model Registry con versionado y lineage
- [x] Día 4: Online Endpoint HTTPS + primera predicción validada
- [x] Día 5: CI/CD con GitHub Actions (CI + CT)
- [x] Día 6: Agente GenAI con Semantic Kernel + Azure OpenAI
- [x] Día 7: Bot Framework SDK + Bot Framework Emulator
- [ ] Día 8: Azure Data Factory pipeline
- [ ] Día 9: Azure AI Search + RAG
- [ ] Día 10: Pulido y pruebas finales

---

## Capacidades demostradas

- Modelos preentrenados en la nube → Azure OpenAI gpt-4o
- Entrenamiento de modelos ML → forecasting + clustering con scikit-learn
- Pipeline de datos → ADF + Azure ML + GitHub Actions
- MLOps end-to-end → training pipeline + registered model + managed endpoint + CI/CD
- LLMs y NLU → agente Semantic Kernel responde en español natural
- Canal conversacional → Azure Bot Framework SDK
- Búsqueda semántica → Azure AI Search + embeddings (próximamente)
- Ingeniería de prompts → ver `docs/prompt_engineering.md`
- Uso responsable de IA en desarrollo → ver `docs/development_process.md`

---

## Licencia

MIT — ver `LICENSE`.
