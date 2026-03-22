import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title('Gráfico de Control - Eventos "Fallidos" por Mes')

# Cargar archivo directamente
df = pd.read_csv("dataset_casa_eventos_400.csv")

# Convertir fecha
df["fecha"] = pd.to_datetime(df["Fecha"])

# -------------------------------
# 1. DETECTAR EVENTOS FALLIDOS
# -------------------------------
df["eventos_fallidos"] = (
    (df["Retraso?"] == "Si") |
    (df["Incompleto"] == "Si") |
    (df["Calidad del evento"] <= 5) |
    (df["Calidad de la comida"] <= 5) |
    (df["Calidad de la organizacion"] <= 5)
)

# -------------------------------
# 2. AGRUPAR POR MES
# -------------------------------
df["mes"] = df["Fecha"].dt.to_period("M")

# Contar eventos fallidos por mes
resumen_mensual = df.groupby("mes")["eventos_fallidos"].sum().reset_index()

st.subheader("Eventos fallidos por mes")
st.write(resumen_mensual)

# -------------------------------
# 3. GRÁFICO DE CONTROL
# -------------------------------
valores = resumen_mensual["eventos_fallidos"]

media = np.mean(valores)
desviacion = np.std(valores)

UCL = media + 3 * desviacion
LCL = max(0, media - 3 * desviacion)  # No puede ser negativo

# Gráfico
fig, ax = plt.subplots()

ax.plot(resumen_mensual["mes"].astype(str), valores, marker='o', label="Eventos fallidos")
ax.axhline(media, linestyle='--', label="Media")
ax.axhline(UCL, linestyle='--', label="UCL (+3σ)")
ax.axhline(LCL, linestyle='--', label="LCL (-3σ)")

ax.set_title("Gráfico de Control - Eventos Fallidos")
ax.set_xlabel("Mes")
ax.set_ylabel("Cantidad de fallos")
ax.legend()
plt.xticks(rotation=45)

st.pyplot(fig)

# Mostrar métricas
st.write(f"Media: {media:.2f}")
st.write(f"Límite Superior (UCL): {UCL:.2f}")
st.write(f"Límite Inferior (LCL): {LCL:.2f}")