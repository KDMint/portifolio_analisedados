import streamlit as st
from components.navigation import navigation_bar

navigation_bar()


st.title("Formação & Certificações")

st.subheader("🎓 Formação Acadêmica")
st.markdown(
    """
    - **Bacharelado em Engenharia de Software**  
      *FIAP (2024–2027, cursando)*
    - **Técnico em Engenharia Mecatrônica**  
      *ETEC Lauro Gomes (2021–2023)*
    """
)

st.divider()

st.subheader("🏆 Certificações e Cursos")
with st.expander("Ver todos os certificados"):
    st.markdown(
        """
        - Algoritmos: Aprenda a programar
        - Lógica de Programação (JavaScript)
        - Acessibilidade no HTML
        - Funções com Excel (intermediário)
        - Formação Social e Sustentabilidade
        """
    )

st.divider()

st.subheader("🌐 Idiomas")
st.markdown("- **Inglês** — Básico (em curso)")