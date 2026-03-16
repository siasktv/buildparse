# BuildParse MVP: AI-Powered Construction Document Pipeline

Un pipeline de extracción multimodal diseñado para la industria de la construcción. Este MVP procesa documentos técnicos desordenados (como reportes de inspección en PDF) y utiliza razonamiento agéntico para devolver estructuras JSON estrictas y deterministas.

## 🚀 El Problema que Resuelve
[cite_start]Los contratistas lidian con procesos manuales tediosos al revisar documentos y normativas[cite: 6]. Este script automatiza la extracción de entidades clave (fechas, inspectores, problemas de seguridad y severidad) aplicando reglas estrictas de validación de datos para evitar alucinaciones del LLM.

## 🛠️ Stack Tecnológico (MVP Local)
- [cite_start]**Python 3.12** (Core pipeline) [cite: 26, 42]
- [cite_start]**PyMuPDF / fitz** (Extracción de texto de documentos PDF) [cite: 30, 42]
- **Pydantic** (Validación de esquemas de datos y tipado estricto)
- [cite_start]**Gemini 2.5 Flash API** (Generación estructurada de JSON) [cite: 21, 42]

---

## 💻 Cómo ejecutarlo localmente

1. **Clona el repositorio e ingresa a la carpeta:**
   ```bash
   git clone <URL_DE_TU_REPO>
   cd buildparse-mvp
Crea y activa el entorno virtual:Bash# En Windows (Git Bash):
python -m venv venv
source venv/Scripts/activate
Instala las dependencias:Bashpip install pymupdf pydantic google-generativeai python-dotenv
Configura tus variables de entorno:Crea un archivo .env en la raíz del proyecto y agrega tu API Key:Fragmento de códigoGEMINI_API_KEY="tu_clave_aqui"
Ejecuta el pipeline:Bashpython main.py
🏗️ Arquitectura de Producción (Next Steps)Este MVP local es la prueba de concepto del core de IA. Para llevar este sistema a producción bajo los estándares de escalabilidad requeridos, la arquitectura evolucionaría de la siguiente manera:1. Contenerización y Despliegue CI/CDEl pipeline de Python se empaquetaría usando Docker para garantizar consistencia entre entornos. El despliegue de los modelos de ML se automatizaría mediante flujos de CI/CD hacia plataformas como Railway o directamente a la nube.2. Infraestructura Cloud (GCP / Azure)El sistema completo residiría en GCP o Azure.Infraestructura como Código (IaC): Utilizaría Terraform para aprovisionar los recursos de forma programática y auditable.Optimización de Costos: Se configurarían alertas y auto-escalado para asegurar que los recursos de cómputo se apaguen cuando no estén en uso. Entiendo perfectamente que una instancia GPU corriendo idle es plata quemada.3. Edge Cases y Visión ComputacionalPara PDFs que son puramente imágenes escaneadas (sin texto embebido), el pipeline se expandiría integrando OCR o enviando las imágenes extraídas a Claude Vision API / OpenCV para análisis visual directo.4. Integración Full StackEl output estructurado de este pipeline alimentaría directamente un backend serverless en Convex (gestionando base de datos en tiempo real y auth), el cual a su vez hidrataría una interfaz web moderna construida con React 19, TypeScript y Tailwind.