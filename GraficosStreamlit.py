import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de página
st.set_page_config(layout="wide")

def plot_radar_chart(data, criteria):
    labels = np.array(criteria)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))  # Aumenta el tamaño del gráfico
    
    for index, row in data.iterrows():
        values = row.tolist()
        values += values[:1]  # Cerrar el gráfico
        ax.plot(angles + [angles[0]], values, label=index, linewidth=2)
        ax.fill(angles + [angles[0]], values, alpha=0.2)
    
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=20)  # Aumenta el tamaño de las etiquetas del eje
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=16)  # Aumenta el tamaño de las etiquetas del eje Y
    plt.title("Gráfico Spider", fontsize=20, pad=20)  # Aumenta el tamaño del título
    plt.legend(loc="lower left", bbox_to_anchor=(-0.2, 0), fontsize=14)  # Aumenta el tamaño de la leyenda
    st.pyplot(fig)

def plot_heatmap(data):
    # Asegúrate de que todos los valores sean numéricos
    data = data.apply(pd.to_numeric, errors='coerce')  # Convertir a numérico, reemplazando valores no convertibles por NaN
    fig, ax = plt.subplots(figsize=(10, 5))  # Aumenta el tamaño del gráfico para aprovechar el ancho
    sns.heatmap(data, annot=True, cmap="RdYlGn", linewidths=1, cbar=True)
    plt.title("Mapa de Calor", fontsize=20)  # Aumenta el tamaño del título
    plt.xlabel("Criterios", fontsize=20)  # Aumenta el tamaño de la etiqueta del eje X
    plt.ylabel("Alternativas", fontsize=20)  # Aumenta el tamaño de la etiqueta del eje Y
    st.pyplot(fig)

st.title("Evaluación de Alternativas")

# Dividir la pantalla en dos columnas con más espacio para los gráficos
col1, col2 = st.columns([2, 3])  # Columna derecha más ancha para los gráficos

with col1:
    # Entrada del número de criterios
    num_criteria = st.number_input("Número de criterios a evaluar", min_value=1, max_value=10, value=4, step=1)
    criteria = [st.text_input(f"Nombre del criterio {i+1}", f"Criterio {i+1}") for i in range(num_criteria)]
    
    # Entrada de alternativas
    num_alternatives = st.number_input("Número de alternativas", min_value=1, max_value=10, value=3, step=1)
    alternatives = [st.text_input(f"Nombre de la alternativa {i+1}", f"Alternativa {i+1}") for i in range(num_alternatives)]
    
    # Entrada de puntajes en columnas
    data = pd.DataFrame(columns=criteria, index=alternatives)
    st.write("Ingrese los puntajes para cada alternativa según cada criterio:")
    num_columns = 2 if num_criteria % 2 == 0 else 3
    columns = st.columns(num_columns)
    
    for i, crit in enumerate(criteria):
        col = columns[i % num_columns]
        with col:
            for alt in alternatives:
                data.at[alt, crit] = st.number_input(f"{crit} ({alt})", min_value=0, max_value=10, value=5, step=1)

with col2:
    # Mostrar gráficos si el usuario lo solicita
    if st.button("Generar gráficos"):
        st.subheader("Gráfico Spider")
        plot_radar_chart(data, criteria)
        st.subheader("Mapa de Calor")
        plot_heatmap(data)
