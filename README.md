# Walmart Retail Intelligence — Azure AI + MLOps End-to-End Demo

> Caso de uso retail que demuestra un sistema completo en Azure: ingesta con ADF, entrenamiento de modelos con Azure Machine Learning, agente conversacional con Azure OpenAI + Semantic Kernel, y CI/CD con GitHub Actions.

**Autor:** José Felipe Fernández Medellín
**Contexto:** Demo técnica alineada con RFP Walmart México & Centroamérica (SEDSA v5.0), secciones 2.2.3 (IA/GenAI) y 2.2.10 (Ingeniería moderna).

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
│   AGENTE CONVERSACIONAL (Semantic Kernel + Azure OpenAI gpt-4o-mini)    │
│   Plugins: ForecastPlugin, ClusterPlugin, BusinessInsightPlugin         │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ (invoca plugins como herramientas)
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│             AZURE ML — Managed Online Endpoint                          │
│   Modelo de forecast (RandomForest/XGBoost) + modelo de clustering      │
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
| ML | scikit-learn, XGBoost, MLflow |
| Cloud ML | Azure Machine Learning (SDK v2) |
| Ingesta | Azure Data Factory + Azure Blob Storage |
| GenAI | Azure OpenAI Service (gpt-4o-mini) |
| Orquestación de agentes | Semantic Kernel (Python) |
| Bot conversacional | Azure Bot Framework SDK (fase 2) |
| CI/CD | GitHub Actions |
| IaC | Azure CLI + YAML |
| Desarrollo | VS Code + Claude Code como asistente |

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
git clone https://github.com/<tu-usuario>/walmart-ai-azure-demo.git
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
```

---

## Progreso del desarrollo

- [ ] Día 0 (jue): Setup ambiente, cuentas, dataset
- [ ] Día 1 (vie): Azure ML Workspace + notebook baseline + MLflow
- [ ] Día 2 (sáb): Pipeline SDK v2 + clustering + registro de modelo
- [ ] Día 3 (dom): Endpoint de inferencia + CI/CD GitHub Actions
- [ ] Día 4 (lun): Agente Semantic Kernel + Azure OpenAI + plugins
- [ ] Día 5 (mar): Demo al director
- [ ] Semana 2: ADF pipeline + Bot Framework + pulido
- [ ] Día 12 (jue 7-may): Entrevista formal

---

## Mapeo a requisitos RFP y perfil del proyecto

**Sección 2.2.3 RFP Walmart — Experiencia en IA y GenAI:**
- Modelos preentrenados en la nube → Azure OpenAI gpt-4o-mini
- Entrenar nuevos modelos ML → forecasting + clustering con scikit-learn
- Pipeline de datos con DataDevOps → ADF + Azure ML + GitHub Actions
- MLOps end-to-end → training pipeline + registered model + managed endpoint + CI/CD
- LLMs y NLU → agente Semantic Kernel responde en español natural
- Búsqueda semántica → opcional fase 2, Azure AI Search + embeddings
- Asistentes de codificación → Claude Code usado durante todo el desarrollo, documentado

**Sección 2.2.10 RFP Walmart — Ingeniería Moderna:**
- Ingeniería de prompts → ver `docs/prompt_engineering.md`
- Ingeniería de plataformas → todo este repo es un platform template
- Ingeniería de software verde → compute instances con auto-shutdown, modelos livianos

**Stack requerido por el proyecto:**
- Azure AI Foundry + Azure OpenAI Service ✅
- Semantic Kernel ✅
- Azure Bot Framework SDK → fase 2
- Agentic coding tools → Claude Code documentado en `docs/development_process.md`

---

## Licencia

MIT — ver `LICENSE`.
