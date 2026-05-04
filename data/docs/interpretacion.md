# Guía de Interpretación de Resultados

## ¿Cómo interpretar una predicción de ventas?

Cuando el agente te da una predicción como:
"Predicción para Tienda 1, Depto 3, Semana 20: $25,876.90 USD"

Esto significa que el modelo estima que esa tienda y departamento 
específico generará aproximadamente $25,876.90 USD en ventas durante 
esa semana. 

### Factores que pueden afectar la predicción:

- **Semanas con festivos** — las ventas pueden ser 15-30% más altas
- **MarkDowns activos** — los descuentos pueden incrementar ventas 10-20%
- **Temporada** — Q4 (octubre-diciembre) históricamente tiene las ventas más altas
- **Tipo de tienda** — tiendas tipo A tienen mayor volumen que B y C

## ¿Cómo interpretar el cluster de una tienda?

### Si la tienda está en Cluster 0:
- Es una tienda de alto rendimiento
- Requiere estrategias agresivas de reabastecimiento
- Responde bien a promociones — vale la pena invertir en MarkDowns
- Monitorear de cerca en temporadas altas para evitar desabasto

### Si la tienda está en Cluster 1:
- Es una tienda de rendimiento estable
- Inventario más predecible — menor riesgo de desabasto
- Menor respuesta a promociones — evaluar ROI antes de invertir en MarkDowns
- Enfocarse en lealtad de clientela local

## Preguntas frecuentes

**¿Con qué frecuencia se actualizan las predicciones?**
El modelo se reentrena automáticamente cada vez que hay cambios en 
el código via GitHub Actions.

**¿Qué hago si la predicción parece incorrecta?**
Verificar que los parámetros de entrada sean correctos — tienda, 
departamento y semana. Si el error persiste, puede ser señal de 
model drift y se debe notificar al equipo técnico.

**¿Puedo pedir predicciones para semanas futuras?**
Sí — el modelo puede predecir cualquier semana del año (1-52) 
para cualquier combinación de tienda y departamento.