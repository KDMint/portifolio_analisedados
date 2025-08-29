import streamlit as st
from components.navigation import navigation_bar, header, github_card, social_links

navigation_bar()

header("Khadija Lima")

st.markdown(
    """
    Olá! Sou uma estudante de **Engenharia de Software** na FIAP, apaixonada por criar soluções que combinam tecnologia e design.
    Com uma base sólida em **Python, Banco de Dados, e desenvolvimento web**, estou sempre em busca de novos desafios e oportunidades para aplicar meus conhecimentos em **análise de dados** e desenvolvimento de software para resolver problemas do mundo real.
    
    Este portfólio foi criado para demonstrar algumas das minhas habilidades e projetos. Sinta-se à vontade para explorar!
    """
)

social_links()

st.divider()

github_card("KDMint")