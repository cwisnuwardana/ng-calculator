from PIL import Image
import streamlit as st

# Load logo
logo = Image.open("suto_logo.png")

# Display
st.image(logo, use_container_width=True)

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
st.header("Error Reading")
actual = st.number_input("Actual Flow (reference)", value=100.0)
measured = st.number_input("Measured Flow (S401)", value=100.0)

error = (measured - actual) / actual * 100

st.metric("Error (%)", f"{error:.2f}")

R_actual = Rs   # dari kalkulasi
R_set = st.number_input("Rₛ di S401", value=460.0)

error = (R_actual / R_set - 1) * 100

st.metric("Error akibat Rₛ (%)", f"{error:.2f}")

# =========================
# VALIDATION
# =========================

if abs(totalgas - 100) > 0.1:
    st.error(f"Total Gas Composition = {totalgas:.2f}% (Harus 100%)")
else :
    st.success("Total Composition Gas 0K (100%)")
                                        
import pandas as pd

st.header("Gas Component Reference")

data = {
    "Component": [
        "CH4","C2H6","C3H8","C4H10",
        "C5H12","C6H14","C7H16","C8H18",
        "N2","CO2","H2O","H2S"
    ],
    "Name": [
        "Methane","Ethane","Propane","Butane",
        "Pentane","Hexane","Heptane","Octane",
        "Nitrogen","Carbon Dioxide","Water","Hydrogen Sulfide"
    ],
    "M (g/mol)": [
        16,30,44,58,72,86,100,114,28,44,18,34
    ]
}

df = pd.DataFrame(data)

# =========================
# CATEGORY LOGIC
# =========================
def category(comp):
    if comp in ["CH4","C2H6"]:
        return "Light Gas"
    elif comp in ["C3H8","C4H10"]:
        return "Medium"
    elif comp.startswith("C") and len(comp) > 3:
        return "Heavy (C5+)"
    elif comp == "N2":
        return "Inert"
    elif comp in ["CO2","H2S"]:
        return "Acid Gas"
    else:
        return "-"

# =========================
# PHASE RISK LOGIC
# =========================
def phase_risk(comp):
    if comp in ["C5H12","C6H14","C7H16","C8H18"]:
        return "⚠️ Condensate"
    elif comp == "H2O":
        return "⚠️ Condensate"
    elif comp == "H2S":
        return "⚠️ Risk (corrosion)"
    else:
        return "Gas"

df["Category"] = df["Component"].apply(category)
df["Phase Risk"] = df["Component"].apply(phase_risk)

# =========================
# COLOR STYLE
# =========================
def highlight(row):
    if "Heavy" in row["Category"]:
        return ["background-color: #ffcccc"] * len(row)
    elif row["Category"] == "Medium":
        return ["background-color: #fff2cc"] * len(row)
    elif row["Category"] == "Light Gas":
        return ["background-color: #d9ead3"] * len(row)
    else:
        return [""] * len(row)

styled_df = df.style.apply(highlight, axis=1)

st.dataframe(styled_df, use_container_width=True)

st.header("⚠️ Gas Quality Warning System")

# =========================
# INPUT (pakai variabel kamu)
# =========================
heavy = c5h12 + c6h14      # bisa ditambah C7, C8 kalau ada
co2_level = co2
h2s_level = st.session_state.get("h2s", 0)  # kalau ada input H2S

# =========================
# RULE ENGINE
# =========================

# 1. Condensate Risk
if heavy > 1:
    st.error("⚠️ HIGH Condensate Risk (C5+ > 1%)")
elif heavy > 0.3:
    st.warning("⚠️ Moderate Condensate Risk")
else:
    st.success("✅ Low Condensate Risk")

# 2. CO2 Quality
if co2_level > 4:
    st.error("⚠️ High CO2 → Calorific Value Drop")
elif co2_level > 2:
    st.warning("⚠️ CO2 Increasing (monitor)")
else:
    st.success("✅ CO2 Normal")

# 3. H2S Safety
if h2s_level > 0:
    st.error("☠️ H2S DETECTED → Corrosion & Safety Risk")
else:
    st.success("✅ No H2S detected")

# 4. Overall Status
st.subheader("Overall Assessment")

if heavy > 1 or co2_level > 4 or h2s_level > 0:
    st.error("🚨 GAS CONDITION: ATTENTION REQUIRED")
elif heavy > 0.3 or co2_level > 2:
    st.warning("⚠️ GAS CONDITION: MONITORING")
else:
    st.success("✅ GAS CONDITION: STABLE")

st.header("🧠 Smart Recommendation")

recommendations = []

# =========================
# CONDENSATE
# =========================
if heavy > 1:
    recommendations.append("➡️ Install / check separator (liquid removal)")
    recommendations.append("➡️ Check gas temperature (avoid drop below dew point)")
elif heavy > 0.3:
    recommendations.append("➡️ Monitor condensate risk (C5+ increasing)")

# =========================
# CO2
# =========================
if co2_level > 4:
    recommendations.append("➡️ Evaluate gas treatment (CO2 removal)")
    recommendations.append("➡️ Expect lower calorific value")
elif co2_level > 2:
    recommendations.append("➡️ Monitor CO2 trend (quality slightly decreasing)")

# =========================
# H2S
# =========================
if h2s_level > 0:
    recommendations.append("➡️ Immediate corrosion check required")
    recommendations.append("➡️ Ensure H2S safety compliance (PPE, detector)")

# =========================
# GAS CONSTANT (Rs)
# =========================
if abs(error) > 2:
    recommendations.append(f"➡️ Adjust Rs setting (current error {error:.2f}%)")

# =========================
# GENERAL
# =========================
if len(recommendations) == 0:
    st.success("✅ No action required (Gas condition optimal)")
else:
    for rec in recommendations:
        st.write(rec)

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.header("📄 Generate Report")

if st.button("Generate PDF Report"):

    styles = getSampleStyleSheet()
    content = []

    # =========================
    # TITLE
    # =========================
    content.append(Paragraph("<b>Natural Gas Analysis Report SUTO iTec Indonesia</b>", styles["Title"]))
    content.append(Spacer(1,12))

    # =========================
    # SUMMARY AUTO
    # =========================
    summary_text = f"""
    Gas composition indicates methane dominant (~{ch4:.2f}%).
    CO2 level at {co2:.2f}%.
    Heavy component (C5+) at {heavy:.2f}%.
    """

    content.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    content.append(Paragraph(summary_text, styles["Normal"]))
    content.append(Spacer(1,12))

    # =========================
    # WARNING SUMMARY
    # =========================
    status = "STABLE"
    if heavy > 1 or co2 > 4 or h2s_level > 0:
        status = "ATTENTION REQUIRED"
    elif heavy > 0.3 or co2 > 2:
        status = "MONITORING"

    content.append(Paragraph("<b>Gas Condition</b>", styles["Heading2"]))
    content.append(Paragraph(status, styles["Normal"]))
    content.append(Spacer(1,12))

    # =========================
    # RECOMMENDATION AUTO
    # =========================
    rec_text = ""

    if heavy > 1:
        rec_text += "- Check separator / condensate removal<br/>"
    elif heavy > 0.3:
        rec_text += "- Monitor condensate risk<br/>"

    if co2 > 4:
        rec_text += "- Evaluate CO2 treatment<br/>"
    elif co2 > 2:
        rec_text += "- Monitor CO2 trend<br/>"

    if h2s_level > 0:
        rec_text += "- Check corrosion & safety system<br/>"

    if abs(error) > 2:
        rec_text += f"- Adjust Rs setting (error {error:.2f}%)<br/>"

    if rec_text == "":
        rec_text = "No action required"

    content.append(Paragraph("<b>Recommendation</b>", styles["Heading2"]))
    content.append(Paragraph(rec_text, styles["Normal"]))
content.append,(Paragraph("<b>By: Cahyadi Wisnu Wardana"</b>", styles["Heading2"]))
    
    
    # =========================
    # SAVE FILE
    # =========================
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(tmp_file.name)
    doc.build(content)

    with open(tmp_file.name, "rb") as f:
        st.download_button("📥 Download Report", f, file_name="NG_Report.pdf")

# =========================
# INFO BOX
# =========================
st.info("Light Gas = Stable | Medium = Transitional | Heavy (C5+) = Condensate Risk")

st.info("Light Gas = Stable | Heavy (C5+) = Potential Condensation Risk")
st.info("Note: Pressure auto convert bar to Pa, Temperature auto convert deg C to K")
st.info("Note: Calculation based on ideal gas approximation. For PGN pipeline typical accuracy +/-2-5%.")
 








