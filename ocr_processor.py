import os
from config import IMAGE_FOLDER, OUTPUT_FILE, SUPPORTED_FORMATS
from pix2text import Pix2Text
from PIL import Image

# Inicialización de modelo Pix2Text
ocr_pix2text = Pix2Text()

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def process_image_with_pix2text(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        result = ocr_pix2text(image)

        print(f"[DEBUG] Resultado crudo de Pix2Text para {image_path}:")
        print(result)

        processed_text = []

        # Si el resultado tiene elementos (como Page.elements)
        if hasattr(result, "elements") and isinstance(result.elements, list):
            for element in result.elements:
                if hasattr(element, "text"):
                    processed_text.append(element.text.strip())
        # Fallback: si tiene atributo .text directamente
        elif hasattr(result, "text"):
            processed_text.append(result.text.strip())

        if not processed_text:
            print(f"[❌ AVISO] Pix2Text no extrajo texto de {image_path}. Tipo de 'result': {type(result)}")

        return "\n".join(processed_text)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[⚠️ ERROR] Pix2Text falló con {image_path}: {e}")
        return ""

def process_folder():
    all_text = []

    if not os.path.isdir(IMAGE_FOLDER):
        print(f"[❌ ERROR] La carpeta de imágenes no existe: '{IMAGE_FOLDER}'")
        return

    for filename in sorted(os.listdir(IMAGE_FOLDER)):
        if filename.lower().endswith(SUPPORTED_FORMATS):
            path = os.path.join(IMAGE_FOLDER, filename)
            print(f"\n📷 Procesando: {filename}")

            text_pix2text = process_image_with_pix2text(path)
            print(f"[DEBUG] Texto extraído para {filename}: {text_pix2text[:100]}...")

            if text_pix2text.strip():
                combined = f"\n\n=== {filename} ===\n"
                combined += text_pix2text.strip() + "\n"
                all_text.append(combined)
            else:
                print(f"[⚠️ AVISO] No se encontró texto útil en {filename}.")

    if all_text:
        try:
            print(f"[DEBUG] Se va a guardar el siguiente contenido ({len(all_text)} entradas):")
            for preview in all_text:
                print(preview[:150])

            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(all_text))
            print(f"\n✅ OCR con Pix2Text completado. Resultado guardado en '{OUTPUT_FILE}'")
        except Exception as e:
            print(f"[❌ ERROR] No se pudo escribir el archivo de salida '{OUTPUT_FILE}': {e}")
    else:
        print("[⚠️ AVISO] No se extrajo ningún texto para guardar.")

if __name__ == "__main__":
    process_folder()
