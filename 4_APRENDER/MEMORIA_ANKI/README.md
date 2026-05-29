# Memoria de Mazos de Anki

Esta carpeta sirve como memoria persistente para organizar y clasificar las fichas de estudio que generamos en el plan de aprendizaje. 

## Estructura Actual de Mazos

* **Mazo Principal**: `Química Cuántica`
  * 📥 **Submazo 1**: `Química Cuántica::01_Ecuación_Schrödinger` (Conceptos y teoría de Schrödinger, incertidumbre, dualidad, etc.)
  * 🔢 **Submazo 2**: `Química Cuántica::02_Matemáticas_Física` (Números complejos, fórmulas, constantes y leyes físicas)
  * 📝 **Submazo 3**: `Química Cuántica::03_Problemas_Prácticos` (Problemas prácticos, normalización y cálculos)

## ¿Cómo funciona?
Al procesar nuevos temas o generar fichas, consultaremos esta memoria para asignar cada pregunta al submazo correspondiente de manera automática o mediante sugerencias. Si creas nuevos mazos en Anki, puedes editar el archivo [estructura_mazos.json](./estructura_mazos.json) para que lo tenga en cuenta en futuras actualizaciones.
