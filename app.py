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
totalgas = (ch4 + c2h6 + c3h8 + c4h10 + n2 + co2 + c5h12 + c6h14)
M = (ch4*16 + c2h6*30 + c3h8*44 + c4h10*58 + n2*28 + co2*44 + c5h12*72 + c6h14*72)/100
Rs = 8.314 / (M/1000)
rho = (P*100000) / (Rs * T * Z)
energy = 35 * (ch4/100)
cost = price * 100

# OUTPUT
st.header("Result")
st.write(f"Total Gas Composition: {totalgas:.2f} %")
st.write(f"Mmix: {M:.2f} g/mol")
st.write(f"Rs: {Rs:.2f} J/kg.K")
st.write(f"Density: {rho:.2f} kg/m3")
st.write(f"Energy: {energy:.2f} MJ/Nm3")
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
# VALIDATION
# =========================

if abs(totalgas - 100) > 0.1:
    st.error(f"Total Gas Composition = {total:.2f}% (Harus 100%)")
else :
    st.success("Total Composition Gas 0K (100%)")
                                        
st.info("Note: Pressure auto convert bar to Pa, Temperature auto convert deg C to K")
st.info("M (g/mol) CH4=16, C2H6=30, C3H8=44, C4H10=58, N2=28, C5H12=72,C6H14=72")    
st.info("Note: Calculation based on idel gas approximation. For PGN pipeline typical accuracy +/-2-5%.")

 








