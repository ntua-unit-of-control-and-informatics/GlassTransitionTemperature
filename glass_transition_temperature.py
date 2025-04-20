import streamlit as st
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

def density_hyperbola(x, rho0, t0, alpha, bita, gamma):
    dT = x - t0
    H0 = 0.5 * dT + np.sqrt(0.25 * dT * dT + np.exp(gamma))
    rho = rho0 - alpha * dT - bita * H0
    return rho

st.header("Glass transition temperature from density vs temperature data")

st.text("This WebApp was created by Evangelos Voyiatzis.")

# Add interactive elements
with st.form("myform"):
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"], help="This is text for help")
    option = st.selectbox("Y-data are about:" , ("Density", "Specific Volume"))
    submit = st.form_submit_button("Plot data")
    if submit:
        if uploaded_file is not None:
            input_stream = uploaded_file.getvalue().decode('utf-8').replace(",", "").split()
            x = [float(i) for i in input_stream[0::2]]
            if option=="Density":
                y = [float(i) for i in input_stream[1::2]]
            else:
                y = [1.0/float(i) for i in input_stream[1::2]]
            st.session_state['data'] = pd.DataFrame({'x': x, 'y': y})
        else:
            st.write("you need to upload a valid txt or csv file")

# Plot the data
if 'data' in st.session_state:
    with st.form("myform2"):
        st.line_chart(st.session_state['data'].set_index('x'), x_label = "Temperature", y_label = "Density")
        submit2 = st.form_submit_button("Fit hyberpola")
        if submit2:
            param, param_cov = curve_fit(density_hyperbola, st.session_state['data']['x'], st.session_state['data']['y'])
            st.write(f"The predicted Tg value is {param[1]:.4f} ")
            st.write(f"The values of the parameters are: \n\
            \N{GREEK SMALL LETTER RHO}_0: {param[0]:.4f}\n\
            \N{GREEK SMALL LETTER ALPHA}: {param[2]:.4f}\n\
            \N{GREEK SMALL LETTER BETA}: {param[3]:.4f}\n\
            \N{GREEK SMALL LETTER GAMMA}: {param[4]:.4f}")

if st.button("Reset"):
    if 'data' in st.session_state:
        del st.session_state['data']
    st.rerun()

