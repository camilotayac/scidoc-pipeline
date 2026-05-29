import re

def bold_paragraph(text):
    # Find all explanations (*...*)
    # The pattern matches: (*explanation*)
    pattern = r"\(\*([^*]+)\*\)"
    
    parts = re.split(pattern, text)
    result_parts = []
    
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # This is normal text
            # Wrap it in **...** if it contains non-whitespace characters
            if part.strip():
                # Retain leading and trailing whitespaces outside the bold markers
                leading_space = part[:len(part) - len(part.lstrip())]
                trailing_space = part[len(part.rstrip()):]
                result_parts.append(f"{leading_space}**{part.strip()}**{trailing_space}")
            else:
                result_parts.append(part)
        else:
            # This is the explanation text (inside the parentheses)
            result_parts.append(f"(*{part}*)")
            
    return "".join(result_parts)

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # First, strip all double asterisks to start clean
    content = content.replace("**", "")

    # Split into lines
    lines = content.split("\n")
    new_lines = []
    
    in_math_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Track math blocks
        if stripped.startswith("$$"):
            in_math_block = not in_math_block
            new_lines.append(line)
            continue
            
        if in_math_block:
            new_lines.append(line)
            continue
            
        # Ignore headings, empty lines, images, tables lines, block math
        if (not stripped or 
            stripped.startswith("#") or 
            stripped.startswith("![") or 
            stripped.startswith("|") or
            stripped.startswith("$$")):
            new_lines.append(line)
            continue
            
        # Check if it is a list item
        list_match = re.match(r"^(\s*[-\*\+]\s+|\s*\d+\.\s+)(.*)$", line)
        if list_match:
            prefix = list_match.group(1)
            rest = list_match.group(2)
            bolded_rest = bold_paragraph(rest)
            new_lines.append(f"{prefix}{bolded_rest}")
        else:
            # Regular paragraph
            bolded_line = bold_paragraph(line)
            new_lines.append(bolded_line)
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
        
    print("Success bolding the base text!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python bold_base_text.py <file_path>")
        sys.exit(1)
    process_file(sys.argv[1])
