import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.markdown(f"<h1 style='text-align: center;'>Gráfico de Control - Eventos \"Fallidos\" por Mes y Año</h1>",unsafe_allow_html=True)

# Cargar archivo
df = pd.read_csv("dataset_casa_eventos_400.csv")

# Convertir fecha
df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")

# -------------------------------
# 1. PORCENTAGE ACTUAL DE FALLAS
# -------------------------------

df['eventos_fallidos'] = (
    (df["Retraso?"] == "Si") |
    (df["Incompleto"] == "Si") |
    (df["Calidad del evento"] <= 5) |
    (df["Calidad de la comida"] <= 5) |
    (df["Calidad de la organizacion"] <= 5)
)

porcentage_f = (df['eventos_fallidos'].sum() / len(df)) * 100

st.markdown(
    f"<h3 style='text-align: center; color: white;'>EL TOTAL DE EVENTOS FALLIDOS ES {df['eventos_fallidos'].sum()} "
    f"Y EL PORCENTAGE ACTUAL DE FALLAS EN OPERACIONES: {porcentage_f:.2f}%</h3>",
    unsafe_allow_html=True
)

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
# 2. CREAR AÑO Y MES
# -------------------------------
df["año"] = df["Fecha"].dt.year
df["mes"] = df["Fecha"].dt.month  # mejor numérico para ordenar

# Agrupar por año y mes
resumen = df.groupby(["año", "mes"])["eventos_fallidos"].sum().reset_index()

st.subheader("Eventos fallidos por año y mes")
st.write(resumen)

# -------------------------------
# 3. GRÁFICOS POR CADA AÑO
# -------------------------------
años = resumen["año"].unique()

for año in años:
    st.subheader(f"Año {año}")

    data_año = resumen[resumen["año"] == año]

    valores = data_año["eventos_fallidos"]

    # Estadísticos por año
    media = np.mean(valores)
    desviacion = np.std(valores)

    UCL = media + 3 * desviacion
    LCL = max(0, media - 3 * desviacion)

    # Gráfico
    fig, ax = plt.subplots()

    ax.plot(data_año["mes"], valores, marker='o', label="Eventos fallidos")
    ax.axhline(media, linestyle='--', label="Media")
    ax.axhline(UCL, linestyle='--', label="UCL (+3σ)")
    ax.axhline(LCL, linestyle='--', label="LCL (-3σ)")

    ax.set_title(f"Gráfico de Control - {año}")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Cantidad de fallos")
    ax.set_xticks(range(1,13))
    ax.legend()

    st.pyplot(fig)

    # Métricas por año
    st.write(f"Media: {media:.2f}")
    st.write(f"UCL: {UCL:.2f}")
    st.write(f"LCL: {LCL:.2f}")

    
# Título
st.title("📊 Diagrama de Pareto")
# Cargar dataset
df = pd.read_csv('dataset_pareto.csv')
# Convertir a formato adecuado (una sola fila → categorías)
frecuencias = df.iloc[0]
frecuencias = frecuencias.sort_values(ascending=False)

# Calcular porcentaje acumulado
porcentaje_acumulado = frecuencias.cumsum() / frecuencias.sum() * 100

# Mostrar dataset con frecuencias
pareto_df = pd.DataFrame({
    'Frecuencia': frecuencias,
    'Porcentaje Acumulado': porcentaje_acumulado
})

st.subheader("📋 Tabla de resultados")
st.dataframe(
    pareto_df.style.format({
        "Porcentaje Acumulado": "{:.2f}%"
    }),
    use_container_width=True
)

# Gráfico mejorado
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.bar(range(len(frecuencias.index)), frecuencias)
ax1.set_ylabel("Frecuencia")

ax2 = ax1.twinx()
ax2.plot(range(len(frecuencias.index)), porcentaje_acumulado, marker='o')
ax2.set_ylabel("Porcentaje acumulado")

ax2.axhline(80, linestyle='--')

# Etiquetas bien organizadas
ax1.set_xticks(range(len(frecuencias.index)))
ax1.set_xticklabels(frecuencias.index, rotation=45, ha='right')

plt.tight_layout()

st.subheader("📈 Gráfico de Pareto")
st.pyplot(fig)

st.title("Análisis de Problemas en Eventos")

st.subheader("Diagrama de Ishikawa - Retrasos")

st.image(
    "images/ishikawa_retrasos.png",
    caption="Causas de retrasos en los eventos",
    use_container_width=True
)

