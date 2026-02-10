import sys
import base64
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QLineEdit, QFormLayout,
    QTabWidget, QTextEdit, QGroupBox, QScrollArea, QInputDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json


API_BASE_URL = 'http://127.0.0.1:8000/api'


class LoginDialog(QDialog):
    """Login dialog for authentication"""
    
    def __init__(self):
        super().__init__()
        self.credentials = None
        self.username = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Login - Chemical Equipment Visualizer')
        self.setFixedSize(400, 200)
        
        layout = QFormLayout()
        
        # Title
        title = QLabel('Chemical Equipment Parameter Visualizer')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addRow(title)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        layout.addRow('Username:', self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('Enter password')
        layout.addRow('Password:', self.password_input)
        
        # Login button
        login_btn = QPushButton('Login')
        login_btn.clicked.connect(self.attempt_login)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3f51b5;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #303f9f;
            }
        """)
        layout.addRow(login_btn)
        
        self.setLayout(layout)
        
        # Allow Enter key to submit
        self.password_input.returnPressed.connect(self.attempt_login)
    
    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter both username and password')
            return
        
        # Create credentials
        credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()
        
        # Test credentials
        try:
            response = requests.get(
                f'{API_BASE_URL}/datasets/',
                headers={'Authorization': f'Basic {credentials}'},
                timeout=5
            )
            
            if response.status_code == 200:
                self.credentials = credentials
                self.username = username
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Invalid credentials')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Connection failed: {str(e)}')


class DataLoader(QThread):
    """Thread for loading data from API"""
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, url, headers):
        super().__init__()
        self.url = url
        self.headers = headers
    
    def run(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                self.finished.emit(response.json())
            else:
                self.error.emit(f'Error: {response.status_code}')
        except Exception as e:
            self.error.emit(str(e))


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def clear(self):
        self.figure.clear()
        self.canvas.draw()
    
    def plot_pie_chart(self, data, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(data.keys())
        sizes = list(data.values())
        colors = plt.cm.Set3.colors[:len(labels)]
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('equal')
        
        self.canvas.draw()
    
    def plot_bar_chart(self, data, title, xlabel, ylabel):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        labels = list(data.keys())
        values = list(data.values())
        
        bars = ax.bar(labels, values, color='#3f51b5', alpha=0.7)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(axis='y', alpha=0.3)
        
        # Rotate labels if needed
        if len(labels) > 5:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_scatter(self, x_data, y_data, title, xlabel, ylabel):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        ax.scatter(x_data, y_data, alpha=0.6, c='#3f51b5', s=50)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(alpha=0.3)
        
        self.figure.tight_layout()
        self.canvas.draw()


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, credentials, username):
        super().__init__()
        self.credentials = credentials
        self.username = username
        self.headers = {'Authorization': f'Basic {credentials}'}
        self.datasets = []
        self.current_dataset = None
        self.current_analytics = None
        
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer - Desktop')
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Tab widget for different views
        self.tabs = QTabWidget()
        
        # Summary tab
        self.summary_widget = self.create_summary_tab()
        self.tabs.addTab(self.summary_widget, 'Summary')
        
        # Charts tab
        self.charts_widget = self.create_charts_tab()
        self.tabs.addTab(self.charts_widget, 'Charts')
        
        # Data table tab
        self.table_widget = self.create_table_tab()
        self.tabs.addTab(self.table_widget, 'Data Table')
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage(f'Logged in as: {self.username}')
    
    def create_header(self):
        header = QGroupBox()
        header.setStyleSheet("""
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout()
        
        title = QLabel('Chemical Equipment Parameter Visualizer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setStyleSheet('color: white;')
        layout.addWidget(title)
        
        layout.addStretch()
        
        user_label = QLabel(f'User: {self.username}')
        user_label.setFont(QFont('Arial', 12))
        user_label.setStyleSheet('color: white;')
        layout.addWidget(user_label)
        
        header.setLayout(layout)
        return header
    
    def create_control_panel(self):
        panel = QGroupBox('Controls')
        layout = QHBoxLayout()
        
        # Upload button
        upload_btn = QPushButton('Upload CSV')
        upload_btn.clicked.connect(self.upload_csv)
        upload_btn.setStyleSheet(self.button_style())
        layout.addWidget(upload_btn)
        
        # Dataset selector
        layout.addWidget(QLabel('Select Dataset:'))
        self.dataset_combo = QComboBox()
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_selected)
        layout.addWidget(self.dataset_combo)
        
        # Refresh button
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.load_datasets)
        refresh_btn.setStyleSheet(self.button_style())
        layout.addWidget(refresh_btn)
        
        # Download report button
        self.report_btn = QPushButton('Download PDF Report')
        self.report_btn.clicked.connect(self.download_report)
        self.report_btn.setEnabled(False)
        self.report_btn.setStyleSheet(self.button_style())
        layout.addWidget(self.report_btn)
        
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
    
    def create_summary_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setFont(QFont('Courier', 10))
        
        layout.addWidget(self.summary_text)
        widget.setLayout(layout)
        return widget
    
    def create_charts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Chart controls
        chart_controls = QHBoxLayout()
        chart_controls.addWidget(QLabel('Chart Type:'))
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems([
            'Equipment Type Distribution',
            'Type Count Bar Chart',
            'Pressure vs Flowrate'
        ])
        self.chart_type_combo.currentIndexChanged.connect(self.update_chart)
        chart_controls.addWidget(self.chart_type_combo)
        chart_controls.addStretch()
        
        layout.addLayout(chart_controls)
        
        # Chart widget
        self.chart = ChartWidget()
        layout.addWidget(self.chart)
        
        widget.setLayout(layout)
        return widget
    
    def create_table_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.data_table)
        widget.setLayout(layout)
        return widget
    
    def button_style(self):
        return """
            QPushButton {
                background-color: #3f51b5;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #303f9f;
            }
            QPushButton:disabled {
                background-color: #9e9e9e;
            }
        """
    
    def load_datasets(self):
        self.statusBar().showMessage('Loading datasets...')
        
        self.loader = DataLoader(f'{API_BASE_URL}/datasets/', self.headers)
        self.loader.finished.connect(self.on_datasets_loaded)
        self.loader.error.connect(self.on_error)
        self.loader.start()
    
    def on_datasets_loaded(self, data):
        self.datasets = data.get('results', data) if isinstance(data, dict) else data
        
        self.dataset_combo.clear()
        self.dataset_combo.addItem('-- Select Dataset --')
        
        for dataset in self.datasets:
            self.dataset_combo.addItem(dataset['name'], dataset['id'])
        
        self.statusBar().showMessage(f'Loaded {len(self.datasets)} datasets')
    
    def on_dataset_selected(self, index):
        if index <= 0:
            self.current_dataset = None
            self.current_analytics = None
            self.report_btn.setEnabled(False)
            return
        
        dataset_id = self.dataset_combo.currentData()
        self.load_dataset_details(dataset_id)
    
    def load_dataset_details(self, dataset_id):
        self.statusBar().showMessage('Loading dataset details...')
        
        # Load dataset
        self.dataset_loader = DataLoader(f'{API_BASE_URL}/datasets/{dataset_id}/', self.headers)
        self.dataset_loader.finished.connect(self.on_dataset_details_loaded)
        self.dataset_loader.error.connect(self.on_error)
        self.dataset_loader.start()
        
        # Load analytics
        self.analytics_loader = DataLoader(f'{API_BASE_URL}/datasets/{dataset_id}/analytics/', self.headers)
        self.analytics_loader.finished.connect(self.on_analytics_loaded)
        self.analytics_loader.error.connect(self.on_error)
        self.analytics_loader.start()
    
    def on_dataset_details_loaded(self, data):
        self.current_dataset = data
        self.report_btn.setEnabled(True)
        self.update_data_table()
        self.statusBar().showMessage('Dataset loaded')
    
    def on_analytics_loaded(self, data):
        self.current_analytics = data
        self.update_summary()
        self.update_chart()
    
    def update_summary(self):
        if not self.current_analytics:
            self.summary_text.setText('No analytics available')
            return
        
        analytics = self.current_analytics
        
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║          CHEMICAL EQUIPMENT PARAMETER SUMMARY                ║
╚══════════════════════════════════════════════════════════════╝

Dataset: {self.current_dataset.get('name', 'N/A')}
Uploaded: {self.current_dataset.get('uploaded_at', 'N/A')}

═══════════════════════════════════════════════════════════════

OVERALL STATISTICS
─────────────────────────────────────────────────────────────

Total Equipment:        {analytics['total_equipment']}

Average Flowrate:       {analytics['avg_flowrate']:.2f}
  Range:                {analytics['min_flowrate']:.2f} - {analytics['max_flowrate']:.2f}

Average Pressure:       {analytics['avg_pressure']:.2f}
  Range:                {analytics['min_pressure']:.2f} - {analytics['max_pressure']:.2f}

Average Temperature:    {analytics['avg_temperature']:.2f}
  Range:                {analytics['min_temperature']:.2f} - {analytics['max_temperature']:.2f}

═══════════════════════════════════════════════════════════════

EQUIPMENT TYPE DISTRIBUTION
─────────────────────────────────────────────────────────────
"""
        
        for eq_type, count in analytics['equipment_types'].items():
            percentage = (count / analytics['total_equipment']) * 100
            summary += f"\n{eq_type:.<30} {count:>5} ({percentage:>5.1f}%)"
        
        summary += "\n\n═══════════════════════════════════════════════════════════════\n"
        
        self.summary_text.setText(summary)
    
    def update_chart(self):
        if not self.current_analytics:
            self.chart.clear()
            return
        
        chart_type = self.chart_type_combo.currentText()
        analytics = self.current_analytics
        
        if chart_type == 'Equipment Type Distribution':
            self.chart.plot_pie_chart(
                analytics['equipment_types'],
                'Equipment Type Distribution'
            )
        elif chart_type == 'Type Count Bar Chart':
            self.chart.plot_bar_chart(
                analytics['equipment_types'],
                'Equipment Count by Type',
                'Equipment Type',
                'Count'
            )
        elif chart_type == 'Pressure vs Flowrate':
            if self.current_dataset and 'equipment_records' in self.current_dataset:
                records = self.current_dataset['equipment_records']
                flowrates = [r['flowrate'] for r in records]
                pressures = [r['pressure'] for r in records]
                self.chart.plot_scatter(
                    flowrates, pressures,
                    'Pressure vs Flowrate Correlation',
                    'Flowrate', 'Pressure'
                )
    
    def update_data_table(self):
        if not self.current_dataset or 'equipment_records' not in self.current_dataset:
            self.data_table.setRowCount(0)
            return
        
        records = self.current_dataset['equipment_records']
        
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        
        self.data_table.setRowCount(len(records))
        
        for i, record in enumerate(records):
            self.data_table.setItem(i, 0, QTableWidgetItem(record['equipment_name']))
            self.data_table.setItem(i, 1, QTableWidgetItem(record['equipment_type']))
            self.data_table.setItem(i, 2, QTableWidgetItem(f"{record['flowrate']:.2f}"))
            self.data_table.setItem(i, 3, QTableWidgetItem(f"{record['pressure']:.2f}"))
            self.data_table.setItem(i, 4, QTableWidgetItem(f"{record['temperature']:.2f}"))
        
        self.data_table.resizeColumnsToContents()
    
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        
        if not file_path:
            return
        
        # Get dataset name
        name, ok = QInputDialog.getText(self, 'Dataset Name', 'Enter dataset name:')
        if not ok or not name:
            return
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'name': name}
                
                response = requests.post(
                    f'{API_BASE_URL}/upload/',
                    headers=self.headers,
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 201:
                    QMessageBox.information(self, 'Success', 'Dataset uploaded successfully!')
                    self.load_datasets()
                else:
                    error_msg = response.json().get('error', 'Upload failed')
                    QMessageBox.warning(self, 'Error', error_msg)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload failed: {str(e)}')
    
    def download_report(self):
        if not self.current_dataset:
            return
        
        dataset_id = self.current_dataset['id']
        dataset_name = self.current_dataset['name']
        
        try:
            response = requests.get(
                f'{API_BASE_URL}/datasets/{dataset_id}/download-report/',
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Save file
                file_path, _ = QFileDialog.getSaveFileName(
                    self, 'Save PDF Report', f'report_{dataset_name}.pdf', 'PDF Files (*.pdf)'
                )
                
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'Report downloaded successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'Failed to generate report')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Download failed: {str(e)}')
    
    def on_error(self, error_msg):
        self.statusBar().showMessage(f'Error: {error_msg}')
        QMessageBox.warning(self, 'Error', error_msg)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Show login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        # Create main window
        window = MainWindow(login_dialog.credentials, login_dialog.username)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
