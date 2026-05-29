import re

def convert_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all concepts of the form *concept* (*explanation*) or **concept** (*explanation*)
    # The concept is in asterisks, followed by parentheses containing italics
    pattern = r"\*+([^*]+)\*+\s*\(\*([^*]+)\*\)"
    matches = re.findall(pattern, content)
    
    concepts = set()
    for concept, explanation in matches:
        concepts.add(concept.strip())
    
    print("Found concepts to bold:", concepts)
    
    # First, replace the defined concepts with their bold term and italic explanation
    # We use a lambda to avoid nested bolding or regex collision
    def repl_def(match):
        concept = match.group(1)
        explanation = match.group(2)
        return f"**{concept}** (*{explanation}*)"
        
    new_content = re.sub(pattern, repl_def, content)
    
    # Now, for each concept found, replace any other occurrence of *concept* with **concept**
    # matching case-insensitively but preserving original case.
    for concept in concepts:
        escaped = re.escape(concept)
        concept_pattern = r"(?<!\*)\*(" + escaped + r")\*(?!\*)"
        new_content = re.sub(concept_pattern, lambda m: f"**{m.group(1)}**", new_content, flags=re.IGNORECASE)
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Conversion completed!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python convert_formatting.py <file_path>")
        sys.exit(1)
    convert_file(sys.argv[1])
