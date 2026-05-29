import os
import sys
import re
from pathlib import Path
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def process_section(section_title, section_body, client, model_name):
    """
    Simulates the two-stage process: extraction and rewriting.
    We instruct the model to first extract the core equations, figures, and concepts,
    and then rewrite the section as a highly fluid, scientifically rigorous, and concise summary.
    """
    prompt = f"""
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

Aquí está la sección a procesar:

# {section_title}

{section_body}

Genera directamente la salida del Agente Escritor en formato Markdown. No agregues introducciones ni comentarios adicionales del tipo "Aquí está tu resumen". Comienza directamente con el encabezado de la sección.
"""
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error procesando la sección con Gemini: {e}", file=sys.stderr)
        return None

def split_markdown_by_headings(content):
    """
    Splits the markdown content by Level 2 headings (##).
    """
    sections = []
    # Find all headings ## 
    pattern = r"^(##\s+.*)$"
    matches = list(re.finditer(pattern, content, re.MULTILINE))
    
    if not matches:
        return [("Capítulo", content)]
        
    # Add content before the first heading if any
    first_start = matches[0].start()
    preamble = content[:first_start].strip()
    if preamble:
        sections.append(("Introducción", preamble))
        
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        sections.append((title, body))
        
    return sections

def generate_concrete_version(input_path, output_path, model_name="gemini-2.5-pro"):
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
        
    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: El archivo de entrada no existe: {input_path}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Leyendo traducción desde: {input_path}")
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    sections = split_markdown_by_headings(content)
    print(f"Se encontraron {len(sections)} secciones para procesar.")
    
    client = genai.Client()
    concrete_sections = []
    
    for i, (title, body) in enumerate(sections):
        print(f"Procesando sección {i+1}/{len(sections)}: {title}...")
        result = process_section(title, body, client, model_name)
        if result:
            concrete_sections.append(result.strip())
        else:
            print(f"Advertencia: Falló el procesamiento de la sección {title}. Se omitirá.")
            
    # Combine sections
    combined_content = "\n\n".join(concrete_sections)
    
    # Save to output path
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(combined_content)
        
    print(f"\nDocumento concreto creado con éxito en: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python 03_pipeline_concreto.py <input_md> <output_md> [model_name]")
        sys.exit(1)
        
    in_md = sys.argv[1]
    out_md = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "gemini-2.5-pro"
    
    generate_concrete_version(in_md, out_md, model)
