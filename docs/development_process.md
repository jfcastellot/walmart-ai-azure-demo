# Proceso de Desarrollo — Uso de Asistentes de Codificación con IA

> Documenta cómo se usaron herramientas de codificación asistida por IA (Claude, Claude Code, GitHub Copilot) durante la construcción de este proyecto.
> Alineado con RFP Walmart sección 2.2.3: "Experiencia en la construcción/uso de asistentes de codificación con IA para el desarrollo y pruebas de software".

## Herramientas usadas

| Herramienta | Uso | Nivel de automatización |
|-------------|-----|-------------------------|
| Claude (chat) | Diseño de arquitectura, decisiones técnicas, pair programming | Colaboración humano-IA |
| Claude Code | Refactorización, generación de tests, revisión de PRs | Agéntico (multi-file) |
| GitHub Copilot | Autocompletado en IDE | Sugerencias inline |

## Flujo de trabajo típico

1. **Especificación en lenguaje natural** — describo el componente o feature al asistente.
2. **Generación inicial** — el asistente produce código base.
3. **Revisión crítica humana** — valido correctitud, seguridad, alineación con estándares del equipo.
4. **Iteración** — refino con feedback específico hasta cumplir criterios de aceptación.
5. **Tests** — el asistente propone tests, yo valido cobertura.
6. **Commit** — mensaje de commit describe el cambio; PR detalla decisiones de diseño.

## Principios de uso responsable

1. **Revisión obligatoria** — ninguna línea generada por IA entra a main sin revisión humana.
2. **No filtración de secretos** — nunca se comparten credenciales, tokens, ni PII con los asistentes.
3. **Atribución** — en casos donde el asistente aportó lógica novedosa, se documenta en el PR.
4. **Trazabilidad** — las decisiones arquitectónicas clave se capturan en ADRs (Architecture Decision Records) independientemente de si provinieron del asistente.

## Métricas de productividad observadas

(A llenar al cierre del proyecto)

- Tiempo promedio de generación inicial de componente: ___
- % de código generado que entró sin modificaciones mayores: ___
- Defectos encontrados en código generado (post-merge): ___
