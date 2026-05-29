# Reglas de Diseño para Fichas de Anki (Active Recall)

Este documento define el estándar científico y de formato para la creación de preguntas y respuestas (tarjetas de estudio) del proyecto. Cualquier agente que genere fichas debe seguir estas pautas estrictamente para optimizar la retención a largo plazo.

---

## 1. Reglas de Estructura y Contenido

### 💡 Principio de Información Mínima (Atomicidad)
* **Regla**: Cada tarjeta debe abordar **una sola pregunta concreta** o un único concepto atómico. 
* *Evitar*: Tarjetas con respuestas kilométricas o múltiples incisos inconexos. Si un concepto es complejo, divídelo en varias preguntas consecutivas (ej. "Deducción parte 1", "Deducción parte 2").

### 🎯 Claridad del Enunciado (Pregunta)
* El enunciado debe ser inequívoco. Usa la **negrita** para resaltar la variable física, constante o concepto central sobre el que se pregunta.
* *Ejemplo*: "¿Cuál es la **longitud de onda de de Broglie** asociada a una partícula de momento lineal $p$?"

### 📝 Respuestas Estructuradas
* Las respuestas deben estar organizadas con **listas ordenadas (`1.`, `2.`)** para pasos secuenciales, o **viñetas (`*`)** para características sueltas. Esto facilita la memorización por bloques de información (chunking).

---

## 2. Reglas de Formato Técnico (LaTeX y HTML)

### 🔢 Notación Matemática y Científica
* **Fórmulas matemáticas/químicas**: Deben ir obligatoriamente en LaTeX.
* En el archivo de texto o Markdown base, usa:
  * `$ ... $` para fórmulas integradas en el texto (inline).
  * `$$ ... $$` para ecuaciones en bloque centrado.
* El script `04_conversor_anki.py` se encargará de traducir estos símbolos al formato nativo MathJax de Anki (`\(...\)` y `\[...\]`).

### 🏷️ Etiquetas HTML Permitidas
Anki lee HTML nativo. Para destacar elementos en las respuestas, se prefiere:
* `<b>texto</b>` para negritas importantes.
* `<i>texto</i>` para explicaciones complementarias o analogías de Feynman.
* `<br>` para saltos de línea (nunca uses tabulaciones dentro del campo, ya que rompen el archivo de importación).

---

## 3. Clasificación y Enrutamiento de Mazos

Las tarjetas deben ser clasificadas en base a su carga conceptual y matemática:

| Tipo de Pregunta | Submazo de Destino | Ejemplo |
|---|---|---|
| Definiciones conceptuales, interpretación de funciones físicas, principios teóricos. | `01_Ecuación_Schrödinger` | Interpretación de Born de $\Psi$. |
| Constantes fundamentales, operaciones complejas, deducciones algebraicas. | `02_Matemáticas_Física` | Separación de variables, fórmula de Euler. |
| Problemas de cálculo numérico, normalización de integrales y aplicación práctica. | `03_Problemas_Prácticos` | Calcular probabilidad en el intervalo $[0, L]$. |
