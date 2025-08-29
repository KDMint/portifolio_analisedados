import streamlit as st
from components.navigation import navigation_bar

navigation_bar()

st.title("Experiências Relevantes")
st.divider()

st.subheader('💼 Estágio')
with st.container(border=True):
    st.markdown("#### Estagiária de TI | Educa Insights (2025–Presente)")
    st.markdown(
        """
        - Suporte e desenvolvimento em sistemas de **CRM** e **Banco de Dados**.
        - Colaboração em projetos de **integração com sistemas TOTVS**.
        - Automação de rotinas e extração de dados para relatórios.
        """
    )

st.subheader('🚀 Projetos')
with st.container(border=True):
    st.markdown("#### BLUE FUTURE – Inovação Azul | FIAP (Mai–Jun/2024)")
    st.markdown(
        """
        - Desenvolvimento de software em **Python e Arduino** para soluções ambientais  
        - Criação de **landing page** (HTML, CSS, JS) com foco em UX  
        - Pitchs e **gestão ágil** de projetos
        """
    )

with st.container(border=True):
    st.markdown("#### Fórmula E | FIAP (Ago–Set/2024)")
    st.markdown(
        """
        - Desenvolvimento **web** para promover a Fórmula E  
        - **Storytelling** para apresentações a investidores  
        - Trabalho em equipe multidisciplinar
        """
    )