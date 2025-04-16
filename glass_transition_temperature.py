import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import streamlit as st

def density_hyperbola(x, rho0, t0, alpha, bita, gamma):
    dT = x - t0
    H0 = 0.5 * dT + np.sqrt(0.25 * dT * dT + np.exp(gamma))
    rho = rho0 - alpha * dT - bita * H0
    return rho

st.header("Glass transition temperature from density vs temperature data")

st.text("This WebApp was created by Evangelos Voyiatzis.")



