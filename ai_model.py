import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def train_ai_model(data_file):
    # Load training data
    data = pd.read_csv(data_file)

    # Preprocess data
    label_encoder = LabelEncoder()
    data["Threat_Type_Encoded"] = label_encoder.fit_transform(data["Threat_Type"])

    X = data[["Feature1", "Feature2", "Feature3"]]
    y = data["Threat_Type_Encoded"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    return model, label_encoder
