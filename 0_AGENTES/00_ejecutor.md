# 00 — Ejecutor: Reglas del Proceso de Traducción

> Documento maestro que define todas las reglas, convenciones y flujo de trabajo para la traducción de capítulos de libros del **inglés al español científico**.  
> Cualquier agente o persona que participe en el proceso **debe seguir estrictamente** estas reglas.

---

## 1. Nomenclatura de Archivos y Carpetas

| Ruta/Archivo | Descripción |
|---|---|
| `0_AGENTES/` | Directorio que contiene los agentes, scripts y este archivo maestro de reglas |
| `1_CAPITULO/` | Directorio que contiene el PDF original, la transcripción original `.md` e imágenes |
| `2_TRADUCCIONES/` | Directorio de salida que contiene la traducción verificada al español científico |
| `1_CAPITULO/{N}.pdf` | Capítulo original en inglés (entrada) |
| `1_CAPITULO/{N}.md` | Transcripción estructurada del PDF a Markdown (Docling). **Se conserva siempre.** |
| `2_TRADUCCIONES/{N}.es.md` | Traducción final verificada al español científico con explicaciones integradas |
| `1_CAPITULO/{N}_images/` | Directorio con las imágenes extraídas del PDF (si aplica) |

> `{N}` es el número del capítulo: `1`, `2`, `3`, etc.

---

## 2. Flujo del Pipeline (4 Fases)

```
┌─────────────────────────────────────────────────────────┐
│  FASE 1: TRANSCRIPCIÓN (Docling)                        │
│  1.pdf  ──►  1.md  +  1_images/  (en 1_CAPITULO/)       │
├─────────────────────────────────────────────────────────┤
│  DETECCIÓN DE IDIOMA: ¿Está en español?                 │
│  SÍ: Omitir FASE 2. Copiar 1.md a borrador en español.  │
│  NO: Proceder a FASE 2 normalmente.                     │
├─────────────────────────────────────────────────────────┤
│  FASE 2: TRADUCCIÓN (Agente de Traducción)              │
│  1.md  ──►  chunks  ──►  borradores en español          │
├─────────────────────────────────────────────────────────┤
│  FASE 3: VERIFICACIÓN (Agente de Verificación)          │
│  borrador vs. original  ──►  correcciones               │
├─────────────────────────────────────────────────────────┤
│  FASE 4: INTEGRACIÓN DE CONCEPTOS (Agente de Conceptos) │
│  Explicaciones añadidas directamente en 1.es.md         │
│  concepto en **negrita** y explicación en (*cursiva*)    │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Fase 1 — Reglas de Transcripción

### Herramienta
- **Docling** (`docling-project/docling`) ejecutado con Python en el entorno `es_book_env`.

### Configuración obligatoria
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

pipeline_options = PdfPipelineOptions(
    do_formula_enrichment=True,   # OBLIGATORIO: activar OCR de fórmulas
)
```

### Reglas
1. **Forzar CPU** en Apple Silicon: establecer `DOCLING_DEVICE=cpu` antes de ejecutar.
2. **Fórmulas**: Docling debe intentar decodificar todas las fórmulas a LaTeX. Si alguna fórmula queda como `<!-- formula-not-decoded -->`, será corregida manualmente en la Fase 2.
3. **Imágenes**: Las figuras del PDF deben exportarse como archivos en `{N}_images/` y referenciarse en el `.md` con rutas relativas: `![Figura X](./1_images/imagen.png)`.
4. **Estructura**: Preservar la jerarquía de encabezados (`##`, `###`), listas, tablas y bloques del documento original.
5. **El archivo `{N}.md` se conserva siempre** como registro de la transcripción original. Nunca se elimina.

---

## 4. Fase 2 — Reglas de Traducción

### Agente
- **`translation_agent`**: Subagente especializado invocado por el orquestador.

### Reglas de Idioma y Estilo
0. **Detección de idioma previo**: Antes de iniciar la traducción, verificar si el texto transcrito `{N}.md` ya está escrito en español. Si está en español:
   - Se **omite** el proceso de traducción de la Fase 2.
   - El archivo `{N}.md` se copia directamente como el borrador en español para proceder a la verificación de formato (Fase 3) e integración de conceptos (Fase 4).
1. **Idioma objetivo**: Español científico-académico, como el usado en la literatura universitaria de habla hispana.
2. **No traducir**:
   - Nombres propios de personas (Schrödinger, Planck, Bohr, Heisenberg, etc.)
   - Títulos de libros y revistas
   - Acrónimos reconocidos internacionalmente (UV, SI, CV, etc.)
   - Símbolos y variables matemáticas
3. **Conceptos técnicos en **negrita****: Todo concepto científico, físico, químico o matemático fundamental debe quedar resaltado en **negrita** la primera vez que aparece y en cada mención relevante. Ejemplos:
   - **mecánica cuántica**, **función de onda**, **principio de incertidumbre**
   - **cuerpo negro**, **efecto fotoeléctrico**, **estados estacionarios**
   - **dualidad onda-partícula**, **ecuación de Schrödinger**
4. **Registro formal**: Usar tercera persona o impersonal. Evitar tuteo.
5. **Notas del traductor**: Si se requiere una aclaración de traducción, usar formato `[N. del T.: ...]` en línea. **Nunca** insertar comentarios o notas sueltas fuera de este formato.

### Reglas de Formato

#### Fórmulas Matemáticas, Físicas y Químicas
6. **Fórmulas inline**: Usar delimitadores `$...$` para ecuaciones dentro del texto.
   ```
   La energía del fotón es $E = h\nu$.
   ```
7. **Fórmulas en bloque**: Usar delimitadores `$$...$$` para ecuaciones numeradas o destacadas, en su propia línea:
   ```
   $$\lambda\nu = c \tag{1.1}$$
   ```
8. **Numeración de ecuaciones**: Conservar la numeración original del libro usando `\tag{N.M}`:
   ```
   $$E = h\nu \tag{1.2}$$
   ```
9. **Fórmulas y ecuaciones químicas**: Deben escribirse siempre utilizando formato LaTeX (`$...$`) para renderizar correctamente los subíndices, superíndices y elementos químicos, utilizando `\text{}` si es necesario para mantener la tipografía recta en los símbolos de los elementos (ej. `$\text{C}_2\text{F}_6$`, `$\text{C}_{48}\text{H}_{26}\text{F}_{24}\text{N}_8\text{O}_8$`).
10. **Fechas, años y cantidades**: Los años, fechas importantes o números asociados a magnitudes físicas y constantes que contengan exponentes o bases decimales (ej. `$1064\text{ nm}$`, `$10^{-13}\text{ s}$`, `$5 \times 10^6\text{ W}$`, `$\text{junio de } 1900$`) deben estar formateados en LaTeX para asegurar una correcta visualización científica y homogeneidad.
11. **Expresiones no decodificadas**: Si la transcripción tiene `<!-- formula-not-decoded -->`, el agente **debe**:
    - Leer el contexto circundante (texto antes y después del marcador)
    - Identificar la ecuación del libro que corresponde
    - Reemplazar el marcador con la fórmula LaTeX correcta en formato `$...$` o `$$...$$`
    - **Nunca** dejar marcadores `<!-- formula-not-decoded -->` en la salida final

#### Imágenes y Figuras
12. **Referencias a figuras**: Conservar las menciones a figuras como `Fig. 1.1`, `Fig. 1.2`, etc.
13. **Marcadores de imagen**: Si la transcripción tiene `<!-- image -->`, reemplazar con:
    ```
    ![Figura X.Y: Descripción breve](./N_images/nombre_archivo.png)
    ```
    Si no se tiene la imagen extraída, usar una descripción textual:
    ```
    > **Figura X.Y**: Descripción detallada del contenido de la figura.
    ```

#### Estructura del Documento
14. **Encabezados**: Conservar la jerarquía exacta del original (`##` para secciones principales, `###` para subsecciones).
15. **Tablas**: Conservar la estructura en formato Markdown.
16. **Listas**: Conservar numeración y viñetas del original.
17. **Citas y referencias bibliográficas**: Conservar el formato original (autor, revista, volumen, página, año).

---

## 5. Fase 3 — Reglas de Verificación

### Agente
- **`verification_agent`**: Subagente especializado que recibe el fragmento original en inglés y el borrador en español.

### Criterios de Verificación
1. **Completitud**: No debe faltar ninguna oración, párrafo, fórmula, referencia o dato del original.
2. **Precisión terminológica**: Los términos técnicos deben estar correctamente traducidos según el uso aceptado en la academia hispanohablante.
3. **Fórmulas**: Verificar que:
   - Todas las fórmulas matemáticas, físicas y químicas están en formato LaTeX (`$...$` o `$$...$$`)
   - No quedan marcadores `<!-- formula-not-decoded -->`
   - Las variables y constantes son correctas
   - La numeración `\tag{}` coincide con el original
4. **Cursivas**: Todos los conceptos técnicos clave deben estar en *cursiva*.
5. **Coherencia**: No hay cambios de sentido, omisiones ni adiciones que alteren el significado científico.
6. **Gramática y ortografía**: El texto debe ser gramaticalmente correcto en español.
7. **Formato**: Encabezados, tablas, listas y referencias deben coincidir con la estructura original.

---

## 6. Fase 4 — Reglas de Integración de Conceptos

### Agente
- **`concept_guide_agent`**: Analiza la traducción final completa.

### Reglas de Integración
1. **Sin archivos separados**: Las explicaciones adicionales no deben crearse en un archivo Markdown separado.
2. **Ubicación en el texto**: Deben integrarse directamente dentro del archivo `{N}.es.md` en los párrafos donde el concepto técnico aparece por primera vez.
3. **Formato en negrita y explicación en cursiva/paréntesis**: El concepto técnico debe ir en **negrita** y la explicación debe ir en *cursiva* y entre paréntesis inmediatamente después del término. Formato: `**concepto** (*explicación del concepto*)`.
4. Ejemplo: 
   - `...mediante el uso de la **mecánica cuántica** (*teoría física moderna fundamental que describe el comportamiento de la materia y de la radiación a escala atómica y subatómica, donde las magnitudes físicas toman valores discretos o cuantizados*).`
5. **Selección de conceptos**: Identificar los 10-20 conceptos más difíciles o avanzados del capítulo para realizar la integración.

---

## 7. Reglas Generales del Proceso

### Calidad
- **Cero marcadores residuales**: El archivo final `{N}.es.md` **nunca** debe contener `<!-- formula-not-decoded -->` ni `<!-- image -->`.
- **Validación por conteo**: Al finalizar, ejecutar:
  ```bash
  grep -c 'formula-not-decoded' 2_TRADUCCIONES/{N}.es.md   # Debe dar 0
  grep -c '<!-- image -->' 2_TRADUCCIONES/{N}.es.md        # Debe dar 0
  grep -c '\$' 2_TRADUCCIONES/{N}.es.md                    # Debe dar > 0
  ```

### Archivos que se Conservan
| Ruta/Archivo | ¿Se conserva? |
|---|---|
| `1_CAPITULO/{N}.pdf` | ✅ Siempre |
| `1_CAPITULO/{N}.md` | ✅ Siempre (transcripción original) |
| `2_TRADUCCIONES/{N}.es.md` | ✅ Siempre (traducción final con explicaciones) |
| `1_CAPITULO/{N}_images/` | ✅ Siempre (si existen imágenes) |

---

## 8. Checklist de Ejecución para un Nuevo Capítulo

```
□ 1. Colocar {N}.pdf en la carpeta 1_CAPITULO/
□ 2. Ejecutar transcripción: DOCLING_DEVICE=cpu python 0_AGENTES/01_transcriptor_pdf.py --pdf 1_CAPITULO/{N}.pdf
□ 3. Verificar que 1_CAPITULO/{N}.md se generó correctamente
□ 4. Contar fórmulas no decodificadas: grep -c 'formula-not-decoded' 1_CAPITULO/{N}.md
□ 5. Verificar idioma: ¿El archivo .md ya está en español?
     - Sí: Omitir paso 6. Copiar 1_CAPITULO/{N}.md directamente a 2_TRADUCCIONES/{N}.es.md (o borrador intermedio).
     - No: Continuar al paso 6.
□ 6. Ejecutar traducción por chunks con translation_agent
□ 7. Ejecutar verificación de cada chunk con verification_agent
□ 8. Ensamblar 2_TRADUCCIONES/{N}.es.md con todos los chunks verificados
□ 9. Integrar explicaciones adicionales de conceptos directamente en 2_TRADUCCIONES/{N}.es.md en cursiva y paréntesis
□ 10. Verificar cero marcadores residuales en 2_TRADUCCIONES/{N}.es.md
□ 11. Generar fichas de aprendizaje en 4_APRENDER/{N}.es.aprender.md y ejecutar `04_conversor_anki.py` para sincronizar con Anki.
□ 12. Generar libreta interactiva de Colab ejecutando: `python 0_AGENTES/05_generador_colab.py 3_CONCRETO/{N}.concreto.md 5_COLAB/{N}_tutorial.ipynb`.
□ 13. Limpieza: eliminar archivos temporales, conservar los permanentes en sus carpetas respectivas
```

---

## 9. Referencia Rápida de Formato LaTeX en Markdown

### Inline (dentro del texto)
```
La constante de Planck es $h = 6.626 \times 10^{-34}\,\text{J·s}$.
```

### Bloque (ecuación centrada)
```
$$E = h\nu \tag{1.2}$$
```

### Ejemplos comunes en física y química cuántica

| Concepto | LaTeX |
|---|---|
| Fórmulas químicas rectas | `$\text{C}_2\text{F}_6$` o `$\text{C}_{48}\text{H}_{26}\text{F}_{24}\text{N}_8\text{O}_8$` |
| Años y fechas | `$\text{junio de } 1900$` |
| Unidades y cantidades | `$1064\text{ nm}$` o `$10^{-13}\text{ s}$` o `$5 \times 10^6\text{ W}$` |
| Relación de de Broglie | `$\lambda = \frac{h}{p}$` |
| Ecuación de Schrödinger (t-dep.) | `$i\hbar\frac{\partial\Psi}{\partial t} = -\frac{\hbar^2}{2m}\frac{\partial^2\Psi}{\partial x^2} + V\Psi$` |
| Ecuación de Schrödinger (t-indep.) | `$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V\psi = E\psi$` |
| Densidad de probabilidad | `$\|\Psi(x,t)\|^2\,dx$` |
| Normalización | `$\int_{-\infty}^{\infty}\|\Psi\|^2\,dx = 1$` |
| Energía del fotón | `$E = h\nu$` |
| Principio de incertidumbre | `$\Delta x\,\Delta p_x \approx h$` |
| Ley de Coulomb | `$F = \frac{Q_1 Q_2}{4\pi\varepsilon_0 r^2}$` |
| h-bar | `$\hbar = \frac{h}{2\pi}$` |
