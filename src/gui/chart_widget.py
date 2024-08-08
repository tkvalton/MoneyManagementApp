from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class ChartWidget(QChartView):
    def __init__(self):
        super().__init__()
        self.chart = QChart()
        self.setChart(self.chart)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)

    def update_chart(self, total_income, total_outgoings, income, outgoings):
        income_series = QPieSeries()
        income_series.setName("Income")
        outgoings_series = QPieSeries()
        outgoings_series.setName("Outgoings")
        
        # Use a list of distinct colors
        income_colors = [QColor("#98FB98"), QColor("#90EE90"), QColor("#3CB371"), QColor("#2E8B57")]
        outgoings_colors = [QColor("#FFA07A"), QColor("#FA8072"), QColor("#E9967A"), QColor("#CD5C5C")]
        
        for i, (description, amount) in enumerate(income):
            slice = income_series.append(description, amount)
            slice.setColor(income_colors[i % len(income_colors)])
            slice.setLabelVisible(True)
            slice.setLabelColor(Qt.black)
            slice.setLabel(f"{description}: £{amount:.2f}")
            slice.setLabelPosition(QPieSeries.LabelOutside)
        
        for i, (description, amount) in enumerate(outgoings):
            slice = outgoings_series.append(description, amount)
            slice.setColor(outgoings_colors[i % len(outgoings_colors)])
            slice.setLabelVisible(True)
            slice.setLabelColor(Qt.black)
            slice.setLabel(f"{description}: £{amount:.2f}")
            slice.setLabelPosition(QPieSeries.LabelOutside)
        
        self.chart.removeAllSeries()
        self.chart.addSeries(income_series)
        self.chart.addSeries(outgoings_series)
        self.chart.setTitle(f"Income (£{total_income:.2f}) vs Outgoings (£{total_outgoings:.2f})")