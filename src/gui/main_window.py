from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QFileDialog, QTableWidgetItem, QMessageBox,
    QComboBox, QLabel, QListWidget
)
from PyQt5.QtChart import QChartView
from logic.csv_importer import import_csv
from logic.calculations import calculate_stats
from logic.data_management import get_table_data
from datetime import datetime
import calendar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Money Management App")
        self.setGeometry(100, 100, 1200, 800)
        self.setContentsMargins(20, 20, 20, 20)
        self.all_data = []  # Store all imported data

        # Main layout
        main_layout = QVBoxLayout()

        # Import and filter layout
        top_layout = QHBoxLayout()
        
        # Import button
        self.import_button = QPushButton("Import CSV")
        self.import_button.clicked.connect(self.import_csv)
        top_layout.addWidget(self.import_button)

        # Month filter
        self.month_combo = QComboBox()
        self.month_combo.addItem("Full Year")
        self.month_combo.addItems(calendar.month_name[1:])
        self.month_combo.currentIndexChanged.connect(self.filter_data)
        top_layout.addWidget(QLabel("Month:"))
        top_layout.addWidget(self.month_combo)

        # Year filter
        self.year_combo = QComboBox()
        self.year_combo.addItem("All Years")
        current_year = datetime.now().year
        for year in range(2022, current_year + 1):
            self.year_combo.addItem(str(year))
        self.year_combo.currentIndexChanged.connect(self.filter_data)
        top_layout.addWidget(QLabel("Year:"))
        top_layout.addWidget(self.year_combo)

        main_layout.addLayout(top_layout)

        # Table for transactions
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Date", "Type", "Sort Code", "Account Number", 
            "Description", "Amount", "Balance"
        ])
        main_layout.addWidget(self.table)

        # Button to calculate stats
        self.calc_button = QPushButton("Calculate Stats")
        main_layout.addWidget(self.calc_button)

        # Lists for income and outgoings
        lists_layout = QHBoxLayout()
        
        self.income_list = QListWidget()
        self.income_list.setFixedHeight(200)  # Adjust as needed
        lists_layout.addWidget(QLabel("Income:"))
        lists_layout.addWidget(self.income_list)
        
        self.outgoings_list = QListWidget()
        self.outgoings_list.setFixedHeight(200)  # Adjust as needed
        lists_layout.addWidget(QLabel("Outgoings:"))
        lists_layout.addWidget(self.outgoings_list)
        
        main_layout.addLayout(lists_layout)

        # Chart view for statistics
        self.chart_view = QChartView()
        main_layout.addWidget(self.chart_view)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Set alternating row colors for the table
        self.table.setAlternatingRowColors(True)
        
        # Set some properties for the lists
        for list_widget in [self.income_list, self.outgoings_list]:
            list_widget.setAlternatingRowColors(True)
            list_widget.setSpacing(2)
        

    

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.all_data = import_csv(file_path)
                self.filter_data()
                QMessageBox.information(self, "Import Successful", f"Successfully imported {len(self.all_data)} rows of data.")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"An error occurred during import: {str(e)}")

    def filter_data(self):
        selected_month = self.month_combo.currentIndex()  # 0 is "Full Year"
        selected_year = self.year_combo.currentText()

        filtered_data = self.all_data

        if selected_year != "All Years":
            filtered_data = [row for row in filtered_data if row[0].startswith(selected_year)]

        if selected_month != 0:  # Not "Full Year"
            filtered_data = [row for row in filtered_data if int(row[0].split('-')[1]) == selected_month]

        self.populate_table(filtered_data)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, (date, trans_type, sort_code, account_number, description, amount, balance) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(trans_type))
            self.table.setItem(row, 2, QTableWidgetItem(sort_code))
            self.table.setItem(row, 3, QTableWidgetItem(account_number))
            self.table.setItem(row, 4, QTableWidgetItem(description))
            self.table.setItem(row, 5, QTableWidgetItem(f"£{amount:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"£{balance:.2f}"))
        self.table.resizeColumnsToContents()

    def update_lists(self, income, outgoings):
        self.income_list.clear()
        self.outgoings_list.clear()
        
        for description, amount in income:
            self.income_list.addItem(f"{description}: £{amount:.2f}")
        
        for description, amount in outgoings:
            self.outgoings_list.addItem(f"{description}: £{amount:.2f}")