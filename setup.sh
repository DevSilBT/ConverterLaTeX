#!/bin/bash

echo "🔧 Iniciando instalación de ConverterLaTeX en Debian..."

# ===============================
# 1. Actualización del sistema
# ===============================

sudo apt update
sudo apt upgrade -y

# ===============================
# 2. Instalar dependencias del sistema
# ===============================

echo "📦 Instalando dependencias del sistema..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libjpeg-dev \
    libpng-dev \
    libopenblas-dev

# ===============================
# 3. Crear entorno virtual
# ===============================

echo "🐍 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# ===============================
# 4. Instalar dependencias de Python
# ===============================

echo "📜 Instalando dependencias de req.txt..."
pip install --upgrade pip setuptools wheel
pip install -r req.txt

# ===============================
# 5. Preparar carpetas
# ===============================

echo "📁 Configurando directorios..."
mkdir -p output
chmod -R 777 output

mkdir -p images
chmod -R 777 images

# ===============================
# 6. Test rápido del programa
# ===============================

echo "🧪 Ejecutando prueba inicial..."
if python3 - <<EOF
import os
print("Python OK")
import PIL
print("Pillow OK")
print("Setup completado")
EOF
then
    echo "✅ Todo instalado y verificado correctamente."
else
    echo "❌ ERROR: Algo falló durante el test."
fi

echo "🎉 Instalación finalizada. Puedes ejecutar:"
echo ""
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
