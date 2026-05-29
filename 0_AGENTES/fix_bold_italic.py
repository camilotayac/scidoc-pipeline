import re

def fix_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    terms = [
        "mecánica newtoniana",
        "mecánica estadística",
        "electrostática clásica",
        "probabilidad condicional",
        "números complejos",
        "número imaginario",
        "número imaginario puro",
        "módulo",
        "conjugado complejo",
        "mecánica estadística clásica",
        "ecuación de Schrödinger",
        "ecuaciones de Schrödinger",
        "función de densidad de probabilidad"
    ]
    
    new_content = content
    for term in terms:
        escaped = re.escape(term)
        # Match *term* but not **term** case-insensitively
        pattern = r"(?<!\*)\*(" + escaped + r")\*(?!\*)"
        new_content = re.sub(pattern, lambda m: f"**{m.group(1)}**", new_content, flags=re.IGNORECASE)

    # Fix (*funciones de onda*) to (**funciones de onda**)
    new_content = new_content.replace("(*funciones de onda*)", "(**funciones de onda**)")

    # Remove empty pipes | from the units section
    # Usually in the form of a line containing only a pipe or pipe with spaces/newlines
    new_content = re.sub(r"\n\s*\|\s*\n\s*\|\s*\n", "\n\n", new_content)
    # Also handle single standalone pipes if any
    new_content = re.sub(r"\n\s*\|\s*\n", "\n\n", new_content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Fixed specific formatting!")

if __name__ == "__main__":
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent
    fix_file(str(project_root / "2_TRADUCCIONES" / "1.es.md"))
