import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Título de la app
st.title("Diagrama de Dispersión - Dataset Casa Eventos")

# Cargar dataset
@st.cache_data
def cargar_datos():
    df = pd.read_csv("dataset_casa_eventos_400.csv")
    return df

df = cargar_datos()

# Mostrar dataset
st.subheader("Vista previa del dataset")
st.write(df.head())

# Obtener columnas numéricas
columnas = df.columns.tolist()

# Selección de variables
st.subheader("Selecciona las variables")

x_var = st.selectbox("Variable para el eje X", columnas)
y_var = st.selectbox("Variable para el eje Y", columnas)

# Crear gráfico
if st.button("Generar gráfico"):
    fig, ax = plt.subplots()
    ax.scatter(df[x_var], df[y_var])
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_title(f"Dispersión: {x_var} vs {y_var}")

    st.pyplot(fig)