from django.shortcuts import render, HttpResponse
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import UserRegistrationModel
from django.conf import settings

import seaborn as sns
from django.core.files.storage import FileSystemStorage


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get("loginid")
        password = request.POST.get("pswd")
        print(loginid)
        print(password)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=password)
            status = check.status
            if status == "activated":
                request.session['id'] = check.id
                request.session['loginid'] = check.loginid
                request.session['password'] = check.password
                request.session['email'] = check.email
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, "your account not activated")
            return render(request, "UserLogin.html")
        except Exception as e:
            print('=======>', e)
        messages.success(request, 'invalid details')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, "users/UserHome.html", {})


def view_data(request):
    from django.conf import settings
    import pandas as pd

    path = 'symptom_disease_dataset.csv'

    # Load the dataset
    d = pd.read_csv(path)

    # Drop the 'Disease' column
    d.drop(['Disease'], inplace=True, axis=1)

    context = {'dataset': d}
    return render(request, 'users/dataset.html', context)


# Django View for Model Training


import pandas as pd
import numpy as np
import joblib
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import SelectFromModel

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import os

def train_models():
    # Load dataset
    file_path = "symptom_disease_dataset.csv"
    df = pd.read_csv(file_path)

    # Drop missing values and duplicates
    df.dropna(inplace=True)
    df = df[df["Disease"] != "Unknown"]
    df = df.drop_duplicates()

    # Encode Disease labels
    label_encoder_path = "media/disease_encoder.pkl"
    if os.path.exists(label_encoder_path):
        disease_encoder = joblib.load(label_encoder_path)
    else:
        disease_encoder = LabelEncoder()
        joblib.dump(disease_encoder, label_encoder_path)

    df["Disease"] = disease_encoder.fit_transform(df["Disease"])

    # One-Hot Encoding for Symptoms
    # encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_encoded = encoder.fit_transform(df.drop(columns=["Disease"]))

    # Save OneHotEncoder
    joblib.dump(encoder, "media/symptom_encoder.pkl")

    # Convert One-Hot Encoded features to DataFrame
    feature_names = encoder.get_feature_names_out()
    X = pd.DataFrame(X_encoded, columns=feature_names)
    y = df["Disease"]

    # Normalize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, "media/scaler.pkl")

    # Handle class imbalance with SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

    # Feature Selection using RandomForest
    feature_selector = RandomForestClassifier(n_estimators=200, random_state=42)
    feature_selector.fit(X_resampled, y_resampled)

    selector = SelectFromModel(feature_selector, prefit=True, threshold='median')
    X_selected = selector.transform(X_resampled)

    # Save feature selector
    joblib.dump(selector, "media/feature_selector.pkl")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, y_resampled, test_size=0.2, stratify=y_resampled, random_state=42
    )

    # Define models
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=1000, max_depth=30, min_samples_split=5, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=500, max_depth=10, learning_rate=0.05, eval_metric='mlogloss',
                                 use_label_encoder=False)
    }

    # Train models and store results
    accuracies = {}
    best_model = None
    best_accuracy = 0
    best_model_name = ""

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        accuracies[name] = acc
        joblib.dump(model, f"media/{name}_model.pkl")

        if acc > best_accuracy:
            best_accuracy = acc
            best_model = model
            best_model_name = name

    # Save best model
    joblib.dump(best_model, "media/best_model.pkl")

    return accuracies, best_model_name


import numpy as np
import joblib


def predict_disease(symptoms):
    # Load the saved model, encoders, and scaler
    best_model = joblib.load("media/best_model.pkl")
    scaler = joblib.load("media/scaler.pkl")
    label_encoders = joblib.load("media/label_encoders.pkl")
    disease_encoder = joblib.load("media/disease_encoder.pkl")

    encoded_symptoms = []

    for i, sym in enumerate(symptoms):
        symptom_key = f'Symptom_{i + 1}'
        if symptom_key in label_encoders and sym in label_encoders[symptom_key].classes_:
            encoded_symptoms.append(label_encoders[symptom_key].transform([sym])[0])
        else:
            encoded_symptoms.append(0)  # Assign 0 if symptom is unknown

    # Convert to NumPy array and reshape for the model
    input_data = np.array(encoded_symptoms).reshape(1, -1)

    # Normalize input using the scaler
    input_data = scaler.transform(input_data)

    # Predict disease using the best model
    predicted_disease = best_model.predict(input_data)

    # Decode the predicted disease
    return disease_encoder.inverse_transform(predicted_disease)[0]


from django.shortcuts import render


def prediction(request):
    predicted_disease = None

    if request.method == "POST":
        symptoms = [request.POST.get(f'symptom_{i + 1}') for i in range(7)]
        import google.generativeai as genai
        import os

        API_KEY = 'AIzaSyAR4Le7R5Wq0R5Pckm0lB24gu_yyfE6o_0'
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel('gemini-1.5-flash')
        attributes = ' '.join(map(str, symptoms))
        query = f"can you give me the diesease name based on this attributes {attributes}, give me only disease name"
        print(f"Your Query is: {query}")
        response = model.generate_content(query)
        data = response.text
        # Get predicted disease
        # predicted_disease = predict_disease(symptoms)

        return render(request, 'users/prediction.html', {'predicted_disease': data})
    else:
        return render(request, 'users/prediction.html', {})


def training(request):
    accuracies, best_model_name = train_models()
    return render(request, 'users/modelresults.html', {'accuracies': accuracies, 'best_model': best_model_name})
