# app.py - Streamlit demo for CubeSim
import streamlit as st
from cubesim import create_circular_orbit, plot_orbit_2d, propagate_orbit, power_profile
import matplotlib.pyplot as plt
import pandas as pd
from astropy import units as u

st.set_page_config(page_title="CubeSim — CubeSat Mission Designer", layout="wide")
st.title("CubeSim — Interactive CubeSat Mission Designer & Simulator 🚀")
st.write("Design a CubeSat mission (LEO), simulate orbits and power budget. Built with poliastro + Streamlit.")

# Sidebar inputs
st.sidebar.header("Mission Parameters")
alt_km = st.sidebar.slider("Altitude (km)", min_value=160, max_value=1200, value=500, step=10)
inc_deg = st.sidebar.slider("Inclination (deg)", min_value=0, max_value=180, value=51, step=1)
duration_min = st.sidebar.slider("Simulate duration (minutes)", min_value=60, max_value=1440, value=240, step=60)
payload_w = st.sidebar.number_input("Payload Power Consumption (W)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
panel_area = st.sidebar.number_input("Solar Panel Area (m²)", min_value=0.01, max_value=2.0, value=0.1, step=0.01)
panel_eff = st.sidebar.slider("Panel Efficiency", 0.05, 0.40, 0.25)
battery_Wh = st.sidebar.number_input("Battery Capacity (Wh)", min_value=1.0, max_value=200.0, value=20.0, step=1.0)

if st.sidebar.button("Run Simulation"):
    orbit = create_circular_orbit(alt_km, inc_deg)
    st.subheader("Orbit Summary")
    st.write({
        "Semi-major axis (km)": float(orbit.a.to(u.km).value),
        "Eccentricity": float(orbit.ecc),
        "Inclination (deg)": float(orbit.inc.to(u.deg).value),
        "Epoch": str(orbit.epoch)
    })
    # Plot groundtrack (approx)
    fig = plot_orbit_2d(orbit, duration_minutes=duration_min, step_seconds=30)
    st.pyplot(fig)

    # Power sim
    times, rr = propagate_orbit(orbit, duration_minutes=duration_min, step_seconds=30)
    gen, cons, soc, in_sun = power_profile(orbit, times, payload_power_w=payload_w,
                                           solar_panel_area_m2=panel_area, panel_efficiency=panel_eff,
                                           battery_capacity_Wh=battery_Wh)
    df = pd.DataFrame({
        "time": [str(t.utc.iso) for t in times],
        "generation_W": gen,
        "consumption_W": cons,
        "battery_soc_Wh": soc,
        "in_sun": in_sun
    })
    st.subheader("Power Profile (sample)")
    st.dataframe(df.head(200))

    # Plots
    st.subheader("Power & Battery")
    fig2, ax = plt.subplots(2,1, figsize=(10,6), sharex=True)
    ax[0].plot(gen, label="Generation (W)")
    ax[0].plot(cons, label="Consumption (W)")
    ax[0].legend()
    ax[0].set_ylabel("Power (W)")
    ax[1].plot(soc, label="Battery SoC (Wh)")
    ax[1].set_ylabel("SoC (Wh)")
    ax[1].set_xlabel("Time step")
    st.pyplot(fig2)

    if soc.min() < battery_Wh * 0.1:
        st.warning("Battery SoC drops under 10% at some point — consider larger panels or lower payload power.")
    else:
        st.success("Battery SoC stays healthy during simulation period.")
