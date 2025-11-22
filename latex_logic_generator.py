from datetime import datetime
import os
import re
from jinja2 import Environment, FileSystemLoader
import language_tool_python

# Rutas
INPUT_TXT = "output/ocr_result.txt"
CORRECTED_TXT = "output/ocr_result_corregido.txt"
OUTPUT_TEX = "output/resultado_final.tex"
TEMPLATE_DIR = "templates"
TEMPLATE_NAME = "logic_template.tex"

# Inicializa el corrector ortográfico
tool = language_tool_python.LanguageTool('es')


def corregir_ortografia(texto):
    """Corrige errores ortográficos en un bloque de texto."""
    return tool.correct(texto)


def guardar_texto_corregido(raw_texto):
    """Aplica corrección ortográfica global al .txt y guarda el resultado."""
    bloques = re.split(r"(=== .*? ===)", raw_texto)
    texto_corregido = ""

    for i in range(0, len(bloques), 2):
        header = bloques[i] if i < len(bloques) else ""
        contenido = bloques[i + 1] if i + 1 < len(bloques) else ""
        corregido = corregir_ortografia(contenido)
        texto_corregido += header + corregido

    with open(CORRECTED_TXT, "w", encoding="utf-8") as f:
        f.write(texto_corregido)

    print(f"📝 Texto corregido guardado en: {CORRECTED_TXT}")
    return texto_corregido


def parse_text(txt_content):
    """Analiza el texto corregido y lo estructura para el LaTeX."""
    blocks = re.split(r"=== .*? ===", txt_content)
    ejercicios = []

    for block in blocks:
        if not block.strip():
            continue

        current = {"ejercicio": "Ejercicio", "items": []}
        items = re.findall(
            r"\(\w\) (.*?)\n(Respuesta|Tipo de proposici[oó]n|An[aá]lisis|Negaci[oó]n|Antecedente|Consecuente|Teorema|Definici[oó]n|F[oó]rmula|Tema|Subtema).*?[:：]\s*(.*?)\n",
            block,
            re.DOTALL
        )

        for enunciado, etiqueta, valor in items:
            item = {"enunciado": enunciado.strip()}
            key = etiqueta.lower().strip()

            if "respuesta" in key:
                item["respuesta"] = valor.strip()
            elif "tipo" in key:
                item["tipo"] = valor.strip()
            elif "negaci" in key:
                item["negacion"] = valor.strip()
            elif "antecedente" in key:
                item["antecedente"] = valor.strip()
            elif "consecuente" in key:
                item["consecuente"] = valor.strip()
            elif "análisis" in key or "analisis" in key:
                item["analisis"] = valor.strip()
            elif "teorema" in key:
                item["teorema"] = valor.strip()
            elif "definici" in key:
                item["definicion"] = valor.strip()
            elif "fórmula" in key or "formula" in key:
                item["formula"] = valor.strip()
            elif "tema" in key:
                item["tema"] = valor.strip()
            elif "subtema" in key:
                item["subtema"] = valor.strip()

            current["items"].append(item)

        ejercicios.append(current)

    return ejercicios


def escape_tex(text):
    """
    Escapa caracteres especiales de LaTeX para evitar errores de compilación.
    """
    if not isinstance(text, str):
        return text

    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text


def render_to_latex(data):
    """Genera el documento .tex usando la plantilla."""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    env.filters["escape_tex"] = escape_tex

    template = env.get_template(TEMPLATE_NAME)
    fecha = datetime.now().strftime('%d/%m/%Y')
    rendered = template.render(ejercicios=data, fecha=fecha)

    with open(OUTPUT_TEX, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"📄 Documento LaTeX guardado en: {OUTPUT_TEX}")


def run():
    if not os.path.exists(INPUT_TXT):
        print(f"[❌ ERROR] Archivo de entrada no encontrado: {INPUT_TXT}")
        return

    with open(INPUT_TXT, encoding="utf-8") as f:
        raw_texto = f.read()

    texto_corregido = guardar_texto_corregido(raw_texto)
    estructura = parse_text(texto_corregido)
    render_to_latex(estructura)


run()
