"""
Agente Generador de Colabs (Colab Generator).
Analiza el capítulo del libro en Markdown y genera automáticamente una libreta interactiva de
Jupyter (.ipynb) lista para Google Colab, que enseña a programar y graficar las ecuaciones.
"""
import os
import sys
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

def generate_colab_notebook(input_md_path: str, output_ipynb_path: str, model_name: str = "gemini-2.5-pro"):
    # Validar API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: La variable de entorno GEMINI_API_KEY no está configurada.", file=sys.stderr)
        sys.exit(1)

    # Leer el archivo Markdown de entrada
    print(f"Leyendo el contenido del capítulo: {input_md_path}")
    try:
        with open(input_md_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error al leer el archivo {input_md_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Cargar dinámicamente las instrucciones del agente desde el archivo .md
    prompt_file_path = Path(__file__).resolve().parent / "05_generador_colab.md"
    print(f"Cargando instrucciones del agente desde: {prompt_file_path}")
    try:
        with open(prompt_file_path, "r", encoding="utf-8") as pf:
            system_instructions = pf.read()
    except Exception as e:
        print(f"Error al cargar las instrucciones desde {prompt_file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Estructurar la petición para el modelo de IA
    prompt = f"""
{system_instructions}

---
Aquí está el contenido del capítulo sobre el cual debes crear la libreta interactiva de Jupyter:

{content}
"""

    print(f"Inicializando cliente de Gemini y llamando al modelo {model_name}...")
    try:
        client = genai.Client()
        # Forzar la respuesta en formato JSON estructurado
        config = types.GenerateContentConfig(
            response_mime_type="application/json"
        )
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config
        )
        
        # Validar y cargar el JSON devuelto
        notebook_data = json.loads(response.text.strip())
    except json.JSONDecodeError as e:
        print(f"Error: La respuesta de Gemini no es un JSON válido de Jupyter Notebook. {e}", file=sys.stderr)
        print("Respuesta cruda recibida:", file=sys.stderr)
        print(response.text if 'response' in locals() else "Sin respuesta", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error al conectar con la API de Gemini: {e}", file=sys.stderr)
        sys.exit(1)

    # Crear directorios padres de salida si no existen
    output_file = Path(output_ipynb_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Escribir la libreta Jupyter
    print(f"Guardando la libreta de Colab generada en: {output_ipynb_path}")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(notebook_data, f, indent=2, ensure_ascii=False)
        print("¡Libreta Jupyter (.ipynb) creada exitosamente y lista para Google Colab!")
    except Exception as e:
        print(f"Error al escribir la libreta en el disco: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python 05_generador_colab.py <input_md_path> <output_ipynb_path> [model_name]")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "gemini-2.5-pro"

    generate_colab_notebook(in_path, out_path, model)
