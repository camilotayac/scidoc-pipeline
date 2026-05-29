# 🧠 SciDoc Pipeline: Transcripción, Traducción y Aprendizaje de Libros Científicos

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/OCR-Docling-orange.svg" alt="OCR Docling">
  <img src="https://img.shields.io/badge/AI-Gemini%20Flash%20/%20Pro-purple.svg" alt="Gemini Models">
  <img src="https://img.shields.io/badge/Anki-Compatible-green.svg" alt="Anki Sync">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="License">
</p>

---

## 🎯 Objetivo del Proyecto

**SciDoc** es un pipeline automatizado y diseñado localmente para transformar capítulos de libros científicos complejos (física, química, biología, matemáticas, etc.) en recursos de aprendizaje de alto rendimiento. El objetivo principal es **eliminar la fricción entre la lectura técnica en inglés y la asimilación conceptual duradera**, automatizando la transcripción, traducción científica formal, simplificación matemática y la inyección directa de fichas de estudio a **Anki** con soporte LaTeX/MathJax integrado.

---

## 🌀 El Flujo del Pipeline (Arquitectura)

El sistema opera a través de un pipeline modular de 4 fases que procesa el contenido de forma secuencial y estructurada:

```mermaid
graph TD
    %% Estilos de Nodos
    classDef pdf fill:#FFD2D2,stroke:#FF5B5B,stroke-width:2px,color:#333;
    classDef phase fill:#D6EAF8,stroke:#3498DB,stroke-width:2px,color:#333;
    classDef folder fill:#EAFAF1,stroke:#2ECC71,stroke-width:2px,color:#333;
    classDef system fill:#F9E79F,stroke:#F1C40F,stroke-width:2px,color:#333;

    A[Capítulo original PDF] -->|Paso 1: Docling OCR| B(Fase 1: Transcripción)
    B -->|Genera .md original| C[1_CAPITULO/]
    
    C -->|Paso 2: LangDetect Heuristic| D{¿Está en Español?}
    
    D -->|No: Traducir con Gemini| E(Fase 2: Traducción y Verificación)
    D -->|Sí: Copiar borrador directamente| F[2_TRADUCCIONES/]
    E --> F
    
    F -->|Paso 3: Condensación y Paso-a-Paso| G(Fase 3: Síntesis y Rigor)
    G -->|Genera .concreto.md con Negrita Semántica| H[3_CONCRETO/]
    
    H -->|Paso 4: Didáctica de Feynman y Recall| I(Fase 4: Aprendizaje y Anki)
    I -->|Script 04_conversor_anki.py| J[4_APRENDER/]
    
    J -->|Sincronización AnkiConnect API| K[Anki Desktop Client 🎴]

    %% Aplicar Estilos
    class A pdf;
    class B,E,G,I phase;
    class C,F,H,J folder;
    class K system;
```

---

## ✨ Características Principales

| Característica | Descripción | Beneficio |
| :--- | :--- | :--- |
| **OCR Científico Nativo** | Integración con **IBM Docling** para extraer texto estructurado, tablas e imágenes de PDFs. | Respeta ecuaciones y no rompe el flujo lector. |
| **Filtro de Idioma Inteligente** | Algoritmo heurístico local que detecta si el documento original ya está en español. | Evita llamadas de API innecesarias y ahorra tiempo. |
| **Deducciones Paso a Paso** | Expande de manera automática las deducciones matemáticas incompletas agregando notas explicativas `[!NOTE]`. | Entendimiento completo del origen físico-matemático de cada ecuación. |
| **Directo a Anki (1-Click Sync)** | Integración nativa con la API de **AnkiConnect** para crear mazos, submazos y tarjetas automáticamente. | Cero importaciones manuales molestas de archivos CSV. |
| **MathJax Nativo en Anki** | Convierte ecuaciones de sintaxis Markdown estándar a delimitadores compatibles con Anki (`\(` y `\[`). | Visualización científica limpia y elegante de LaTeX en tus dispositivos de estudio. |

---

## 🚀 Configuración y Uso con Asistentes de IA (AI Agents)

Este repositorio está optimizado para una arquitectura **Agent-First**. No necesitas crear entornos virtuales de Python manualmente, ni realizar instalaciones o configuraciones complejas. Tu asistente de codificación favorito (**Antigravity CLI**, **OpenCode**, o **Claude Code**) se encargará de todo el trabajo técnico.

---

## 🛠️ Paso 1: Configuración Inicial (Vía tu Agente)

Abre la terminal en la carpeta de este proyecto, inicializa tu asistente de IA de preferencia y pídele lo siguiente:

> 🤖 **Prompt para el Agente**:  
> *"Instala los requerimientos de requirements.txt, asegúrate de que Python esté disponible y valida que mi API key de Gemini esté correctamente configurada desde el entorno local."*

El agente se encargará de validar tu versión de Python, instalar las dependencias requeridas y confirmar que las llaves estén listas para operar.

---

## 🎴 Paso 2: Configurar Anki (Sincronización Automática)

Para que el agente pueda inyectar las fichas directamente en tu aplicación de estudio:
1. Abre tu aplicación de **Anki** en tu computadora.
2. Ve al menú superior: **Herramientas ➔ Complementos (Tools ➔ Add-ons)**.
3. Haz clic en **Obtener complementos... (Get Add-ons...)**.
4. Pega el código de **AnkiConnect**: `2055492159`
5. Reinicia Anki.

---

## 📖 Paso 3: Uso Diario y Ejecución del Pipeline (Vía tu Agente)

Para procesar tus capítulos, solo debes colocar el PDF del libro (ej. `capitulo_1.pdf`) en la carpeta `1_CAPITULO/` y delegar las fases al agente usando estos comandos en lenguaje natural:

### Fases de Ejecución:

*   **Para transcribir y estructurar el PDF**:
    > 🤖 **Prompt**: *"Ejecuta la transcripción en 01_transcriptor_pdf.py para el PDF en 1_CAPITULO/capitulo_1.pdf y verifica el idioma detectado."*
    *(Nota: Si el agente detecta que el PDF ya está en español, omitirá automáticamente la Fase 2 de traducción).*
    
*   **Para traducir y realizar control de calidad**:
    > 🤖 **Prompt**: *"Traduce el capítulo transcrito, verifica que la sintaxis LaTeX sea correcta y que los conceptos técnicos clave queden destacados en negrita según las reglas de 00_ejecutor.md."*

*   **Para sintetizar el contenido y crear las fichas de estudio**:
    > 🤖 **Prompt**: *"Genera el resumen concreto en 3_CONCRETO/ y las fichas de aprendizaje en 4_APRENDER/ para este capítulo."*

*   **Para crear el tutorial interactivo de Google Colab (basado en el resumen concreto)**:
    > 🤖 **Prompt**: *"Ejecuta el script 05_generador_colab.py pasando como entrada el archivo resumido en 3_CONCRETO/1.concreto.md y guardando la libreta resultante en 5_COLAB/1_tutorial.ipynb."*

*   **Para sincronizar con tu Anki**:
    > 🤖 **Prompt**: *"Asegúrate de que mi aplicación Anki esté abierta y ejecuta el script 04_conversor_anki.py para importar las fichas directamente."*

---

## 📂 Estructura del Repositorio

*   📁 **`0_AGENTES/`**: Scripts de automatización ejecutados por los agentes (`01_transcriptor_pdf.py`, `02_verificar_traduccion.py`, `03_pipeline_concreto.py`, `04_conversor_anki.py`, `05_generador_colab.py`).
*   📁 **`1_CAPITULO/`**: PDF original y transcripción Markdown (`.md`) inicial.
*   📁 **`2_TRADUCCIONES/`**: Archivos traducidos formalmente al español científico.
*   📁 **`3_CONCRETO/`**: Versión condensada con explicaciones paso a paso de fórmulas complejas.
*   📁 **`4_APRENDER/`**: Cronogramas de repetición y la memoria de mazos de Anki (`MEMORIA_ANKI/`).
*   📁 **`5_COLAB/`**: Libretas de Jupyter resultantes (`.ipynb`) para Google Colab.


