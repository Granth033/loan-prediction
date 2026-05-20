import streamlit as st
import numpy as np
import pickle
import os
import plotly.graph_objects as go
import plotly.express as px

# ── Page config — MUST be first ───────────────────────────────────────────────
st.set_page_config(
    page_title="LoanIQ Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
  --bg0:     #020408;
  --bg1:     #060C14;
  --bg2:     #0B1420;
  --bg3:     #101D2E;
  --border:  #1A2D45;
  --border2: #243D5A;
  --cyan:    #00E5FF;
  --cyan2:   #00B8D4;
  --green:   #00FF9D;
  --green2:  #00C87A;
  --amber:   #FFB300;
  --red:     #FF3D5A;
  --text:    #CDD9E8;
  --muted:   #4A6380;
  --dim:     #2A3F58;
  --font:    'Outfit', sans-serif;
  --mono:    'IBM Plex Mono', monospace;
}

/* ── Hide Streamlit chrome ── */
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }
footer { display: none !important; }

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp { font-family: var(--font) !important; }

.stApp {
  background: var(--bg0) !important;
  color: var(--text);
}
.block-container {
  padding: 1.2rem 1.8rem 3rem !important;
  max-width: 1280px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg1); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

/* ── Top navbar ── */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0 1rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.4rem;
}
.nav-logo {
  font-family: var(--mono);
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--cyan);
  letter-spacing: 0.06em;
  display: flex;
  align-items: center;
  gap: 8px;
}
.nav-logo span { color: var(--muted); font-weight: 400; font-size: 0.75rem; }
.nav-pills { display: flex; gap: 6px; }
.nav-pill {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 4px 12px;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
}
.nav-pill.active { color: var(--cyan); border-color: var(--cyan); background: rgba(0,229,255,0.05); }
.nav-status {
  display: flex; align-items: center; gap: 6px;
  font-size: 0.72rem; color: var(--muted); font-family: var(--mono);
}
.status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green2);
  animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── KPI row ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 1.2rem;
}
.kpi-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem 1.2rem;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
}
.kpi-card:hover { border-color: var(--border2); transform: translateY(-1px); }
.kpi-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.kpi-card.cyan::before { background: linear-gradient(90deg, transparent, var(--cyan), transparent); }
.kpi-card.green::before { background: linear-gradient(90deg, transparent, var(--green), transparent); }
.kpi-card.amber::before { background: linear-gradient(90deg, transparent, var(--amber), transparent); }
.kpi-card.red::before { background: linear-gradient(90deg, transparent, var(--red), transparent); }
.kpi-label { font-size: 0.63rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.4rem; font-family: var(--mono); }
.kpi-value { font-size: 1.65rem; font-weight: 800; color: var(--text); line-height: 1; }
.kpi-sub { font-size: 0.7rem; color: var(--muted); margin-top: 0.3rem; }
.kpi-icon { position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); font-size: 1.6rem; opacity: 0.12; }

/* ── Panel cards ── */
.panel {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
  height: 100%;
}
.panel-title {
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--cyan);
  font-family: var(--mono);
  margin-bottom: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 0.7rem;
  border-bottom: 1px solid var(--border);
}
.panel-title::before { content: '▸'; }

/* ── Form elements ── */
div[data-testid="stSelectbox"] > div,
div[data-testid="stNumberInput"] > div,
div[data-testid="stSlider"] { margin-bottom: 2px !important; }

label, .stSelectbox label, .stNumberInput label, .stSlider label {
  font-size: 0.72rem !important;
  font-family: var(--mono) !important;
  color: var(--muted) !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  font-weight: 500 !important;
}
div[data-testid="stSelectbox"] > div > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: 7px !important;
  color: var(--text) !important;
  font-size: 0.85rem !important;
  transition: border-color 0.15s !important;
}
div[data-testid="stSelectbox"] > div > div > div:focus-within { border-color: var(--cyan) !important; }
div[data-testid="stNumberInput"] input {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: 7px !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: 0.88rem !important;
}
div[data-testid="stNumberInput"] input:focus { border-color: var(--cyan) !important; outline: none !important; }

/* slider track */
div[data-testid="stSlider"] > div > div > div > div {
  background: var(--cyan) !important;
}

/* ── Predict button ── */
div[data-testid="stButton"] > button {
  width: 100% !important;
  background: linear-gradient(135deg, #003D52, #005F7A) !important;
  border: 1px solid var(--cyan) !important;
  color: var(--cyan) !important;
  border-radius: 8px !important;
  font-family: var(--mono) !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  padding: 0.75rem !important;
  transition: all 0.2s !important;
  box-shadow: 0 0 20px rgba(0,229,255,0.1) !important;
}
div[data-testid="stButton"] > button:hover {
  background: linear-gradient(135deg, #005F7A, #007FA0) !important;
  box-shadow: 0 0 30px rgba(0,229,255,0.25) !important;
  transform: translateY(-1px) !important;
}

/* ── Result verdict ── */
.verdict-box {
  border-radius: 10px;
  padding: 1.4rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.verdict-approved {
  background: linear-gradient(135deg, rgba(0,255,157,0.06), rgba(0,200,122,0.02));
  border: 1px solid rgba(0,255,157,0.3);
}
.verdict-rejected {
  background: linear-gradient(135deg, rgba(255,61,90,0.06), rgba(255,61,90,0.02));
  border: 1px solid rgba(255,61,90,0.3);
}
.verdict-icon { font-size: 2.2rem; margin-bottom: 0.4rem; }
.verdict-label {
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 0.2rem;
}
.verdict-text {
  font-size: 1.7rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  line-height: 1;
}
.verdict-approved .verdict-text { color: var(--green); }
.verdict-rejected .verdict-text { color: var(--red); }
.verdict-conf {
  font-family: var(--mono);
  font-size: 0.78rem;
  margin-top: 0.6rem;
  opacity: 0.7;
}

/* ── Metric row ── */
.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.45rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  font-size: 0.78rem;
}
.metric-key { color: var(--muted); font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.05em; }
.metric-val { color: var(--text); font-weight: 500; }

/* ── Risk badge ── */
.risk-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: 20px;
  font-family: var(--mono);
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.risk-low    { background: rgba(0,255,157,0.1);  color: var(--green); border: 1px solid rgba(0,255,157,0.2); }
.risk-medium { background: rgba(255,179,0,0.1);  color: var(--amber); border: 1px solid rgba(255,179,0,0.2); }
.risk-high   { background: rgba(255,61,90,0.1);  color: var(--red);   border: 1px solid rgba(255,61,90,0.2); }

/* ── Footer ── */
.footer {
  text-align: center;
  color: var(--dim);
  font-size: 0.65rem;
  font-family: var(--mono);
  margin-top: 2.5rem;
  padding-top: 1.2rem;
  border-top: 1px solid var(--border);
  letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Load model (cached — runs only once) ──────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts():
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "loan_model.pkl"), "rb") as f:
        m = pickle.load(f)
    with open(os.path.join(base, "scaler.pkl"), "rb") as f:
        s = pickle.load(f)
    return m, s

model, scaler = load_artifacts()

# ── Plotly dark theme helper ───────────────────────────────────────────────────
# Build layout dicts explicitly per chart — no **unpacking conflicts
PLOT_CFG = {"displayModeBar": False, "staticPlot": False}
_DARK = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             font=dict(family="IBM Plex Mono, monospace", color="#4A6380", size=10))
_AX   = dict(gridcolor="#1A2D45", zerolinecolor="#1A2D45", showline=False)

# ── Gauge chart ───────────────────────────────────────────────────────────────
def make_gauge(prob, approved):
    color = "#00FF9D" if approved else "#FF3D5A"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob * 100, 1),
        number={"suffix": "%", "font": {"size": 28, "color": color, "family": "IBM Plex Mono"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#1A2D45",
                     "tickfont": {"size": 9, "color": "#4A6380"}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#0B1420",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40],  "color": "rgba(255,61,90,0.08)"},
                {"range": [40, 70], "color": "rgba(255,179,0,0.08)"},
                {"range": [70, 100],"color": "rgba(0,255,157,0.08)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.75, "value": prob * 100},
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="IBM Plex Mono, monospace", color="#4A6380", size=10),
                      height=200, margin=dict(l=20, r=20, t=20, b=0))
    return fig

# ── Feature importance bar ────────────────────────────────────────────────────
def make_feature_bar(features_dict):
    coefs = np.abs(model.coef_[0])
    names = ["Dependents","Loan Amt","Term","Credit Hist","Total Income",
             "Gender F","Gender M","Married N","Married Y",
             "Grad","Not Grad","Self Emp N","Self Emp Y",
             "Rural","Semiurban","Urban"]
    top_idx = np.argsort(coefs)[-8:]
    top_names = [names[i] for i in top_idx]
    top_vals  = [coefs[i] for i in top_idx]
    colors = ["#00E5FF" if v > np.median(top_vals) else "#243D5A" for v in top_vals]

    fig = go.Figure(go.Bar(
        x=top_vals, y=top_names,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="%{y}: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="IBM Plex Mono, monospace", color="#4A6380", size=10),
                      xaxis=dict(gridcolor="#1A2D45", zerolinecolor="#1A2D45", showline=False),
                      yaxis=dict(gridcolor="#1A2D45", zerolinecolor="#1A2D45", showline=False),
                      height=240, margin=dict(l=10, r=10, t=36, b=10),
                      title=dict(text="MODEL WEIGHTS (TOP 8)", font=dict(size=9, color="#4A6380")))
    return fig

# ── Probability breakdown donut ───────────────────────────────────────────────
def make_donut(prob):
    fig = go.Figure(go.Pie(
        values=[prob * 100, (1 - prob) * 100],
        labels=["Approved", "Rejected"],
        hole=0.72,
        marker=dict(colors=["#00FF9D", "#FF3D5A"],
                    line=dict(color="#020408", width=2)),
        textinfo="none",
        hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
    ))
    fig.add_annotation(text=f"{prob*100:.1f}%", x=0.5, y=0.5,
                       showarrow=False,
                       font=dict(size=22, color="#CDD9E8", family="IBM Plex Mono"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="IBM Plex Mono, monospace", color="#4A6380", size=10),
                      height=200, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    return fig

# ── Income vs approval reference bars ────────────────────────────────────────
def make_income_chart(total_income):
    benchmarks = {"Low\n<₹25K": 25000, "Med\n₹50K": 50000,
                  "Good\n₹1L": 100000, "High\n₹2L": 200000, "You": total_income}
    cols = ["#1A2D45","#1A2D45","#1A2D45","#1A2D45","#00E5FF"]
    fig = go.Figure(go.Bar(
        x=list(benchmarks.keys()),
        y=list(benchmarks.values()),
        marker=dict(color=cols, line=dict(width=0)),
        hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="IBM Plex Mono, monospace", color="#4A6380", size=10),
                      xaxis=dict(gridcolor="#1A2D45", zerolinecolor="#1A2D45", showline=False),
                      yaxis=dict(gridcolor="#1A2D45", zerolinecolor="#1A2D45",
                                 showline=False, tickformat=",.0f"),
                      height=200, margin=dict(l=10, r=10, t=36, b=10),
                      title=dict(text="INCOME BENCHMARK", font=dict(size=9, color="#4A6380")))
    return fig

# ── Risk radar ────────────────────────────────────────────────────────────────
def make_radar(credit, income, loan_amt, dependents, education):
    edu_score     = 90 if education == "Graduate" else 50
    income_score  = min(100, income / 2000)
    loan_score    = max(0, 100 - loan_amt / 5)
    dep_score     = max(0, 100 - dependents * 15)
    credit_score  = credit * 100

    cats   = ["Credit", "Income", "Loan Ratio", "Dependents", "Education"]
    scores = [credit_score, income_score, loan_score, dep_score, edu_score]
    scores += [scores[0]]
    cats   += [cats[0]]

    fig = go.Figure(go.Scatterpolar(
        r=scores, theta=cats,
        fill="toself",
        fillcolor="rgba(0,229,255,0.08)",
        line=dict(color="#00E5FF", width=2),
        marker=dict(color="#00E5FF", size=5),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono, monospace", color="#4A6380", size=10),
        height=230, margin=dict(l=10, r=10, t=36, b=10),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100],
                            gridcolor="#1A2D45", tickcolor="#1A2D45",
                            tickfont=dict(size=8, color="#4A6380")),
            angularaxis=dict(gridcolor="#1A2D45",
                             tickfont=dict(size=9, color="#4A6380")),
        ),
        title=dict(text="RISK RADAR", font=dict(size=9, color="#4A6380")),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-logo">◈ LOAN<b>IQ</b> <span>/ CREDIT INTELLIGENCE PLATFORM</span></div>
  <div class="nav-pills">
    <div class="nav-pill active">Dashboard</div>
    <div class="nav-pill">Analytics</div>
    <div class="nav-pill">Reports</div>
  </div>
  <div class="nav-status"><div class="status-dot"></div>MODEL ONLINE · v2.1</div>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kpi-grid">
  <div class="kpi-card cyan">
    <div class="kpi-label">Model Accuracy</div>
    <div class="kpi-value">85.4%</div>
    <div class="kpi-sub">Logistic Regression · L2</div>
    <div class="kpi-icon">⚙</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">Avg Approval Rate</div>
    <div class="kpi-value">68.7%</div>
    <div class="kpi-sub">Based on training data</div>
    <div class="kpi-icon">✓</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-label">Features Used</div>
    <div class="kpi-value">16</div>
    <div class="kpi-sub">After one-hot encoding</div>
    <div class="kpi-icon">◫</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-label">Latency</div>
    <div class="kpi-value">&lt;50ms</div>
    <div class="kpi-sub">Avg inference time</div>
    <div class="kpi-icon">⚡</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main layout: left form | right dashboard ──────────────────────────────────
col_form, col_dash = st.columns([1, 1.55], gap="medium")

# ════════ LEFT: INPUT FORM ════════════════════════════════════════════════════
with col_form:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">INPUT PARAMETERS</div>', unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        gender       = st.selectbox("Gender",         ["Male","Female"],               key="g")
        education    = st.selectbox("Education",      ["Graduate","Not Graduate"],      key="e")
        property_area= st.selectbox("Property Area",  ["Urban","Semiurban","Rural"],   key="p")
    with r1c2:
        married      = st.selectbox("Married",        ["Yes","No"],                    key="m")
        self_emp     = st.selectbox("Self Employed",  ["No","Yes"],                    key="se")
        credit       = st.selectbox("Credit History", ["Good (1)","Bad (0)"],          key="c")

    dependents = st.slider("Dependents", 0, 5, 0, key="d")

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        app_inc  = st.number_input("Applicant Income (₹)",    min_value=0, value=50000, step=5000, key="ai")
        loan_amt = st.number_input("Loan Amount (₹ thousands)",min_value=1, value=150,  step=10,   key="la")
    with r2c2:
        coapp_inc = st.number_input("Co-Applicant Income (₹)", min_value=0, value=0,    step=5000, key="ci")
        loan_term = st.selectbox("Loan Term (months)", [360,180,120,84,60,36,12], key="lt")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("◈  RUN PREDICTION ENGINE", key="predict")
    st.markdown('</div>', unsafe_allow_html=True)

# ════════ RIGHT: DASHBOARD ════════════════════════════════════════════════════
with col_dash:

    # ── Prepare inputs & run model ────────────────────────────────────────────
    credit_val   = 1 if "Good" in credit else 0
    total_income = app_inc + coapp_inc

    features = [
        dependents, loan_amt, float(loan_term), credit_val, total_income,
        1 if gender=="Female" else 0,
        1 if gender=="Male"   else 0,
        1 if married=="No"    else 0,
        1 if married=="Yes"   else 0,
        1 if education=="Graduate"     else 0,
        1 if education=="Not Graduate" else 0,
        1 if self_emp=="No"  else 0,
        1 if self_emp=="Yes" else 0,
        1 if property_area=="Rural"     else 0,
        1 if property_area=="Semiurban" else 0,
        1 if property_area=="Urban"     else 0,
    ]
    X          = np.array(features, dtype=float).reshape(1, -1)
    X_scaled   = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]
    proba      = model.predict_proba(X_scaled)[0]
    approved   = int(prediction) == 1
    conf       = proba[1] if approved else proba[0]

    # risk level
    if conf >= 0.75:
        risk_cls, risk_lbl = ("risk-low","LOW RISK") if approved else ("risk-high","HIGH RISK")
    elif conf >= 0.55:
        risk_cls, risk_lbl = "risk-medium", "MEDIUM RISK"
    else:
        risk_cls, risk_lbl = ("risk-low","LOW RISK") if approved else ("risk-high","HIGH RISK")

    # ── Verdict card ──────────────────────────────────────────────────────────
    v_cls  = "verdict-approved" if approved else "verdict-rejected"
    v_icon = "✦" if approved else "✖"
    v_text = "APPROVED" if approved else "REJECTED"
    v_prob = f"CONFIDENCE: {conf*100:.1f}%  ·  P(approved)={proba[1]*100:.1f}%  P(rejected)={proba[0]*100:.1f}%"

    st.markdown(f"""
    <div class="verdict-box {v_cls}">
      <div class="verdict-icon">{v_icon}</div>
      <div class="verdict-label">CREDIT DECISION</div>
      <div class="verdict-text">{v_text}</div>
      <div class="verdict-conf">{v_prob}</div>
      <div style="margin-top:0.5rem">
        <span class="risk-badge {risk_cls}">{risk_lbl}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Chart row 1: gauge + donut ────────────────────────────────────────────
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown('<div class="panel"><div class="panel-title">APPROVAL SCORE</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(proba[1], approved),
                        use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)
    with ch2:
        st.markdown('<div class="panel"><div class="panel-title">PROBABILITY SPLIT</div>', unsafe_allow_html=True)
        st.plotly_chart(make_donut(proba[1]),
                        use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Chart row 2: radar + income bench ─────────────────────────────────────
    ch3, ch4 = st.columns(2)
    with ch3:
        st.markdown('<div class="panel"><div class="panel-title">RISK PROFILE</div>', unsafe_allow_html=True)
        st.plotly_chart(make_radar(credit_val, total_income, loan_amt, dependents, education),
                        use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)
    with ch4:
        st.markdown('<div class="panel"><div class="panel-title">INCOME CONTEXT</div>', unsafe_allow_html=True)
        st.plotly_chart(make_income_chart(total_income),
                        use_container_width=True, config=PLOT_CFG)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Feature importance (full width) ──────────────────────────────────────
    st.markdown('<div class="panel"><div class="panel-title">MODEL FEATURE WEIGHTS</div>', unsafe_allow_html=True)
    st.plotly_chart(make_feature_bar(features), use_container_width=True, config=PLOT_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Summary metrics ───────────────────────────────────────────────────────
    st.markdown('<div class="panel"><div class="panel-title">APPLICATION SUMMARY</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    rows = [
        ("GENDER", gender), ("MARRIED", married), ("EDUCATION", education),
        ("SELF EMPLOYED", self_emp), ("DEPENDENTS", dependents), ("PROPERTY", property_area),
        ("APPL. INCOME", f"₹{app_inc:,}"), ("CO-APPL. INC.", f"₹{coapp_inc:,}"),
        ("TOTAL INCOME", f"₹{total_income:,}"), ("LOAN AMT", f"₹{loan_amt}K"),
        ("LOAN TERM", f"{loan_term} mo"), ("CREDIT HIST", "Good" if credit_val else "Bad"),
    ]
    for col, chunk in zip([s1,s2,s3], [rows[:4], rows[4:8], rows[8:]]):
        with col:
            for k, v in chunk:
                st.markdown(f"""
                <div class="metric-row">
                  <span class="metric-key">{k}</span>
                  <span class="metric-val">{v}</span>
                </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  LOANIQ CREDIT INTELLIGENCE · LOGISTIC REGRESSION · SKLEARN · STREAMLIT &nbsp;·&nbsp;
  FOR EDUCATIONAL USE ONLY — NOT FINANCIAL ADVICE
</div>
""", unsafe_allow_html=True)