import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

# Título de la app
st.title("Diagrama de Dispersión - Dataset Casa Eventos")

# -------------------------------
# CARGAR DATASET
# -------------------------------
@st.cache_data
def cargar_datos():
    df = pd.read_csv("dataset_casa_eventos_400.csv")
    return df

df = cargar_datos()

# -------------------------------
# MOSTRAR DATASET ORIGINAL
# -------------------------------
st.subheader("Vista previa del dataset")
st.write(df.head())

# -------------------------------
# PREPARAR DATASET AGRUPADO
# -------------------------------
df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")

# Convertir variables categóricas a numéricas
df["Incompleto_num"] = df["Incompleto"].map({"Si": 1, "No": 0})
df["Retraso_num"] = df["Retraso?"].map({"Si": 1, "No": 0})
df["Error_pedido_num"] = df["Error en pedido"].map({"Si": 1, "No": 0})

# Crear año y mes
df["año"] = df["Fecha"].dt.year
df["mes"] = df["Fecha"].dt.month

# Dataset agregado (PROMEDIOS)
df_promedio = df.groupby(["año", "mes"]).agg({
    "Calidad del evento": "mean",
    "Cantidad personal": "mean",
    "Calidad de la comida": "mean",
    "Incompleto_num": "mean",
    "Retraso_num": "mean",
    "Calidad de la organizacion": "mean",
    "Error_pedido_num": "mean"
}).reset_index()

# -------------------------------
# MOSTRAR DATASET AGRUPADO
# -------------------------------
st.subheader("Vista previa del dataset agregado (por mes y año)")
st.write(df_promedio.head())

# -------------------------------
# PREPARAR COLUMNAS PARA SELECTBOX
# -------------------------------
columnas_df = [f"Original - {col}" for col in df.columns if col not in ["Fecha", "año", "mes"]]
columnas_prom = [f"Promedio - {col}" for col in df_promedio.columns if col not in ["año", "mes"]]

columnas = columnas_df + columnas_prom

# -------------------------------
# SELECCIÓN DE VARIABLES
# -------------------------------
st.subheader("Selecciona las variables")

x_var = st.selectbox("Variable para el eje X", columnas)
y_var = st.selectbox("Variable para el eje Y", columnas)

# -------------------------------
# GENERAR GRÁFICO
# -------------------------------
if st.button("Generar gráfico"):
    fig, ax = plt.subplots()

    # Función para obtener datos según dataset
    def obtener_serie(var):
        if var.startswith("Original - "):
            col = var.replace("Original - ", "")
            return df[col]
        elif var.startswith("Promedio - "):
            col = var.replace("Promedio - ", "")
            return df_promedio[col]

    # Obtener datos
    x = obtener_serie(x_var)
    y = obtener_serie(y_var)

    # Validar que sean del mismo tamaño
    if len(x) != len(y):
        st.error("No puedes mezclar variables de diferente nivel (original vs promedio)")
        st.stop()

    # Scatter
    ax.scatter(x, y)

    # Línea de tendencia
    if len(x) > 1:
        m, b = np.polyfit(x, y, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = m * x_line + b
        ax.plot(x_line, y_line)

    # Etiquetas
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_title(f"Dispersión: {x_var} vs {y_var}")

    st.pyplot(fig)

    # Coeficiente de correlación
    if len(x) > 1:
        correlacion = np.corrcoef(x, y)[0, 1]
        st.write(f"Coeficiente de correlación: {correlacion:.4f}")