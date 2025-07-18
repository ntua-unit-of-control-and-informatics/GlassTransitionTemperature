import streamlit as st
import altair as alt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

def convert_temperature(units, temperature):
    """A function to convert temperature from input units to Kelvin"""

    if units == "Celcius":
        new_temperature = [x + 273.15 for x in temperature]
    elif units == "Fahrenheit":
        new_temperature = [(x - 32.0) / 1.8 + 273.15 for x in temperature]
    elif units == "Rankine":
        new_temperature = [x / 1.8 for x in temperature]
    else:
        new_temperature = [x for x in temperature]

    return new_temperature

def density_hyperbola(x, rho0, t0, alpha, bita, gamma):
    dT = x - t0
    H0 = 0.5 * dT + np.sqrt(0.25 * dT * dT + np.exp(gamma))
    rho = rho0 - alpha * dT - bita * H0
    return rho

st.header("Glass Transition Temperature App")

st.markdown("The implemented method is based on the work of Patrone *et al* (P.N. Patrone, A. Dienstfrey, A.R. Browning, S. Tucker, S. Christensen \"Uncertainty Quantification in Molecular Dynamics Studies of the Glass Transition Temperature\" Polymer 87 (2016) 246-259). It assumes that a single hyberpola, as defined by Eq. (1) in Patrone *et al* and shown below, fits density vs temperature data for the entire temperature range.")
st.markdown("$\\rho \\left(T \\right) = \\rho_0 - \\alpha \\left( T - T_0 \\right) -\\beta H\\left(T, T_0, \\gamma \\right)$\n")
st.markdown("$H\\left(T, T_0, \\gamma \\right) = \\frac{1}{2} \\left( T - T_0 \\right) + \\sqrt{\\frac{\\left( T - T_0 \\right)^2}{4} + \\exp(\\gamma)}$")

st.markdown("This WebApp was created by Evangelos Voyiatzis.")

# Add interactive elements
with st.form("myform"):
    help_str = "The decimal separator must be a dot and not a comma. The file is assumed to have two columns of equal length: the first is the temperature and the second the density or the specific volume "
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"], help=help_str)
    option = st.selectbox("Y-data are about:" , ("Density", "Specific Volume"))
    temperature_option = st.selectbox("Temperature unit" , ("Kelvin", "Celcius", "Fahrenheit", "Rankine"))
    submit = st.form_submit_button("Plot data")
    if submit:
        if uploaded_file is not None:
            input_stream = uploaded_file.getvalue().decode('utf-8').replace(",", "").split()
            x = [float(i) for i in input_stream[0::2]]
            x = convert_temperature(temperature_option, x)
            if option == "Density":
                y = [float(i) for i in input_stream[1::2]]
            else:
                y = [1.0/float(i) for i in input_stream[1::2]]
            st.session_state['data'] = pd.DataFrame({'Temperature': x, 'y': y})
        else:
            st.write("you need to upload a valid txt or csv file")

# Plot the data
if 'data' in st.session_state:
    with st.form("myform2"):
        fig1 = alt.Chart(st.session_state['data']).mark_point(filled=True).encode(x='Temperature',y='y') 
        submit2 = st.form_submit_button("Fit hyberpola")
        if submit2:
            try:
                param, param_cov = curve_fit(density_hyperbola, st.session_state['data']['Temperature'], st.session_state['data']['y'])
                y_from_fitting = density_hyperbola(st.session_state['data']['Temperature'], param[0], param[1], param[2], param[3], param[4])
                st.session_state['data_from_fitting'] = pd.DataFrame({'Temperature': st.session_state['data']['Temperature'], 'y_from_fitting': y_from_fitting})
                fig2 = alt.Chart(st.session_state['data_from_fitting']).mark_line(color='red').encode(x='Temperature',y='y_from_fitting')
                st.altair_chart((fig1 + fig2).interactive())
                st.write(f"The predicted glass transition temperature T\u2080 is {param[1]:.4f} Kelvin")
                st.write(f"The fitted values of the parameters are: \n\
                \N{GREEK SMALL LETTER RHO}\u2080: {param[0]:.4f}\n\
                \N{GREEK SMALL LETTER ALPHA}: {param[2]:.4f}\n\
                \N{GREEK SMALL LETTER BETA}: {param[3]:.4f}\n\
                \N{GREEK SMALL LETTER GAMMA}: {param[4]:.4f}")
            except RuntimeError as e:
                st.write("Optimal parameters not found")
        else:
            st.altair_chart(fig1.interactive())

if st.button("Reset"):
    if 'data' in st.session_state:
        del st.session_state['data']
    if 'data_from_fitting' in st.session_state:
        del st.session_state['data_from_fitting']
    st.rerun()
