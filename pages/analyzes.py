import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
from components.navigation import navigation_bar

navigation_bar()

st.title("Análise de Dados de Processos do Sistema")

# --- 1. Apresentação dos Dados e Tipos de Variáveis (Requisito 1) ---
st.markdown("""
### 1. Sobre o Conjunto de Dados
Esta análise é baseada em um arquivo de texto (`processos.txt`) que simula a saída de um comando de monitoramento de processos em um sistema operacional (como o `top` ou `ps`). O objetivo é entender o comportamento do consumo de recursos (CPU e memória) pelos diferentes processos e usuários.
""")

st.info("""
**Como gerar o arquivo de análise:**
Para extrair os dados de processos do seu sistema, execute o comando correspondente ao seu sistema operacional no terminal. 
""")

lin_tab, win_tab = st.tabs(["🐧 Linux / macOS", "🪟 Windows"])

with lin_tab:
    st.markdown("""
    Execute o comando abaixo no seu terminal. Ele irá gerar o arquivo `processos.txt` no formato esperado para a **Análise Guiada**.
    
    ```bash
    ps -eo pid,user,%cpu,%mem,command --sort=-%cpu > processos.txt
    ```
    Depois, coloque o arquivo gerado na pasta `data/` do projeto ou faça o upload na aba "Análise Customizada".
    """)

with win_tab:
    st.markdown("""
    Execute o comando abaixo no **PowerShell**. Ele irá gerar um arquivo `processos.csv`.

    ```powershell
    Get-Process -IncludeUserName | Select-Object Id, UserName, CPU, WS, ProcessName | ConvertTo-Csv -NoTypeInformation > processos.csv
    ```
    
    **Importante:** Use o arquivo `processos.csv` gerado diretamente na aba "Análise Customizada", pois o formato é diferente do esperado pela análise guiada.
    """)

with st.expander("Detalhes do Conjunto de Dados"):
    st.markdown("""
    **Perguntas de Análise:**
    - Qual é a distribuição do consumo de CPU e memória?
    - Existem processos ou usuários que consomem mais recursos?
    - A média de consumo de CPU do sistema se mantém em um nível esperado?

    **Tipos de Variáveis:**
    - **PID**: `Quantitativa Discreta` (Identificador do Processo)
    - **USER**: `Qualitativa Nominal` (Nome do Usuário)
    - **%CPU**: `Quantitativa Contínua` (Percentual de uso da CPU)
    - **%MEM**: `Quantitativa Contínua` (Percentual de uso da Memória)
    - **COMMAND**: `Qualitativa Nominal` (Nome do Comando/Processo)
    """)

tab_dashboard, tab_report, tab_conversor = st.tabs(['📈 Análise Guiada', '📋 Análise Customizada', '🔄 Conversor TXT -> CSV'])

# =========================
# Função para converter TXT -> DataFrame
# =========================
def converter_txt_para_df(linhas):
    dados = []
    for linha in linhas:
        partes = linha.split()
        if len(partes) < 5:
            continue
        try:
            pid = int(partes[0])
            user = partes[1]
            cpu = float(partes[2])
            mem = float(partes[3])
            command = " ".join(partes[4:])
            dados.append([pid, user, cpu, mem, command])
        except:
            pass
    return pd.DataFrame(dados, columns=["PID", "USER", "%CPU", "%MEM", "COMMAND"])

# =========================
# Função de análise
# =========================
def analise_processos(df):
    st.subheader("Pré-visualização dos Dados")
    st.dataframe(df.head())

    # --- 2. Medidas Centrais, Dispersão, Correlação (Requisito 2) ---
    st.markdown("### 2. Análise Descritiva e Correlação")
    st.write("A tabela abaixo resume as principais estatísticas das variáveis de consumo.")
    st.write(df[["%CPU", "%MEM"]].describe())

    media_cpu = df["%CPU"].mean()
    mediana_cpu = df["%CPU"].median()
    dp_cpu = df["%CPU"].std()

    col1, col2, col3 = st.columns(3)
    col1.metric("Média CPU (%)", f"{media_cpu:.2f}")
    col2.metric("Mediana CPU (%)", f"{mediana_cpu:.2f}")
    col3.metric("Desvio Padrão CPU (%)", f"{dp_cpu:.2f}")

    st.markdown("#### Distribuição e Correlação")
    st.write("O histograma mostra que a maioria dos processos consome pouca CPU, com alguns outliers consumindo mais. O gráfico de dispersão investiga se há uma correlação entre o consumo de CPU e memória.")

    col_hist, col_scatter = st.columns(2)
    with col_hist:
        fig_hist = px.histogram(df, x="%CPU", nbins=20, title="Distribuição do Uso de CPU (%)")
        st.plotly_chart(fig_hist, use_container_width=True)
    with col_scatter:
        fig_scatter = px.scatter(df, x="%CPU", y="%MEM", title="Correlação CPU vs. Memória")
        st.plotly_chart(fig_scatter, use_container_width=True)

    correlacao = df["%CPU"].corr(df["%MEM"])
    st.info(f"**Correlação entre CPU e Memória:** `{correlacao:.2f}`. Um valor próximo de 0 indica uma correlação linear fraca.")

    st.markdown("#### Consumo por Usuário")
    consumo_usuario = df.groupby("USER")[["%CPU", "%MEM"]].sum().sort_values(by="%CPU", ascending=False).reset_index()
    fig_bar = px.bar(consumo_usuario, x="USER", y="%CPU", title="Consumo Total de CPU por Usuário (%)")
    st.plotly_chart(fig_bar, use_container_width=True)


    # --- 3. Intervalo de Confiança e Teste de Hipótese (Requisito 3) ---
    st.markdown("### 3. Inferência Estatística sobre o Uso de CPU")
    st.write("Nesta seção, usamos a amostra de dados para fazer inferências sobre a população de todos os processos.")

    st.markdown("#### Teste de Hipótese para a Média de CPU")
    st.markdown("""
    **Justificativa:** Para verificar se o consumo médio de CPU do sistema está acima de um patamar hipotético de **2%**, usamos um **Teste T de uma amostra**. Este teste é adequado porque temos uma amostra dos dados e queremos comparar sua média com um valor específico.

    - **Hipótese Nula (H₀):** A média de uso de CPU é igual a 2% (`μ = 2`).
    - **Hipótese Alternativa (H₁):** A média de uso de CPU é diferente de 2% (`μ ≠ 2`).
    """)

    media_hipotetica = 2.0
    t_stat, p_val = stats.ttest_1samp(df["%CPU"], media_hipotetica)

    st.write(f"**Resultado do Teste T:** (H₀: Média de CPU = {media_hipotetica}%)")
    col_t, col_p = st.columns(2)
    col_t.metric("Estatística t", f"{t_stat:.2f}")
    col_p.metric("Valor-p", f"{p_val:.4f}")

    if p_val < 0.05:
        st.success(f"**Conclusão:** Rejeitamos a hipótese nula (p < 0.05). A média de consumo de CPU é estatisticamente diferente de {media_hipotetica}%.")
    else:
        st.info(f"**Conclusão:** Não há evidências para rejeitar a hipótese nula (p >= 0.05). A média de consumo de CPU não é estatisticamente diferente de {media_hipotetica}%.")

    st.markdown("#### Intervalo de Confiança")
    st.write("O Intervalo de Confiança (IC) de 95% nos dá uma faixa de valores onde podemos ter 95% de certeza de que a verdadeira média de consumo de CPU da população se encontra.")
    ic = stats.t.interval(0.95, len(df["%CPU"])-1, loc=media_cpu, scale=stats.sem(df["%CPU"]))
    st.success(f"**IC de 95% para a Média de CPU:** `{ic[0]:.2f}%` a `{ic[1]:.2f}%`")

    st.markdown("### 4. Conclusões e Insights")
    st.info("""
    Com base nos dados, notamos que a média de consumo de CPU é estatisticamente diferente de 2%, o que pode indicar que o sistema opera com uma carga um pouco acima do esperado. 
    
    Além disso, a baixa correlação entre CPU e memória sugere que não há uma relação direta de consumo entre esses dois recursos, ou seja, um processo que usa muita CPU não necessariamente usará muita memória.
    """)


# =========================
# Aba Análise Guiada
# =========================
with tab_dashboard:
    try:
        with open("data/processos.txt", "r") as f:
            linhas = f.readlines()
        df = converter_txt_para_df(linhas)
        analise_processos(df)
    except FileNotFoundError:
        st.error("Arquivo `data/processos.txt` não encontrado. Verifique o caminho e a estrutura do projeto.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")


# =========================
# Aba Análise Customizada
# =========================
with tab_report:
    uploaded_file = st.file_uploader("Envie seu arquivo .txt ou .csv", type=["txt", "csv"], key="custom_uploader")
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".txt"):
                linhas = uploaded_file.read().decode("utf-8").splitlines()
                df = converter_txt_para_df(linhas)
            else:
                df = pd.read_csv(uploaded_file)
            analise_processos(df)
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

# =========================
# Aba Conversor
# =========================
with tab_conversor:
    st.header("Conversor de TXT (processos) para CSV")
    uploaded_file_conv = st.file_uploader("Envie o arquivo de processos (.txt)", type=["txt"], key="converter_uploader")
    if uploaded_file_conv is not None:
        try:
            linhas = uploaded_file_conv.read().decode("utf-8").splitlines()
            df_conv = converter_txt_para_df(linhas)

            st.subheader("Pré-visualização dos Dados")
            st.dataframe(df_conv.head())

            csv = df_conv.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar CSV formatado",
                data=csv,
                file_name="processos.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")