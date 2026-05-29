import os
import sys
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load env variables from .env if present
load_dotenv()

def generate_concept_guide(input_md_path: str, output_md_path: str, model_name: str = "gemini-2.5-pro"):
    """
    Reads a translated Markdown file, sends it to Gemini to analyze and evaluate 
    difficult/advanced concepts, and writes the explanatory guide to the output path.
    """
    # Ensure API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please add GEMINI_API_KEY to your environment or .env file.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading translated file: {input_md_path}")
    try:
        with open(input_md_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {input_md_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if not content.strip():
        print("Error: Translated file is empty. Nothing to analyze.", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing Gemini client and using model: {model_name}...")
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing Gemini client: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = f"""
Actúa como un profesor experto y científico de datos. Tu tarea es analizar la siguiente traducción de un capítulo de libro e identificar todos los conceptos que sean difíciles, avanzados, técnicos o matemáticos que un estudiante o profesional promedio podría encontrar complicados.

Para cada uno de estos conceptos identificados, debes generar una explicación detallada estructurada de la siguiente manera:

---
### 📘 [Nombre del Concepto]
- **Ubicación/Contexto en el texto**: Breve descripción o cita de dónde o cómo se menciona en el texto.
- **¿Por qué es difícil/avanzado?**: Explica brevemente qué hace que este concepto sea complejo o requiera prerrequisitos.
- **Explicación Sencilla (Intuición)**: Una explicación para principiantes (estilo "Explain Like I'm 5" o analogía cotidiana) para entender el núcleo de la idea sin tecnicismos complejos.
- **Explicación Profunda y Técnica**: Un análisis técnico detallado. Si aplica, incluye fórmulas matemáticas (en formato LaTeX de markdown), algoritmos, diagramas conceptuales representados con texto o código, y detalles arquitectónicos o teóricos clave.
---

Por favor, genera la respuesta directamente en formato Markdown en español. No agregues texto introductorio ni de cierre innecesario, ve directo al grano para que el documento resultante sea una guía de acompañamiento limpia y estructurada.

Aquí está el texto traducido del capítulo:

{content}
"""

    print("Sending content to Gemini for analysis (this might take a minute depending on the chapter length)...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        guide_content = response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Writing concept guide to: {output_md_path}")
    try:
        # Create parent directories if they don't exist
        Path(output_md_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(guide_content)
        print("Concept guide generated successfully!")
    except Exception as e:
        print(f"Error writing concept guide to {output_md_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python 02_integrador_conceptos.py <input_translated_md> <output_guide_md> [model_name]")
        sys.exit(1)
    
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "gemini-2.5-pro"
    
    generate_concept_guide(in_path, out_path, model)
