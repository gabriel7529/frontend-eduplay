# EduPlay

**Descripción general**
EduPlay es una plataforma educativa gamificada que transforma automáticamente materiales de estudio (PDFs, apuntes, presentaciones) en actividades interactivas (trivias, flashcards, retos) mediante IA.

**Características técnicas principales**
- **Generación automática con IA**
  Convierte documentos en juegos interactivos, liberando al usuario de la creación manual de preguntas.
- **Arquitectura multiplataforma**
  Aplicación web y PWA accesible desde cualquier navegador en desktop o móvil.
- **Infraestructura en la nube**
  Almacenamiento de archivos en la nube, procesamiento escalable y respuesta en menos de 2 s para el 95 % de las solicitudes.
- **Gamificación avanzada**
  Niveles, insignias, rankings y recompensas para maximizar la motivación y el engagement.
- **Panel de análisis para docentes**
  Dashboard con métricas de uso, rendimiento y progreso de cada estudiante en tiempo real.
- **Seguridad y alta disponibilidad**
  Certificados TLS, cifrado en tránsito y reposo, backups diarios y SLA de 99.9 %.

---

# Configuración en Español (PDF a Quiz)

## Importante
Para probar esta app clonada en OpenAI GPT, visita mi [GPTs Agent PDF-to-Quizz](https://chat.openai.com/g/g-oMR8x3UTD-pdf-to-quizz). Es gratis, pero necesitas GPT Plus.

## Uso
1. Sube un PDF de varias páginas.
2. La app genera un cuestionario interactivo con opciones múltiples (2 preguntas por página).

Esta aplicación utiliza LangChain para abstraer las llamadas al modelo de lenguaje y Streamlit para la interfaz.

Ejemplo de PDF:

![PDF sample](img/PDF-sample.png)

Y genera:

![Quiz sample](img/quiz-reponse.png)

## Prerrequisitos
- Clave de API de OpenAI (https://platform.openai.com/account/api-keys).
- Se recomienda el modelo **gpt-3.5-turbo** para mantener el coste bajo, incluso con PDFs de hasta ~100 páginas.

```bash
export OPENAI_API_KEY=TU_API_KEY
```
## Instrucciones


Para instalar:
``` sh
pip install -r requirements.txt
```

## Ejecutar



Ejecutas con:
```sh
streamlit run ui.py
```

Para ejecutar en docker
```sh
docker build -t pdf-to-quizz .
docker run -e OPENAI_API_KEY=[your-api-key] -p 8501:8501 pdf-to-quizz
```
