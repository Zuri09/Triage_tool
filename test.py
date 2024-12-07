import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QTabWidget, QTableWidget, QTableWidgetItem
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import yara
import os
import numpy as np

# Function to train AI model
def train_model(data_file):
    data = pd.read_csv(data_file)
    label_encoder = LabelEncoder()
    data["Threat_Type_Encoded"] = label_encoder.fit_transform(data["Threat_Type"])

    X = data[["Feature1", "Feature2", "Feature3"]]
    y = data["Threat_Type_Encoded"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Test the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy:.2f}")

    return model, label_encoder

# Function to identify IOCs with YARA (simplified)
def scan_with_yara(file_path):
    rules = yara.compile(filepath='malware_rules.yar')  # YARA rules file
    matches = rules.match(file_path)
    return matches

# Function to generate a report
def generate_report(data, file_format="PDF"):
    # Placeholder for generating a report (PDF generation, CSV export etc.)
    if file_format == "PDF":
        # Implement PDF generation using reportlab or similar libraries
        pass
    elif file_format == "CSV":
        data.to_csv("report.csv", index=False)

# The main window class for the application
class DigitalForensicsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Forensics & Incident Response Tool")
        self.setGeometry(200, 200, 1200, 800)

        self.model = None
        self.label_encoder = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.import_tab = QWidget()
        self.analysis_tab = QWidget()

        self.tabs.addTab(self.import_tab, "Import Evidence")
        self.tabs.addTab(self.analysis_tab, "Analysis & Report")

        self.import_label = QLabel("Import Forensic Image (RAW, E01, etc.)")
        self.import_btn = QPushButton("Select Image")
        self.import_btn.clicked.connect(self.import_image)

        self.analysis_label = QLabel("Analyze Evidence")
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.analyze_data)

        self.import_tab.layout = QVBoxLayout()
        self.import_tab.layout.addWidget(self.import_label)
        self.import_tab.layout.addWidget(self.import_btn)

        self.analysis_tab.layout = QVBoxLayout()
        self.analysis_tab.layout.addWidget(self.analysis_label)
        self.analysis_tab.layout.addWidget(self.analyze_btn)

        layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def import_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Forensic Image File", "", "Forensic Image Files (*.e01 *.raw)")
        if file_name:
            # Placeholder for raw image import logic
            print(f"Imported forensic image: {file_name}")

    def analyze_data(self):
        if not self.model:
            print("Model not trained!")
            return
        
        # Placeholder for automated scanning & analysis (YARA, AI analysis, etc.)
        print("Scanning evidence for IOCs and anomalies...")
        
        # Example: Running YARA rule scan
        matches = scan_with_yara('sample_data.raw')
        if matches:
            print(f"YARA Matches: {matches}")
        else:
            print("No matches found")

        # Example: AI threat prioritization
        example_data = pd.DataFrame({'Feature1': [100], 'Feature2': [0.8], 'Feature3': [1]})
        threat = self.model.predict(example_data)
        print(f"Predicted Threat: {threat}")
        
        self.generate_report()

    def generate_report(self):
        # Here we will generate a CSV or PDF report with the data
        data = pd.DataFrame({
            "Feature1": [100, 50],
            "Feature2": [0.8, 0.3],
            "Threat": ["High", "Low"]
        })
        generate_report(data, "CSV")
        print("Report generated!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = DigitalForensicsApp()
    mainWin.show()
    sys.exit(app.exec_())
