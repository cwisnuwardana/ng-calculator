import streamlit as st

st.title("Natural Gas Engineering Tool SUTO S401")
st.caption("Developed by Cahyadi Wisnu Wardana")

# =========================
# INPUT GAS
# =========================
st.header("Gas Composition (%)")
ch4 = st.number_input("CH4 (Methane)", value=90.0)
c2h6 = st.number_input("C2H6 (Ethane)", value=4.72)
c3h8 = st.number_input("C3H8 (Propane)", value=2.0)
c4h10 = st.number_input("C4H10 (Butane)", value=0.5)
n2 = st.number_input("N2 (Nitrogen)", value=1.8)
co2 = st.number_input("CO2 (Carbon Dioxed)", value=0.7)
c5h12 = st.number_input("C5H12 (Pentane)", value=0.16)
c6h14 = st.number_input("C6H14 (Hexane)", value=0.12)
c7h16 = st.number_input("C7H16 (n-Heptane)", value=0.0)
c8h18 = st.number_input("C8H18 (3-Methylheptane)", value=0.0)
h2o = st.number_input("H2O (Water)", value=0.0)
h2s = st.number_input("H2S (Hydrogen Sulfide)", value=0.0)
st.info("Note: Total Gas Composition must 100% -see result in detail")

# =========================
# PROCESS CONDITION
# =========================
st.header("Process Condition")
P_bar = st.number_input("Pressure (bar abs)", value=7.0)
T_C = st.number_input("Temperature (deg C)", value=35.0)
Z = st.number_input("Z factor", value=1.0)
price = st.number_input("Gas Price (Rp/Nm3)", value=10000)

# =========================
# AUTO CONVERSION (ANTI ERROR)
# =========================
P = P_bar*100000     # bar to pa
T = T_C + 273.15     # deg C to K   

# =========================
# CALCULATION
# =========================
# CALCULATION
totalgas = (ch4 + c2h6 + c3h8 + c4h10 + n2 + co2 + c5h12 + c6h14 + c7h16 + c8h18 +h2s)
M = (ch4*16 + c2h6*30 + c3h8*44 + c4h10*58 + n2*28 + co2*44 + c5h12*72 + c6h14*86 + c7h16*100 + c8h18*114 +h2o*18.016 +h2s*34.08)/100
Rs = 8.314 / (M/1000)
rho = P / (Rs * T * Z)
energy = 35 * (ch4/100)
cost = price * 100

# OUTPUT
st.header("Result")

st.metric("Total Gas Composition:", f"{totalgas:.2f} %")
st.metric("Mmix (g/mol)", f"{M:.2f}")
st.metric("Gas Constant Rs (J/kg·K)", f"{Rs:.2f}")
st.metric("Density (kg/m³)", f"{rho:.2f}")

st.write(f"Energy: {energy:.2f} MJ/Nm³")
st.write(f"Cost: Rp {cost:,.0f}/h")

# =========================
# STATUS
# =========================
if M < 19:
    st.success("Lean Gas (Dry Gas)")
else:
    st.warning("Rich Gas (Wet Gas)")

# =========================
# RECOMENDATION
# =========================
st.header("S401 Recommendation")
st.write(f"Set Rs = {round(Rs)} J/kg.K")

# =========================
# Error reading
# =========================
actual = st.number_input("Actual Flow (reference)", value=100.0)
measured = st.number_input("Measured Flow (S401)", value=100.0)

error = (measured - actual) / actual * 100

st.metric("Error (%)", f"{error:.2f}")

# =========================
# VALIDATION
# =========================

if abs(totalgas - 100) > 0.1:
    st.error(f"Total Gas Composition = {totalgas:.2f}% (Harus 100%)")
else :
    st.success("Total Composition Gas 0K (100%)")
                                        
st.info("Note: Pressure auto convert bar to Pa, Temperature auto convert deg C to K")
st.info("Note: Calculation based on idel gas approximation. For PGN pipeline typical accuracy +/-2-5%.")

import pandas as pd

st.header("Gas Component Reference")

data = {
    "Component": [
        "CH4", "C2H6", "C3H8", "C4H10",
        "C5H12", "C6H14", "N2", "CO2"
    ],
    "Name": [
        "Methane", "Ethane", "Propane", "Butane",
        "Pentane", "Hexane", "Nitrogen", "Carbon Dioxide"
    ],
    "M (g/mol)": [16, 30, 44, 58, 72, 86, 28, 44],
    "Category": [
        "Light Gas", "Light Gas", "Medium", "Medium",
        "Heavy", "Heavy", "Inert", "Acid Gas"
    ],
    "Phase Risk": [
        "Gas", "Gas", "Gas", "Gas",
        "⚠️ Condensate", "⚠️ Condensate", "Gas", "Gas"
    ]
}

df = pd.DataFrame(data)

# 🎨 Styling
def highlight(row):
    if row["Category"] == "Heavy":
        return ["background-color: #ffcccc"] * len(row)
    elif row["Category"] == "Medium":
        return ["background-color: #fff2cc"] * len(row)
    elif row["Category"] == "Light Gas":
        return ["background-color: #d9ead3"] * len(row)
    else:
        return [""] * len(row)

styled_df = df.style.apply(highlight, axis=1)

st.dataframe(styled_df, use_container_width=True)

st.info("Light Gas = Stable | Heavy (C5+) = Potential Condensation Risk")
 








