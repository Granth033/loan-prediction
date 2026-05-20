# 💰 LoanIQ — AI-Powered Loan Eligibility Predictor

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-FF4B4B?style=flat-square&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> An elegant, production-ready Streamlit web application that predicts loan eligibility using a trained **Logistic Regression** model — delivering instant results with a beautiful dark-themed UI.

---

## 🖼️ Preview

| Input Form | Approved | Rejected |
|:---:|:---:|:---:|
| Fill in 12 financial fields | ✅ Green result card | ❌ Red result card |

---

## ✨ Features

- 🔍 **Instant AI Prediction** — Logistic Regression model trained on real loan data
- 🎨 **Beautiful Dark UI** — Navy + Emerald design system with smooth hover effects
- 📊 **Confidence Score** — Visual progress bar showing prediction confidence
- 📋 **Input Summary** — Post-prediction recap of all submitted values
- 💡 **Eligibility Tips** — Built-in guidance to improve approval chances
- ⚡ **16 Features** — Gender, Marital Status, Education, Employment, Income, Credit History, and more
- 📱 **Responsive Layout** — Works on desktop and tablet screens

---

## 🗂️ Project Structure

```
loan-prediction-app/
│
├── app.py               # Main Streamlit application
├── loan_model.pkl       # Trained Logistic Regression model
├── scaler.pkl           # StandardScaler for feature normalization
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/loan-prediction-app.git
   cd loan-prediction-app
   ```

2. **Create a virtual environment** *(recommended)*
   ```bash
   python -m venv venv
   source venv/bin/activate       # macOS / Linux
   venv\Scripts\activate          # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501` 🎉

---

## 📥 Input Features

| Feature | Type | Description |
|---|---|---|
| Gender | Categorical | Male / Female |
| Married | Categorical | Yes / No |
| Dependents | Numeric | 0 – 5 |
| Education | Categorical | Graduate / Not Graduate |
| Self Employed | Categorical | Yes / No |
| Applicant Income | Numeric | Monthly income (₹) |
| Co-Applicant Income | Numeric | Co-applicant monthly income (₹) |
| Loan Amount | Numeric | Requested loan in ₹ thousands |
| Loan Term | Categorical | 12 – 360 months |
| Credit History | Binary | Good (1) / Bad (0) |
| Property Area | Categorical | Urban / Semiurban / Rural |

---

## 🧠 Model Details

| Attribute | Value |
|---|---|
| Algorithm | Logistic Regression |
| Regularization | L2 (Ridge) |
| Preprocessing | StandardScaler (16 features) |
| Output Classes | 0 = Not Approved, 1 = Approved |
| Framework | scikit-learn 1.6.1 |

---

## 🌐 Deploying to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo, branch `main`, and file `app.py`
4. Click **Deploy** — your app goes live in minutes!

> **Note:** Make sure `loan_model.pkl` and `scaler.pkl` are committed to the repo root.

---

## ⚠️ Disclaimer

> This application is built for **educational and demonstration purposes only**.  
> The predictions made by this model should **not** be used as actual financial advice.  
> Always consult a qualified financial advisor for real loan decisions.

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<p align="center">
  Built with ❤️ using <a href="https://streamlit.io">Streamlit</a> &amp; <a href="https://scikit-learn.org">scikit-learn</a>
</p>
