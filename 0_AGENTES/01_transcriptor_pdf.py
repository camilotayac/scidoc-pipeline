import os
# Se fuerza a Docling a usar CPU para evitar conflictos y problemas de precisión 
# de tensores float64 al ejecutarse en arquitecturas Apple Silicon (MPS).
os.environ["DOCLING_DEVICE"] = "cpu"

import sys
from pathlib import Path
import click

# Interfaz CLI amigable y parametrizada con la biblioteca Click
@click.command()
@click.option("--pdf", "-p", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False), help="Ruta al archivo PDF original del capítulo.")
@click.option("--out-dir", "-o", type=click.Path(file_okay=False, dir_okay=True), default=None, help="Directorio de salida (por defecto, la carpeta donde reside el PDF).")
def main(pdf, out_dir):
    """
    Agente Transcriptor y Detector de Idioma.
    Transcripción inicial del PDF a Markdown usando Docling y detección automática
    de idioma para omitir traducción si el documento original ya está en español.
    """
    pdf_path = Path(pdf).resolve()
    base_name = pdf_path.stem
    
    # Resolución del directorio de salida: si no se especifica, se usa el mismo directorio del PDF
    if out_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(out_dir).resolve()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    transcribed_md_path = output_dir / f"{base_name}.md"
    
    click.secho("\n--- Fase 1: Transcribiendo PDF usando Docling (Ejecutándose en CPU) ---", fg="cyan", bold=True)
    click.echo(f"PDF de Origen: {pdf_path}")
    click.echo(f"Destino de Transcripción: {transcribed_md_path}")
    
    try:
        # Importación diferida para agilizar la carga de la interfaz Click
        from docling.document_converter import DocumentConverter
        click.echo("Inicializando DocumentConverter de Docling (puede descargar modelos la primera vez)...")
        converter = DocumentConverter()
        
        click.echo("Convirtiendo PDF a formato Markdown...")
        result = converter.convert(pdf_path)
        md_text = result.document.export_to_markdown()
        
        # Guardar la transcripción Markdown original (se preserva siempre)
        with open(transcribed_md_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        click.secho("¡Transcripción completada con éxito!", fg="green")
        click.echo(f"Archivo guardado en: {transcribed_md_path}")
        
        # --- Heurística de Detección de Idioma Automática ---
        # Comparamos la frecuencia de artículos y conectores clave en español vs inglés.
        # Al ser local y basado en conteo, es 100% gratuito y no requiere llamadas a APIs de red.
        sample = md_text.lower()
        es_words = [" el ", " la ", " de ", " que ", " en ", " los ", " las ", " un ", " una ", " con ", " por ", " para ", " es ", " del "]
        en_words = [" the ", " of ", " and ", " to ", " a ", " in ", " for ", " is ", " on ", " that ", " by ", " this ", " with ", " as "]
        
        es_count = sum(sample.count(word) for word in es_words)
        en_count = sum(sample.count(word) for word in en_words)
        
        click.echo(f"Métricas de detección - Indicadores en Español: {es_count}, Indicadores en Inglés: {en_count}")
        
        if es_count > en_count:
            click.secho("Idioma Detectado: ESPAÑOL. Se omite la traducción (Fase 2).", fg="yellow", bold=True)
            
            # Calculamos dinámicamente la carpeta 2_TRADUCCIONES basándonos en la raíz del proyecto
            traducciones_dir = pdf_path.parents[1] / "2_TRADUCCIONES"
            traducciones_dir.mkdir(parents=True, exist_ok=True)
            translated_path = traducciones_dir / f"{base_name}.es.md"
            
            # Copiar directamente la transcripción como el borrador final traducido
            import shutil
            shutil.copy(transcribed_md_path, translated_path)
            click.secho(f"Copiado directamente al directorio de traducciones en: {translated_path}", fg="green")
        else:
            click.secho("Idioma Detectado: INGLÉS (u otro). Se requiere traducción manual/por agentes en el siguiente paso.", fg="cyan")
            
    except Exception as e:
        click.secho(f"Error en la etapa de transcripción: {e}", fg="red", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
