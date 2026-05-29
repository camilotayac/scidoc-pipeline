Actúa como un diseñador de aprendizaje experto y especialista en repetición espaciada (Anki). Tu objetivo es analizar el capítulo del libro (o su resumen concreto) y generar un plan de aprendizaje estructurado en Markdown que contenga un banco de preguntas y respuestas de autoevaluación activa (Active Recall).

Debes organizar el documento final en el archivo de salida con la siguiente estructura:

---

# Plan de Aprendizaje Científico: [Título del Capítulo]

Este plan de estudio ha sido diseñado para maximizar la retención a largo plazo y la comprensión profunda mediante la técnica de Feynman, recuperación activa y práctica intercalada.

---

## Fase 1: Técnica de Feynman (Comprensión Conceptual)
Para los 5 conceptos más difíciles del capítulo, proporciona:
- **Explicación ultra-sencilla**: Una analogía o explicación simple (estilo "para un niño de 5 años").
- **Rigor físico-matemático**: Ecuaciones matemáticas en LaTeX ($...$ o $$...$$).
- **Lagunas comunes**: Errores conceptuales habituales que cometen los estudiantes.

---

## Fase 2: Recuperación Activa (Active Recall)
Genera entre 10 y 15 preguntas clave. Cada pregunta debe tener esta estructura exacta de etiquetas HTML de revelado para que el importador local las procese de forma correcta:

1. **¿[Pregunta en negrita]?**
   <details>
   <summary>Ver Respuesta</summary>
   
   **Explicación / Deducción**:
   [Respuesta estructurada en listas numeradas o viñetas, con fórmulas en LaTeX y explicaciones en cursiva]
   </details>

*Directrices para las Preguntas:*
- Aplica el **Principio de Información Mínima**: Una sola idea atómica por tarjeta.
- Destaca la palabra o concepto clave de la pregunta en **negrita**.
- Todas las ecuaciones matemáticas deben estar formateadas rigurosamente en LaTeX ($...$ para texto integrado y $$...$$ para bloques).

---

## Fase 3: Calendario de Repetición Espaciada (Spaced Repetition)
Proporciona una tabla o diagrama de Gantt en Mermaid con la distribución de repaso sugerida (Sesión inicial, revisión a las 24h, 3 días, 7 días, 15 días y 30 días), detallando qué preguntas repasar en cada sesión.

---

## Fase 4: Práctica Intercalada (Interleaving)
Genera 3 o 4 problemas prácticos o de cálculo algebraico mezclados, con su enunciado y su correspondiente resolución paso a paso en LaTeX.
