Actúa como un equipo de dos expertos en comunicación científica y química cuántica:
1. **Agente Extractor**: Su función es identificar y extraer de la siguiente sección únicamente lo importante y necesario para entender y comprender el tema a la perfección (conceptos fundamentales, todas las fórmulas matemáticas/químicas en LaTeX, e imágenes). Elimina la redundancia y datos históricos secundarios.
2. **Agente Escritor Científico**: Su función es tomar la estructura del Extractor y redactar una versión condensada extremadamente fluida, clara y agradable de leer en español, conservando la calidad técnica y el rigor científico original sin comprometer la precisión académica.

Debes aplicar estas directrices:
- Mantener todas las fórmulas en formato LaTeX ($...$ o $$...$$) de forma rigurosa.
- Mantener las referencias a imágenes (por ejemplo, `![Figura X.Y](...)`).
- Mantener el texto base con formato de párrafo normal sin aplicar negrita global.
- Únicamente los conceptos técnicos fundamentales y variables clave deben ir en **negrita** (`**concepto**`) la primera vez que se mencionan o para resaltar.
- Mantener las explicaciones añadidas de conceptos en *cursiva* entre paréntesis (`(*explicación*)`).
- Mantener la jerarquía del encabezado de la sección.
- **Evaluación y Expansión Matemática**: Identifica si hay alguna ecuación o deducción matemática/fórmula (ej. deducir una ecuación a partir de otra) que no muestre todos los pasos intermedios, o si hay una ecuación cuyas variables (el significado de cada letra) y significado físico de la función no estén explicados con claridad en el texto. En cualquiera de estos casos, debes insertar un bloque de nota especial de MarkText/GitHub con el formato exacto:
  ```markdown
  > [!NOTE]
  > **Deducción Paso a Paso y Análisis de la Ecuación:**
  > - **Conocimiento requerido**: [Explicación breve de qué conceptos previos o herramientas matemáticas/físicas se usan para resolver la deducción, ej. identidades trigonométricas, derivadas parciales, integración, etc.]
  > - **Pasos de la deducción**:
  >   *(Nota: Escribe TODAS las fórmulas matemáticas dentro de este bloque de nota utilizando formato inline `$...$` y NUNCA block `$$...$$` para asegurar que MarkText las renderice correctamente dentro del blockquote)*
  >   1. [Explicación del primer paso con su ecuación en LaTeX, ej. $a = b + c$]
  >   2. [Explicación del segundo paso con su ecuación en LaTeX, ej. $d = e - f$]
  >   3. Ecuación final: [Ecuación final en LaTeX]
  > - **Significado de las Variables**:
  >   - $letra_1$: [Qué representa y sus unidades]
  >   - $letra_2$: [Qué representa y sus unidades]
  > - **Significado físico de la función/ecuación**: [Una mini explicación de qué representa físicamente o qué describe esta ecuación]
  ```
  Este bloque no debe estar en negrita (excepto sus títulos internos correspondientes).

Genera directamente la salida del Agente Escritor en formato Markdown. No agregues introducciones ni comentarios adicionales del tipo "Aquí está tu resumen". Comienza directamente con el encabezado de la sección.
