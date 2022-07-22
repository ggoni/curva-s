import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit,fsolve
import matplotlib.pyplot as plt

st.title("Solver para Curva S")



st.sidebar.header("Opciones")

options_form = st.sidebar.form("options_form")


st.markdown(
    """
    <style>
        .css-9ycgxx::after {
            content: "/ Subir planilla de datos";
        }
    <style>
    """, unsafe_allow_html=True)



fileup = st.sidebar.file_uploader(label="Subir planilla",
                        type=['xlsx','xls','csv'],
                        help="Esta versión recibe archivos en excel como insumo")

if fileup is not None:
    df = pd.read_excel(fileup)
    st.write(df)
    df = df.tail(len(df)-1)

    smin, smax, t0 = df.Real.min(), 1, df.W.min()

    def s_curve(t,k,a):

        return smin + (smax-smin)*(1/(1 + np.exp(-k*(t-t0))))**a



    popt, _ = curve_fit(s_curve,df.W,df.Real)

    Pred = s_curve(df.W,popt[0],popt[1])

    fig, ax = plt.subplots()
    plt.scatter(df.W,df.Real, label= "Real")
    plt.plot(df.W, Pred,color='red', linestyle='--', label ="Proyección");
    plt.plot(df.W, df.Plan,color='black',label = "Plan")    
    plt.legend(loc="upper left")
    
    st.pyplot(fig)


    def fitted_s_curve(t,k=popt[0],a=popt[1]):
        return smin + (smax-smin)*(1/(1 + np.exp(-k*(t-t0))))**a



    def pending(t):
        return 0.995 - fitted_s_curve(t)

    valor = df.W.max()

    root = fsolve(pending,valor)
    
    
    final_week = round(root[0])
    st.markdown(f"Al ritmo actual, el proyecto se terminaría en la semana **{final_week}**")
    
