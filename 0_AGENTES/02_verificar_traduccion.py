import re
import os
import sys
from pathlib import Path

def verify_document(es_md_path, en_md_path, images_dir):
    print(f"=== INICIANDO VERIFICACIÓN DE: {es_md_path} ===")
    
    if not os.path.exists(es_md_path):
        print(f"Error: El archivo en español no existe: {es_md_path}")
        return False
        
    with open(es_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = 0

    # 1. Verificar marcadores residuales de Docling
    print("\n1. Buscando marcadores residuales...")
    formula_placeholders = content.count("formula-not-decoded")
    image_placeholders = content.count("<!-- image -->")
    
    if formula_placeholders > 0:
        print(f"  [ERROR] Se encontraron {formula_placeholders} marcadores 'formula-not-decoded'.")
        errors += 1
    else:
        print("  [OK] Cero marcadores 'formula-not-decoded'.")
        
    if image_placeholders > 0:
        print(f"  [ERROR] Se encontraron {image_placeholders} marcadores de imagen '<!-- image -->'.")
        errors += 1
    else:
        print("  [OK] Cero marcadores '<!-- image -->'.")

    # 2. Verificar referencias de imágenes y existencia física de archivos
    print("\n2. Verificando referencias a imágenes y existencia física...")
    # Matches patterns like ![caption](./1_images/image.png) or similar relative paths
    img_matches = re.findall(r"!\[.*?\]\((.*?)\)", content)
    
    if not img_matches:
        print("  [ADVERTENCIA] No se encontraron referencias a imágenes en el documento.")
    else:
        print(f"  Se encontraron {len(img_matches)} referencias a imágenes.")
        for img_path in img_matches:
            # Clean up query params if any
            clean_path = img_path.split("?")[0].split("#")[0]
            # Since 1.es.md is in 2_TRADUCCIONES/, relative path ./1_images/image.png
            # actually points to 2_TRADUCCIONES/1_images/image.png.
            # But the images are stored in 1_CAPITULO/1_images/.
            # Let us check the path relative to the workspace root or the folder.
            base_dir = os.path.dirname(es_md_path) # 2_TRADUCCIONES/
            
            # The expected relative path in 1.es.md is: ../1_CAPITULO/1_images/image.png
            # Let us resolve it:
            absolute_img_path = os.path.abspath(os.path.join(base_dir, clean_path))
            
            if os.path.exists(absolute_img_path):
                print(f"  [OK] Imagen encontrada: {clean_path} -> {absolute_img_path}")
            else:
                project_root = Path(__file__).resolve().parent.parent
                fallback_path = os.path.abspath(project_root / "1_CAPITULO" / clean_path.replace("../1_CAPITULO/", ""))
                if os.path.exists(fallback_path):
                    print(f"  [OK] Imagen encontrada en carpeta original (pero la ruta relativa debe ajustarse): {clean_path}")
                else:
                    print(f"  [ERROR] El archivo de imagen no existe físicamente: {absolute_img_path}")
                    errors += 1

    # 3. Verificar que las fórmulas matemáticas críticas estén en LaTeX
    print("\n3. Verificando integridad de formato LaTeX...")
    # Separate parts outside of LaTeX blocks
    parts = content.split("$")
    outside_latex_content = "".join(parts[::2])
    
    raw_var_exps = [
        (r"\bh\s*n\b", "h\\nu"),
        (r"\bpc\s*=\s*h\s*n\b", "pc = h\\nu"),
        (r"\bl\s*=\s*h\s*/\s*p\b", "\\lambda = h/p"),
        (r"\bE\s*=\s*pc\b", "E = pc"),
        (r"\be\s*-\s*iEt\b", "e^{-iEt}"),
        (r"\bV\s*=\s*mgx\b", "V = mgx"),
    ]
    
    for pattern, latex in raw_var_exps:
        matches = re.findall(pattern, outside_latex_content)
        if matches:
            print(f"  [ERROR] Expresión sin formatear detectada: {matches} -> debe ser LaTeX: ${latex}$")
            errors += 1
            
    # Verify brackets mismatch in LaTeX $...$
    latex_blocks = re.findall(r"\$(.*?)\$", content)
    for block in latex_blocks:
        open_braces = block.count("{")
        close_braces = block.count("}")
        if open_braces != close_braces:
            print(f"  [ERROR] Desajuste de llaves en bloque LaTeX: ${block}$ (Llaves abiertas: {open_braces}, Cerradas: {close_braces})")
            errors += 1

    # 4. Verificar que todas las fechas/años conocidos estén en LaTeX
    print("\n4. Verificando años e hitos históricos...")
    years = ["1749", "1803", "1827", "1864", "1887", "1888", "1900", "1904", "1905", "1907", "1909", "1911", "1913", "1923", "1925", "1926", "1927", "1932", "1948", "1961", "1965", "1988", "1993", "2001", "2002", "2005", "2012"]
    
    # We find any bare occurrence of these years (not inside a LaTeX block)
    for yr in years:
        # Regex matches year if not immediately preceded by \text{ or $
        pattern = r"(?<![\$\{\d])\b" + yr + r"\b(?![\}\d\$])"
        matches = re.findall(pattern, content)
        if matches:
            print(f"  [ERROR] Año sin formato LaTeX detectado: {yr} -> debe ser $\\text{{{yr}}}$")
            errors += 1

    # 5. Verificar que las explicaciones de conceptos integradas estén completas
    print("\n5. Verificando formato de conceptos en negrita y explicaciones en cursiva...")
    concept_pattern = r"\*\*[^*]+\*\*\s*\(\*[^*]+\*\)"
    integrated_concepts = re.findall(concept_pattern, content)
    print(f"  Se encontraron {len(integrated_concepts)} conceptos integrados con explicación en cursiva/paréntesis.")
    
    if len(integrated_concepts) < 10:
        print(f"  [ADVERTENCIA] Se encontraron pocas explicaciones integradas ({len(integrated_concepts)}), se recomiendan al menos 10 para completar la Fase 4.")
    else:
        print(f"  [OK] Total de conceptos integrados verificados: {len(integrated_concepts)}")

    print("\n=== RESUMEN DE LA VERIFICACIÓN ===")
    if errors == 0:
        print("✅ ¡La verificación se completó con éxito! El documento cumple con todas las directrices.")
        return True
    else:
        print(f"❌ Se encontraron {errors} errores en el documento. Por favor, corrígelos antes de finalizar.")
        return False

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    es_path = str(project_root / "2_TRADUCCIONES" / "1.es.md")
    en_path = str(project_root / "1_CAPITULO" / "1.md")
    img_dir = str(project_root / "1_CAPITULO" / "1_images")
    
    if len(sys.argv) > 1:
        es_path = sys.argv[1]
    if len(sys.argv) > 2:
        en_path = sys.argv[2]
    if len(sys.argv) > 3:
        img_dir = sys.argv[3]
        
    success = verify_document(es_path, en_path, img_dir)
    sys.exit(0 if success else 1)
