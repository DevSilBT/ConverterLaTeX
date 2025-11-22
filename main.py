# main.py

from ocr_processor import process_folder
from parser_generator import run

def main():
    print("🧠 Ejecutando OCR sobre imágenes...")
    process_folder()
    print("\n📄 Generando archivo .tex desde el resultado...")
    run()
    print("\n✅ Todo listo. Puedes compilar el resultado en Overleaf o localmente.")

if __name__ == "__main__":
    main()
