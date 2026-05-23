# Multiple Disease Detection System

A Django-based web application that predicts diseases from user-entered 
symptoms using Machine Learning and Google Gemini AI.

## Tech Stack
- Python, Django
- scikit-learn, XGBoost, RandomForest
- Google Gemini 1.5 Flash
- SQLite, pandas, numpy

## Features
- User registration with admin-controlled activation
- On-demand ML model training (RandomForest + XGBoost)
- Disease prediction via Google Gemini AI
- Dataset viewer
- 6 pre-trained ML models

## Publication
This project is associated with a peer-reviewed paper published in  
**IJARESM, Vol. 13, Issue 4, April 2025**

## Setup Instructions
1. Clone the repo
   git clone https://github.com/DARSHANBAISANE/multiple-disease-detection.git
2. Create virtual environment
   python -m venv env
3. Activate it
   env\Scripts\activate
4. Install dependencies
   pip install -r requirments.txt
5. Run migrations
   python manage.py migrate
6. Add your Gemini API key to .env file
7. Run the server
   python manage.py runserver

## Note on ML Models
Pre-trained model files (.pkl) are not included due to file size limits.
Run the training endpoint after setup to generate them locally.

## Admin Login
URL: /AdminLogin/
Username: admin
Password: admin