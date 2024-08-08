import sys
import os
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
from gui.main_window import MainWindow
from gui.chart_widget import ChartWidget
from logic.calculations import calculate_stats
from logic.data_management import get_table_data

def load_stylesheet(app):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stylesheet_path = os.path.join(current_dir, '..', 'resources', 'style.qss')
    file = QFile(stylesheet_path)
    if not file.open(QFile.ReadOnly | QFile.Text):
        print(f"Cannot open stylesheet file: {stylesheet_path}")
        return
    stream = QTextStream(file)
    stylesheet = stream.readAll()
    file.close()
    app.setStyleSheet(stylesheet)
    print(f"Stylesheet loaded successfully from: {stylesheet_path}")

class MoneyManagementApp(MainWindow):
    def __init__(self):
        super().__init__()
        self.chart_widget = ChartWidget()
        self.chart_view.setChart(self.chart_widget.chart)
        self.calc_button.clicked.connect(self.update_stats)

    def update_stats(self):
        try:
            data = get_table_data(self.table)
            if not data:
                QMessageBox.warning(self, "No Data", "No valid data found in the table.")
                return
            print(f"Data extracted from table: {data[:5]}")  # Print first 5 rows for debugging
            total_income, total_outgoings, income, outgoings = calculate_stats(data)
            print(f"Calculated stats: Income={total_income}, Outgoings={total_outgoings}")
            self.chart_widget.update_chart(total_income, total_outgoings, income, outgoings)
            self.update_lists(income, outgoings)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            print(f"Error details: {e}")  # Print full error details

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = MoneyManagementApp()
    window.show()
    sys.exit(app.exec_())