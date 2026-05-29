"""
Agente de Conversión e Inyección en Anki (Anki Bridge).
Parsea el Markdown de estudio, extrae las fichas (Active Recall), las formatea a HTML/MathJax
y las inserta directamente en los submazos correctos mediante la API de AnkiConnect.
"""
import re
import os

def markdown_to_anki(md_path, out_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the questions section (Active Recall)
    # We want to match:
    # <number>. **Question**
    # <details>
    # <summary>Ver Respuesta</summary>
    # Answer content
    # </details>
    
    # Let's use a regex to extract questions and answers.
    # Questions start with a number like "1. **...**" and end with "</details>"
    pattern = r'(\d+)\.\s+\*\*(.*?)\*\*\s*\n\s*<details>\s*\n\s*<summary>Ver Respuesta</summary>(.*?)</details>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    anki_lines = []
    
    for num, question, answer in matches:
        # Clean up question and answer
        question = question.strip()
        answer = answer.strip()
        
        # Convert markdown newlines to HTML <br> for Anki cards
        # Anki import file format can be tab-separated, with fields containing HTML.
        # We should also convert Markdown bold/italic to HTML, or keep them if Anki parses basic markdown (Anki imports HTML natively).
        # Let's convert basic markdown elements in both question and answer:
        # **text** -> <b>text</b>
        # *text* -> <i>text</i>
        # Lists: * or - at start of line -> Bullet points
        
        def md_to_html(text):
            # Convert LaTeX:
            # Inline math: $...$ -> \(...\)
            # Block math: $$...$$ -> \[...\]
            # Note: Do block math first to avoid conflicting with inline math.
            text = re.sub(r'\$\$(.*?)\$\$', r'\[\1\]', text, flags=re.DOTALL)
            text = re.sub(r'\$(.*?)\$', r'\(\1\)', text)
            
            # Convert bold/italic
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            
            # Replace newlines with <br>
            lines = text.split('\n')
            html_lines = []
            in_list = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('* ') or stripped.startswith('- '):
                    if not in_list:
                        html_lines.append('<ul>')
                        in_list = True
                    html_lines.append(f'<li>{stripped[2:]}</li>')
                elif stripped.startswith('1. ') or stripped.startswith('2. ') or stripped.startswith('3. ') or stripped.startswith('4. ') or stripped.startswith('5. ') or stripped.startswith('6. ') or stripped.startswith('7. ') or stripped.startswith('8. ') or stripped.startswith('9. ') or stripped.startswith('10. '):
                    # Simple ordered list item
                    if not in_list:
                        html_lines.append('<ol>')
                        in_list = True
                    # Find dot index
                    dot_idx = stripped.find('.')
                    html_lines.append(f'<li>{stripped[dot_idx+1:].strip()}</li>')
                else:
                    if in_list:
                        html_lines.append('</ul>') # Close list (simplified)
                        in_list = False
                    html_lines.append(line)
            if in_list:
                html_lines.append('</ul>')
            
            html_text = '<br>'.join(html_lines)
            # Replace multiple consecutive <br> with single or double
            html_text = re.sub(r'(<br>\s*){3,}', '<br><br>', html_text)
            return html_text
            
        # Route deck based on question number (from our MEMORIA_ANKI structure)
        q_num = int(num)
        if q_num in [1, 2, 3, 4, 5, 7]:
            target_deck = "SciDoc::01_Conceptos_Teoricos"
        elif q_num in [6, 8, 9, 10, 11, 12]:
            target_deck = "SciDoc::02_Matematicas_Fisica"
        else:
            target_deck = "SciDoc::03_Problemas_Practicos"
            
        q_html = md_to_html(question)
        a_html = md_to_html(answer)
        
        # Escape tabs and double quotes for TSV/CSV format.
        # Tab-separated values is the simplest format for Anki.
        # If we use tabs, we must not have tabs inside fields.
        q_html = q_html.replace('\t', ' ').replace('\n', ' ')
        a_html = a_html.replace('\t', ' ').replace('\n', ' ')
        
        anki_lines.append((target_deck, q_html, a_html))
        
    # Write to target file for manual import fallback
    with open(out_path, 'w', encoding='utf-8') as f:
        # Header for Anki to recognize HTML and format
        f.write("#separator:tab\n#html:true\n")
        for deck, q, a in anki_lines:
            f.write(f"{q}\t{a}\t{deck}\n")
            
    print(f"Generated {len(anki_lines)} flashcards at: {out_path}")
    
    # --- AnkiConnect Sync Integration ---
    import json
    import urllib.request
    
    def request_anki(action, params=None):
        payload = {"action": action, "version": 6}
        if params:
            payload["params"] = params
        try:
            req = urllib.request.Request(
                "http://localhost:8765",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=3) as res:
                response = json.loads(res.read().decode("utf-8"))
                if response.get("error"):
                    print(f"AnkiConnect Error: {response['error']}")
                    return None
                return response.get("result")
        except Exception:
            return None

    print("\nAttempting to connect to Anki via AnkiConnect...")
    anki_version = request_anki("version")
    if anki_version is None:
        print("Anki is not running or AnkiConnect add-on is not installed.")
        print("To enable automatic sync:")
        print("1. Open Anki.")
        print("2. Install 'AnkiConnect' add-on (Code: 2055492159).")
        print("3. Restart Anki. Run this script again to sync automatically.")
        return
        
    print(f"Connected to Anki (Version: {anki_version})! Creating decks...")
    
    # Get available models/note types (standard is 'Básico' or 'Basic')
    models = request_anki("modelNames") or []
    model_name = "Básico"
    if "Básico" not in models and "Basic" in models:
        model_name = "Basic"
    
    # Map field names for model
    fields = ["Anverso", "Reverso"]
    if model_name == "Basic":
        fields = ["Front", "Back"]

    # Process and sync cards
    notes = []
    for deck, q, a in anki_lines:
        # Create deck if it doesn't exist
        request_anki("createDeck", {"deck": deck})
        
        notes.append({
            "deckName": deck,
            "modelName": model_name,
            "fields": {
                fields[0]: q,
                fields[1]: a
            },
            "tags": ["scidoc"]
        })
        
    print(f"Syncing {len(notes)} notes...")
    added_notes = request_anki("addNotes", {"notes": notes})
    if added_notes:
        print(f"Successfully synced {len(added_notes)} cards directly into Anki!")
    else:
        print("Failed to add some notes (they might already exist).")

if __name__ == "__main__":
    from pathlib import Path
    project_root = Path(__file__).resolve().parent.parent
    md_file = str(project_root / "4_APRENDER" / "1.es.aprender.md")
    out_file = str(project_root / "4_APRENDER" / "fichas_anki.txt")
    markdown_to_anki(md_file, out_file)
