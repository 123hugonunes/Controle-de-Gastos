import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Carregar ou criar base de dados
def load_data():
    try:
        return pd.read_csv("gastos.csv", parse_dates=["Data"])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Data", "Categoria", "Valor", "Descrição"])

# Salvar dados
def save_data(df):
    df.to_csv("gastos.csv", index=False)

# Interface
st.title("💰 Controle de Gastos Pessoais")

# Entrada de dados
with st.form("form_gasto"):
    data = st.date_input("Data", value=datetime.today())
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Saúde", "Outros"])
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
    descricao = st.text_input("Descrição")
    submit = st.form_submit_button("Adicionar Gasto")

# Processamento
df = load_data()
if submit:
    novo_gasto = pd.DataFrame([[data, categoria, valor, descricao]], columns=df.columns)
    df = pd.concat([df, novo_gasto], ignore_index=True)
    save_data(df)
    st.success("Gasto adicionado com sucesso!")

# Visualização
st.subheader("📋 Tabela de Gastos")
st.dataframe(df)

# Estatísticas
st.subheader("📊 Estatísticas")
if not df.empty:
    st.write("Total gasto:", df["Valor"].sum())
    fig, ax = plt.subplots()
    df.groupby("Categoria")["Valor"].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
