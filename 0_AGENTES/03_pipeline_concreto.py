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
    Agente de Síntesis y Deducciones Paso a Paso (Extractor y Escritor).
    Coordina la extracción de fórmulas y conceptos clave, y redacta una síntesis fluida
    con la inserción automática de deducciones algebraicas completas en notas.
    """
    # Cargar las instrucciones del agente desde el archivo .md correspondiente de manera dinámica.
    # Si el usuario o agente edita el archivo .md, el comportamiento del .py se actualizará automáticamente.
    prompt_file_path = Path(__file__).resolve().parent / "03_pipeline_concreto.md"
    try:
        with open(prompt_file_path, "r", encoding="utf-8") as pf:
            system_instructions = pf.read()
    except Exception as e:
        print(f"Error al cargar las instrucciones del sistema desde {prompt_file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = f"""
{system_instructions}

---
Aquí está la sección a procesar:

# {section_title}

{section_body}
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
