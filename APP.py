import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sympy import symbols, sympify

# ==================================================
# CONFIGURACION
# ==================================================

st.set_page_config(
    page_title="Metodos Numericos",
    layout="wide"
)

# ==================================================
# MENU LATERAL
# ==================================================

st.sidebar.title("📘 Métodos Numéricos")

metodo = st.sidebar.radio(
    "Seleccione un método",
    [
        "Metodo de Biseccion",
        "Metodo de Falsa Posicion"
    ]
)
# ==================================================
# METODO DE BISECCION
# ==================================================

def biseccion():

    st.title("Metodo de Biseccion")

    # ENTRADAS
    funcion = st.text_input(
        "Ingrese la funcion",
        "x**2 - 2",
        key="bi_funcion"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        a_input = st.number_input(
            "Valor de A",
            value=1.0,
            key="bi_a"
        )

    with col2:
        b_input = st.number_input(
            "Valor de B",
            value=2.0,
            key="bi_b"
        )

    with col3:
        tolerancia = st.number_input(
            "Tolerancia",
            value=0.00001,
            format="%.10f",
            key="bi_tol"
        )

    # SESSION STATE
    if "fp_calcular" not in st.session_state:
        st.session_state.fp_calcular = False

    # BOTON
    if st.button(
        "Calcular",
        key="fp_btn"
    ):
        st.session_state.fp_calcular = True

    # EJECUCION
    if st.session_state.fp_calcular:

        try:

            x = symbols('x')

            f = sympify(funcion)

            fa_inicial = float(f.subs(x, a_input))
            fb_inicial = float(f.subs(x, b_input))

            if fa_inicial * fb_inicial > 0:

                st.error(
                    "El intervalo no contiene una raiz."
                )

            else:

                datos = []

                x_anterior = 0

                max_iter = 100

                a = a_input
                b = b_input

                for i in range(1, max_iter + 1):

                    # PUNTO MEDIO
                    xm = (a + b) / 2

                    # EVALUACIONES
                    fa = float(f.subs(x, a))
                    fx = float(f.subs(x, xm))
                    fb = float(f.subs(x, b))

                    # PRODUCTO
                    producto = fa * fx

                    # ERROR
                    if i == 1:

                        error = 0
                        error_porcentaje = 0

                    else:

                        error = abs(
                            (xm - x_anterior) / xm
                        )

                        error_porcentaje = (
                            error * 100
                        )

                    # CONVERGENCIA
                    converge = (
                        "SI"
                        if error < tolerancia and i != 1
                        else "NO"
                    )

                    # GUARDAR
                    datos.append({
                        "Iteracion": i,
                        "A": a,
                        "X": xm,
                        "B": b,
                        "f(A)": fa,
                        "f(X)": fx,
                        "f(B)": fb,
                        "f(A)*f(X)": producto,
                        "Error": error,
                        "Error %": error_porcentaje,
                        "Converge": converge
                    })

                    # DETENER
                    if converge == "SI":
                        break

                    # ACTUALIZAR
                    if producto < 0:
                        b = xm
                    else:
                        a = xm

                    x_anterior = xm

                # TABLA
                tabla = pd.DataFrame(datos)

                st.subheader(
                    "Tabla de Iteraciones"
                )

                st.dataframe(
                    tabla.style.format({
                        "A": "{:.6f}",
                        "X": "{:.6f}",
                        "B": "{:.6f}",
                        "f(A)": "{:.6f}",
                        "f(X)": "{:.6f}",
                        "f(B)": "{:.6f}",
                        "f(A)*f(X)": "{:.6f}",
                        "Error": "{:.10f}",
                        "Error %": "{:.6f} %"
                    }),
                    width='stretch',
                    height=450
                )

                # VISUALIZACION
                st.subheader(
                    "Visualizacion de Iteraciones"
                )

                iteracion_visual = st.slider(
                    "Iteración",
                    min_value=1,
                    max_value=len(tabla),
                    value=len(tabla)
                )

                fila = tabla.iloc[
                    iteracion_visual - 1
                ]

                # DATOS
                a_graf = fila["A"]
                x_graf = fila["X"]
                b_graf = fila["B"]

                fa_graf = fila["f(A)"]
                fx_graf = fila["f(X)"]
                fb_graf = fila["f(B)"]

                # ZOOM X
                margen_x = abs(
                    b_graf - a_graf
                )

                if margen_x < 0.02:
                    margen_x = 0.02

                x_min = a_graf - margen_x
                x_max = b_graf + margen_x

                # VALORES
                x_vals = np.linspace(
                    x_min,
                    x_max,
                    1000
                )

                y_vals = [
                    float(f.subs(x, val))
                    for val in x_vals
                ]

                # FIGURA
                fig, ax = plt.subplots(
                    figsize=(12, 7)
                )

                # FUNCION
                ax.plot(
                    x_vals,
                    y_vals,
                    color='blue',
                    linewidth=2.5,
                    label='f(x)'
                )

                # PUNTOS
                ax.scatter(
                    a_graf,
                    fa_graf,
                    color='red',
                    s=120,
                    zorder=5,
                    label='A'
                )

                ax.scatter(
                    x_graf,
                    fx_graf,
                    color='orange',
                    s=120,
                    zorder=5,
                    label='X'
                )

                ax.scatter(
                    b_graf,
                    fb_graf,
                    color='green',
                    s=120,
                    zorder=5,
                    label='B'
                )

                # LINEAS VERTICALES
                ax.vlines(
                    a_graf,
                    0,
                    fa_graf,
                    colors='red',
                    linestyles='dashed'
                )

                ax.vlines(
                    x_graf,
                    0,
                    fx_graf,
                    colors='orange',
                    linestyles='dashed'
                )

                ax.vlines(
                    b_graf,
                    0,
                    fb_graf,
                    colors='green',
                    linestyles='dashed'
                )

                # ZOOM Y
                y_puntos = [
                    fa_graf,
                    fx_graf,
                    fb_graf
                ]

                y_min = min(y_puntos)
                y_max = max(y_puntos)

                margen_y = abs(
                    y_max - y_min
                )

                if margen_y < 0.05:
                    margen_y = 0.05

                ax.set_ylim(
                    y_min - margen_y,
                    y_max + margen_y
                )

                ax.set_xlim(
                    x_min,
                    x_max
                )

                # GRID
                ax.grid(
                    True,
                    linestyle='--',
                    alpha=0.5
                )

                # EJE X
                ax.axhline(
                    0,
                    color='black',
                    linewidth=1.5
                )

                # EJE Y
                eje_y_posicion = x_min

                ax.vlines(
                    eje_y_posicion,
                    y_min - margen_y,
                    y_max + margen_y,
                    colors='black',
                    linewidth=1.5
                )

                # LINEAS HORIZONTALES
                ax.plot(
                    [eje_y_posicion, a_graf],
                    [fa_graf, fa_graf],
                    color='red',
                    linestyle='dotted'
                )

                ax.plot(
                    [eje_y_posicion, x_graf],
                    [fx_graf, fx_graf],
                    color='orange',
                    linestyle='dotted'
                )

                ax.plot(
                    [eje_y_posicion, b_graf],
                    [fb_graf, fb_graf],
                    color='green',
                    linestyle='dotted'
                )

                # ETIQUETAS
                ax.annotate(
                    f"A\nx={a_graf:.4f}\ny={fa_graf:.4f}",
                    (a_graf, fa_graf),
                    textcoords="offset points",
                    xytext=(-55, -35),
                    fontsize=10,
                    color='red',
                    fontweight='bold',
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        fc="white",
                        ec="red",
                        alpha=0.9
                    )
                )

                ax.annotate(
                    f"X\nx={x_graf:.4f}\ny={fx_graf:.4f}",
                    (x_graf, fx_graf),
                    textcoords="offset points",
                    xytext=(10, 15),
                    fontsize=10,
                    color='orange',
                    fontweight='bold',
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        fc="white",
                        ec="orange",
                        alpha=0.9
                    )
                )

                ax.annotate(
                    f"B\nx={b_graf:.4f}\ny={fb_graf:.4f}",
                    (b_graf, fb_graf),
                    textcoords="offset points",
                    xytext=(10, -30),
                    fontsize=10,
                    color='green',
                    fontweight='bold',
                    bbox=dict(
                        boxstyle="round,pad=0.3",
                        fc="white",
                        ec="green",
                        alpha=0.9
                    )
                )

                # TITULO
                ax.set_title(
                    f"Metodo de Biseccion - Iteracion {iteracion_visual}",
                    fontsize=18,
                    fontweight='bold'
                )

                # EJES
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")

                # LEYENDA
                ax.legend(
                    fontsize=10,
                    loc='upper right'
                )

                # MOSTRAR
                st.pyplot(fig)

                # RAIZ
                raiz_final = tabla.iloc[-1]["X"]

                st.success(
                    f"Raiz final aproximada = {raiz_final:.10f}"
                )

        except Exception as e:

            st.error(
                f"Error en la funcion: {e}"
            )

# ==================================================
# METODO DE FALSA POSICION
# ==================================================

def falsa_posicion():

    st.title("Metodo de Falsa Posicion")

    funcion = st.text_input(
        "Ingrese la funcion",
        "x**2 - 2",
        key="fp_funcion"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        a_input = st.number_input(
            "Valor de A",
            value=1.0,
            key="fp_a"
        )

    with col2:
        b_input = st.number_input(
            "Valor de B",
            value=2.0,
            key="fp_b"
        )

    with col3:
        tolerancia = st.number_input(
            "Tolerancia",
            value=0.00001,
            format="%.10f",
            key="fp_tol"
        )

    calcular = st.button(
        "Calcular",
        key="fp_btn"
    )

    if calcular:

        try:

            x = symbols('x')

            f = sympify(funcion)

            fa_inicial = float(f.subs(x, a_input))
            fb_inicial = float(f.subs(x, b_input))

            if fa_inicial * fb_inicial > 0:

                st.error(
                    "El intervalo no contiene una raiz."
                )

            else:

                datos = []

                x_anterior = 0

                max_iter = 100

                a = a_input
                b = b_input

                for i in range(1, max_iter + 1):

                    fa = float(f.subs(x, a))
                    fb = float(f.subs(x, b))

                    # FORMULA
                    xm = b - (
                        (fb * (a - b))
                        /
                        (fa - fb)
                    )

                    fx = float(f.subs(x, xm))

                    producto = fa * fx

                    if i == 1:

                        error = 0
                        error_porcentaje = 0

                    else:

                        error = abs(
                            (xm - x_anterior) / xm
                        )

                        error_porcentaje = (
                            error * 100
                        )

                    converge = (
                        "SI"
                        if error < tolerancia and i != 1
                        else "NO"
                    )

                    datos.append({
                        "Iteracion": i,
                        "A": a,
                        "X": xm,
                        "B": b,
                        "f(A)": fa,
                        "f(X)": fx,
                        "f(B)": fb,
                        "f(A)*f(X)": producto,
                        "Error": error,
                        "Error %": error_porcentaje,
                        "Converge": converge
                    })

                    if converge == "SI":
                        break

                    if producto < 0:
                        b = xm
                    else:
                        a = xm

                    x_anterior = xm

                tabla = pd.DataFrame(datos)

                st.subheader(
                    "Tabla de Iteraciones"
                )

                st.dataframe(
                    tabla.style.format({
                        "A": "{:.6f}",
                        "X": "{:.6f}",
                        "B": "{:.6f}",
                        "f(A)": "{:.6f}",
                        "f(X)": "{:.6f}",
                        "f(B)": "{:.6f}",
                        "f(A)*f(X)": "{:.6f}",
                        "Error": "{:.10f}",
                        "Error %": "{:.6f} %"
                    }),
                    width='stretch',
                    height=450
                )

                raiz_final = tabla.iloc[-1]["X"]

                st.success(
                    f"Raiz final aproximada = {raiz_final:.10f}"
                )

        except Exception as e:

            st.error(
                f"Error en la funcion: {e}"
            )

# ==================================================
# EJECUCION
# ==================================================

if metodo == "Metodo de Biseccion":
    biseccion()

elif metodo == "Metodo de Falsa Posicion":
    falsa_posicion()
    st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; color: gray; padding-top: 30px;'>
        © 2026 | Desarrollado por <b>Cumpa Smith (EL TRIPLE H)</b><br>
        Fisica • Métodos Numéricos • Python
    </div>
    """,
    unsafe_allow_html=True
)
                   
