import os
# Force Docling to use CPU to avoid Apple Silicon (MPS) float64 tensor issues
os.environ["DOCLING_DEVICE"] = "cpu"

import sys
from pathlib import Path
import click

@click.command()
@click.option("--pdf", "-p", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False), help="Path to the English PDF book chapter.")
@click.option("--out-dir", "-o", type=click.Path(file_okay=False, dir_okay=True), default=None, help="Output directory for generated files (defaults to the same directory as the PDF).")
def main(pdf, out_dir):
    """
    Transcription stage of the Book Translation Pipeline.
    Converts PDF to Markdown using docling.
    The subsequent translation and analysis are orchestrated by the AI agent system.
    """
    pdf_path = Path(pdf).resolve()
    base_name = pdf_path.stem
    
    # Resolve output directory
    if out_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(out_dir).resolve()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    transcribed_md_path = output_dir / f"{base_name}.md"
    click.secho("\n--- Stage 1: Transcribing PDF using Docling ---", fg="cyan", bold=True)
    click.echo(f"Source PDF: {pdf_path}")
    click.echo(f"Transcribed Markdown Output: {transcribed_md_path}")
    
    try:
        from docling.document_converter import DocumentConverter
        click.echo("Initializing DocumentConverter (this may download models on first run)...")
        converter = DocumentConverter()
        
        click.echo("Converting PDF to Markdown...")
        result = converter.convert(pdf_path)
        md_text = result.document.export_to_markdown()
        
        with open(transcribed_md_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        click.secho("Transcription completed successfully!", fg="green")
        click.echo(f"Saved to: {transcribed_md_path}")
        
        # --- Automatic Language Detection Heuristic ---
        # Look for common stop words in Spanish vs English
        sample = md_text.lower()
        es_words = [" el ", " la ", " de ", " que ", " en ", " los ", " las ", " un ", " una ", " con ", " por ", " para ", " es ", " del "]
        en_words = [" the ", " of ", " and ", " to ", " a ", " in ", " for ", " is ", " on ", " that ", " by ", " this ", " with ", " as "]
        
        es_count = sum(sample.count(word) for word in es_words)
        en_count = sum(sample.count(word) for word in en_words)
        
        click.echo(f"Language detection metrics - Spanish indicators: {es_count}, English indicators: {en_count}")
        
        if es_count > en_count:
            click.secho("Detected Language: SPANISH. Auto-skipping translation stage.", fg="yellow", bold=True)
            # Define 2_TRADUCCIONES path
            traducciones_dir = pdf_path.parents[1] / "2_TRADUCCIONES"
            traducciones_dir.mkdir(parents=True, exist_ok=True)
            translated_path = traducciones_dir / f"{base_name}.es.md"
            
            import shutil
            shutil.copy(transcribed_md_path, translated_path)
            click.secho(f"Copied transcription directly as translation draft to: {translated_path}", fg="green")
        else:
            click.secho("Detected Language: ENGLISH (or other). Translation is required.", fg="cyan")
            
    except Exception as e:
        click.secho(f"Error during transcription stage: {e}", fg="red", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
