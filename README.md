<div align="center">

# 🩺 Multiple Disease Detection System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Framework-Django-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini%201.5%20Flash-4285F4.svg?logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn%20%26%20XGBoost-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Publication](https://img.shields.io/badge/Published-IJARESM%20(April%202025)-success.svg)](http://www.ijaresm.com/)

**A hybrid AI-powered web application that analyzes user symptoms to deliver precise disease predictions using Machine Learning algorithms and Google Gemini AI.**

[Explore Features](#-key-features) • [Installation Guide](#-quick-start) • [Publication Details](#-research--publication)

</div>

---

## 📌 Overview

The **Multiple Disease Detection System** bridges traditional Machine Learning models with Large Language Model (LLM) capabilities. By accepting user-inputted symptoms, the application leverages pre-trained **RandomForest** and **XGBoost** algorithms alongside **Google Gemini 1.5 Flash** to provide instant diagnostic insights.

> 🎓 **Research Backing:** This system is based on research published in the *International Journal of All Research Education and Scientific Methods (IJARESM)*, Vol. 13, Issue 4, April 2025.

---

## ✨ Key Features

* 🤖 **Hybrid Prediction Engine:** Combines structured ML models (`RandomForest`, `XGBoost`) with generative AI (`Gemini 1.5 Flash`) for multi-perspective symptom analysis.
* 🔐 **Secure User Activation:** Admin-driven account review and activation workflow to manage system access safely.
* ⚡ **On-Demand Model Training:** Built-in backend endpoints allowing administrators to train and refresh up to 6 distinct ML models on the fly.
* 📊 **Dataset Viewer:** Embedded tool enabling admins to inspect symptom-disease datasets (`symptom_disease_dataset.csv` and `sampled_500_diseases.csv`).
* 💻 **Interactive UI:** Clean, responsive user interface developed with Django templates, custom CSS, and JavaScript.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend** | Python, Django |
| **AI & Machine Learning** | Google Gemini 1.5 Flash API, Scikit-Learn, XGBoost |
| **Data Handling** | Pandas, NumPy, SQLite |
| **Frontend** | HTML5, CSS3, JavaScript |

---

## 🚀 Quick Start

### Prerequisites
* Python 3.10+ installed
* Google Gemini API Key ([Get your API Key here](https://aistudio.google.com/))

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/DARSHANBAISANE/multiple-disease-detection.git](https://github.com/DARSHANBAISANE/multiple-disease-detection.git)
   cd multiple-disease-detection


   
2. Set Up Virtual Environment
Bash
python -m venv env
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

3. Install Dependencies

Bash
pip install -r requirments.txt

4. Environment Configuration
Create a .env file in the root directory and add your API credentials:

Code snippet
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_django_secret_key

5. Run Migrations & Launch Server

Bash
python manage.py migrate
python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.

⚙️ Model Training Note
⚠️ Pre-trained .pkl model files are excluded from this repository due to GitHub file size limits.

To generate model files locally:

Log in to the Admin Dashboard (/AdminLogin/).

Trigger the On-Demand Training endpoint to generate and save trained models into your workspace.

🔐 Default Admin Credentials
URL: /AdminLogin/

Username: admin

Password: admin

(Note: Please update the default password after initial setup in a production context.)

📄 Research & Publication
Paper Title: Multiple Disease Detection System

Journal: International Journal of All Research Education and Scientific Methods (IJARESM)

Publication Date: Vol. 13, Issue 4, April 2025

👤 Author
Darshan Baisane - GitHub Profile
