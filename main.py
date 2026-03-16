import os
from pydantic import BaseModel, Field
from typing import List
import fitz  
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Definir los esquemas de Pydantic (Tu output estructurado)
class ProblemaDetectado(BaseModel):
    descripcion: str = Field(description="Descripción detallada del problema o anomalía encontrada")
    severidad: str = Field(description="Nivel de severidad: ALTA, MEDIA o BAJA")
    ubicacion: str = Field(description="Ubicación física mencionada en el documento, si aplica")

class ReporteInspeccion(BaseModel):
    inspector: str = Field(description="Nombre del inspector o contratista a cargo")
    fecha_inspeccion: str = Field(description="Fecha de la inspección en formato YYYY-MM-DD")
    obra_aprobada: bool = Field(description="¿El documento indica explícitamente que la obra fue aprobada? True/False")
    problemas_detectados: List[ProblemaDetectado] = Field(description="Lista de problemas encontrados en la inspección")

print("Esquemas cargados correctamente. ¡Listo para procesar!")

def extraer_texto_pdf(ruta_archivo: str) -> str:
    """
    Abre un PDF, extrae todo su texto página por página 
    y maneja errores comunes en producción.
    """
    # 1. Validar que el archivo realmente exista antes de intentar abrirlo
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Error crítico: No se encontró el archivo '{ruta_archivo}'.")

    texto_completo = ""
    
    try:
       
        with fitz.open(ruta_archivo) as doc:
            for num_pagina, pagina in enumerate(doc):
                texto_extraido = pagina.get_text()
                if texto_extraido:
                    texto_completo += f"\n--- PÁGINA {num_pagina + 1} ---\n{texto_extraido}"
   
        if not texto_completo.strip():
            print("Advertencia: El documento parece no tener texto seleccionable (podría requerir OCR).")
            return ""

        return texto_completo

    except Exception as e:
        raise RuntimeError(f"Fallo inesperado al procesar el documento: {str(e)}")


def analizar_documento_con_ia(texto_extraido: str) -> str:
    """
    Envía el texto a Gemini forzando un output estructurado (JSON) 
    basado en el esquema de Pydantic.
    """
    if not texto_extraido:
        return "No hay texto para analizar."

    model = genai.GenerativeModel('gemini-2.5-flash')
    
    
    prompt = f"""
    Eres un agente experto en análisis de documentos y cumplimiento para la industria de la construcción.
    Tu tarea es leer el siguiente texto extraído de un documento desordenado y estructurar los datos 
    ESTRICTAMENTE siguiendo el esquema JSON proporcionado. 
    
    Reglas:
    - No inventes información. Si no encuentras un dato como el inspector, usa "No especificado".
    - Si no hay problemas, devuelve una lista vacía [].
    - EXTRAE CADA PROBLEMA UNA SOLA VEZ. Está estrictamente prohibido repetir información.
    
    TEXTO DEL DOCUMENTO:
    {texto_extraido}
    """
    
    try:
        respuesta = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ReporteInspeccion,
                temperature=0.3
            )
        )
        return respuesta.text
    
    except Exception as e:
        raise RuntimeError(f"Falló la comunicación con la IA: {str(e)}")

if __name__ == "__main__":
    archivo_prueba = "documento_prueba.pdf" 
    
    try:
        print(f"1. Extrayendo texto de '{archivo_prueba}'...")
        texto = extraer_texto_pdf(archivo_prueba)
        
        print("2. Procesando texto con Gemini (Output Estructurado)...")
        resultado_json = analizar_documento_con_ia(texto)
        
        print("\n--- RESULTADO FINAL (JSON ESTRUCTURADO) ---")
        print(resultado_json)
        
    except Exception as error:
        print(f"\n❌ Ocurrió un error: {error}")