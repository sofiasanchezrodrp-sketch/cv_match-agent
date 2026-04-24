import streamlit as st
from src.graph import build_graph

st.set_page_config(page_title="CV Match Agent", page_icon="🔍", layout="wide")

st.title("🔍 CV Match Agent")
st.caption("Analiza el fit entre tu CV y una oferta de trabajo")

col1, col2 = st.columns(2)

with col1:
    cv_texto = st.text_area("Tu CV", height=400, placeholder="Pega aquí tu CV...")

with col2:
    oferta_texto = st.text_area("Oferta de trabajo", height=400, placeholder="Pega aquí la oferta...")

if st.button("Analizar fit", type="primary"):
    if not cv_texto or not oferta_texto:
        st.error("Por favor rellena los dos campos.")
    else:
        with st.spinner("Analizando..."):
            graph = build_graph()
            result = graph.invoke({
                "cv_texto": cv_texto,
                "oferta_texto": oferta_texto,
                "skills_cv": [],
                "skills_oferta": [],
                "skills_match": [],
                "skills_gap": [],
                "fit_score": 0.0,
                "recomendaciones": "",
                "cv_adaptado": ""
            })

        st.divider()

        col3, col4 = st.columns(2)

        with col3:
            st.metric("Fit Score", f"{result['fit_score']}%")
            st.subheader("Skills que tienes")
            st.write(", ".join(result["skills_match"]) or "Ninguna")
            st.subheader("Skills que te faltan")
            st.write(", ".join(result["skills_gap"]) or "Ninguna")

        with col4:
            st.subheader("💡 Recomendaciones")
            st.write(result["recomendaciones"])

        st.divider()
        st.subheader("📝 CV adaptado")
        st.write(result["cv_adaptado"])