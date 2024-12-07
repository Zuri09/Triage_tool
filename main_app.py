import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget
)
from PyQt5.QtGui import QPalette, QColor
from forensic_analysis import analyze_raw_file
from report_generator import generate_report


class ForensicToolApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Forensics and Incident Response Tool")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()
        self.apply_styles()

    def initUI(self):
        layout = QVBoxLayout()

        # Status Label
        self.status_label = QLabel("Welcome to the Forensic Tool!")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; background-color: #2F4F4F; padding: 15px; border-radius: 5px; text-align: center;")

        # Analyze File Button
        self.analyze_btn = QPushButton("Analyze RAW File")
        self.analyze_btn.setStyleSheet("padding: 15px; font-size: 16px; font-weight: bold; color: #FFFFFF; background-color: #4682B4; border-radius: 10px;")

        # Generate Report Button
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.setStyleSheet("padding: 15px; font-size: 16px; font-weight: bold; color: #FFFFFF; background-color: #6B8E23; border-radius: 10px;")

        # Button Connections
        self.analyze_btn.clicked.connect(self.analyze_file)
        self.generate_btn.clicked.connect(self.generate_report)

        # Add widgets to layout
        layout.addWidget(self.status_label)
        layout.addWidget(self.analyze_btn)
        layout.addWidget(self.generate_btn)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def apply_styles(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1E1E2F"))
        palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
        self.setPalette(palette)

    def analyze_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select RAW File", "", "RAW Files (*.raw *.e01)")
        if file_name:
            self.analysis_data = analyze_raw_file(file_name)
            self.status_label.setText(f"Analyzed file: {file_name}")
        else:
            self.status_label.setText("No file selected for analysis.")

    def generate_report(self):
        if hasattr(self, "analysis_data"):
            generate_report(self.analysis_data)
            self.status_label.setText("Report generated successfully!")
        else:
            self.status_label.setText("No data to generate a report.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForensicToolApp()
    window.show()
    sys.exit(app.exec_())
