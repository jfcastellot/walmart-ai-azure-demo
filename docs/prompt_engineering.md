# Guía de Prompt Engineering — Proyecto Walmart AI

> Documento vivo que captura las prácticas de ingeniería de prompts aplicadas al agente conversacional de este proyecto.
> Alineado con RFP Walmart México & Centroamérica SEDSA v5.0, sección 2.2.10 ("Ingeniería de prompts").

## 1. Principios aplicados

### 1.1 Especificidad sobre brevedad
El prompt del sistema define rol, audiencia, idioma, estilo y herramientas disponibles explícitamente. Ejemplo del agente:

> "Eres un asistente analítico para gerentes de categoría de Walmart México. Respondes en español natural, de forma ejecutiva y concisa."

### 1.2 Herramientas sobre descripciones
En lugar de pedirle al LLM que "invente" predicciones, le damos plugins concretos (`ForecastPlugin`, `ClusterPlugin`) y dejamos que el modelo decida cuándo invocarlos. Esto reduce alucinaciones y garantiza trazabilidad.

### 1.3 Formato de salida definido
Los docstrings de cada `@kernel_function` especifican el formato de retorno. El LLM consume estos metadatos y aprende el contrato.

### 1.4 Guardrails de dominio
Instrucciones explícitas:
- "Siempre contextualiza los números con una interpretación de negocio breve"
- "Si necesitas múltiples datos, llama a varios plugins en secuencia"

## 2. Patrones de prompt por caso de uso

### 2.1 Predicciones puntuales
**Entrada del usuario:** "¿Cuánto se va a vender la próxima semana en el depto 5 de la tienda 10?"
**Estrategia:** el agente detecta entidades (tienda=10, depto=5, week=next) → invoca `predict_sales` → envuelve respuesta con interpretación.

### 2.2 Preguntas sobre segmentación
**Entrada:** "¿Qué tiendas son parecidas a la 4?"
**Estrategia:** `get_store_cluster(4)` → `stores_in_cluster(N)` → respuesta narrativa.

### 2.3 Preguntas abiertas de negocio
**Entrada:** "¿Dónde debería enfocar promociones este trimestre?"
**Estrategia:** prompt de planeación (chain-of-thought implícito) + múltiples invocaciones de plugins + síntesis.

## 3. Evaluación y mejora continua

- Cada iteración del prompt se versiona en Git (este archivo).
- Ejemplos de inputs típicos en `tests/test_agent_prompts.py` (fase 2).
- Métricas: tasa de invocación correcta de plugins, latencia, costo por respuesta.

## 4. Próximos pasos

- [ ] Few-shot examples para casos bordes (ventas negativas, datos faltantes)
- [ ] Guardrails contra preguntas fuera de dominio (PII, temas personales)
- [ ] Cache de respuestas frecuentes (semantic caching)
- [ ] Evaluación automática con prompt flow de Azure AI Foundry
