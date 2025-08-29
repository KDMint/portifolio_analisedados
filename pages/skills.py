import streamlit as st
from components.navigation import navigation_bar

navigation_bar()

st.title("Skills Técnicas & Soft Skills")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛠️ Tecnologias")
    st.markdown(
        """
        - **Linguagens:** Python, C++, SQL
        - **Frameworks e Bibliotecas:** Django, Flet, Streamlit, Pandas, Plotly
        - **Web:** HTML, CSS, JavaScript
        - **Banco de Dados:** MySQL, PostgreSQL
        - **Sistemas e Ferramentas:** Linux, Git/GitHub, Docker (básico)
        """
    )

with col2:
    st.subheader("🤝 Soft Skills")
    st.markdown(
        """
        - Criatividade e Storytelling  
        - Trabalho em equipe  
        - Comunicação e Apresentação
        - Resolução de Problemas
        - Gestão Ágil
        """
    )

st.divider()

st.subheader("💡 Interesses")
st.markdown("- Desenvolvimento Web (Full-Stack), Análise de Dados, Cibersegurança, DevOps")