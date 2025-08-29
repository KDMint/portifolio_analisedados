import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def navigation_bar():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] > div:first-child {
                display: flex;
                flex-direction: column;
                height: 100vh;
                padding-bottom: 0;
            }
            .footer {
                margin-top: auto;
                font-size: 12px;
                color: #888;
                text-align: center;
                padding: 12px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("Navigation Bar")
        st.page_link("pages/home.py", label="Home", icon=':material/home_app_logo:')
        st.page_link("pages/formation.py", label="Education", icon=':material/school:')
        st.page_link("pages/professional_experiences.py", label="Professional Experience", icon=':material/business_center:')
        st.page_link("pages/skills.py", label="Skills", icon=':material/construction:')
        st.page_link("pages/analyzes.py", label="Data Analysis", icon=':material/chart_data:')

        # Rodapé fixado no fundo da sidebar
        st.markdown('<div class="footer">&copy; Todos os Direitos Reservados a Khadija Lima</div>', unsafe_allow_html=True)

def header(title: str, subtitle: str | None = None):
    col1, col2 = st.columns([1,5])
    with col1:
        st.image("https://github.com/KDMint.png", width=80)
    with col2:
        st.markdown(f"# {title}")
        if subtitle:
            st.markdown(subtitle)

def github_card(username: str = "KDMint"):
    st.subheader("GitHub")
    st.caption("Dados públicos via GitHub API")
    try:
        r = requests.get(f"https://api.github.com/users/{username}", timeout=10)
        if r.status_code == 200:
            info = r.json()
            cols = st.columns([1,2,2,2])
            cols[0].metric("Repositórios", info.get("public_repos", 0))
            cols[1].metric("Seguidores", info.get("followers", 0))
            cols[2].metric("Seguindo", info.get("following", 0))
            cols[3].markdown(f"[Perfil](https://github.com/{username})")
            if info.get("bio"):
                st.info(info["bio"])
        else:
            st.warning("Não consegui ler a API do GitHub agora.")
    except Exception as e:
        st.warning(f"Falha ao contactar GitHub: {e}")

def social_links(linkedin_url: str = "https://linkedin.com/in/khadija-lima-8215672b7"):
    st.subheader("Links")
    st.markdown(f"- 🔗 [LinkedIn]({linkedin_url})\n- 🐙 [GitHub](https://github.com/KDMint)")

