import streamlit as st
import tempfile
import os
import json
from cv_parser import parse_cv, generate_cv_from_template

# ===============================
# CONFIG
# ===============================

TEMPLATES = {
    "Plantilla 1": "templates/Plantilla1.docx",
    "Plantilla 2": "templates/Plantilla2.docx",
    "Plantilla 3": "templates/Plantilla3.docx",
}

st.set_page_config(page_title="CV ATS Generator", layout="centered")

st.title("📄 CV ATS Parser & Generator")
st.write("Sube tu CV, elige una plantilla y genera un nuevo CV automáticamente.")

# ===============================
# SUBIR PDF
# ===============================

uploaded_file = st.file_uploader("Sube tu CV (PDF)", type=["pdf"])

template_name = st.selectbox("Selecciona una plantilla", list(TEMPLATES.keys()))

# ===============================
# PROCESAR
# ===============================

if uploaded_file and st.button("Generar CV"):
    with st.spinner("Procesando CV..."):
        # Guardar PDF temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        # Parsear CV
        cv_json = parse_cv(pdf_path)

        # Mostrar JSON
        st.subheader("📄 Datos detectados")
        st.json(cv_json)

        # Generar CV final
        output_docx, output_pdf = generate_cv_from_template(
            template_path=TEMPLATES[template_name],
            cv_json=cv_json,
            output_dir="output"
        )

        st.success("CV generado correctamente")

        # ===============================
        # DESCARGAS
        # ===============================

        with open(output_docx, "rb") as f:
            st.download_button(
                "⬇ Descargar DOCX",
                f,
                file_name=os.path.basename(output_docx),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        if output_pdf and os.path.exists(output_pdf):
            with open(output_pdf, "rb") as f:
                st.download_button(
                    "⬇ Descargar PDF",
                    f,
                    file_name=os.path.basename(output_pdf),
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ El PDF no pudo generarse en este entorno.")