from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from config.theme_manager import ThemeManager


class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardPage")
        self.current_tab = "Overview"
        
        self._init_ui()
        
        # Connect to theme changes
        ThemeManager().theme_changed.connect(self.update_theme)
    
    def _init_ui(self):
        """Initialize dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add all sections
        self.create_tabs(layout)
        self.create_metrics(layout)
        self.create_insights(layout)
        self.create_product_section(layout)
        self.create_financial_section(layout)
        
        # Add stretch at bottom
        layout.addStretch()
    
    def create_tabs(self, parent_layout):
        """Create tab navigation"""
        tabs_widget = QWidget()
        tabs_widget.setObjectName("TabsWidget")
        layout = QHBoxLayout(tabs_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        tabs = ["Overview", "POS Dashboard", "ABC Dashboard"]
        
        self.tab_buttons = []
        for tab_name in tabs:
            btn = QPushButton(tab_name)
            btn.setObjectName(f"TabButton_{tab_name.replace(' ', '')}")
            btn.setProperty("class", "tab-button")
            btn.setCheckable(True)
            btn.setChecked(tab_name == self.current_tab)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, t=tab_name: self.switch_tab(t))
            layout.addWidget(btn)
            self.tab_buttons.append((tab_name, btn))
        
        layout.addStretch()
        parent_layout.addWidget(tabs_widget)
    
    def switch_tab(self, tab_name):
        """Switch active tab"""
        self.current_tab = tab_name
        for name, btn in self.tab_buttons:
            btn.setChecked(name == tab_name)
    
    def create_metrics(self, parent_layout):
        """Create metric cards section"""
        container = QWidget()
        container.setObjectName("MetricsContainer")
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        metrics = [
            ("Today Sales", "₹89,000", "4.3%", "Down from yesterday", "red", False),
            ("Today Purchase", "₹1,00,293", "1.3%", "Up from past week", "yellow", True),
            ("Today Bills", "1805", "1.3%", "Up from Yesterday", "purple", True),
            ("To Pay", "₹40,689", "", "For 3 Vendors", "pink", False),
        ]
        
        for title, value, change, subtitle, color, is_up in metrics:
            card = self.create_metric_card(title, value, change, subtitle, color, is_up)
            layout.addWidget(card)
        
        parent_layout.addWidget(container)
    
    def create_metric_card(self, title, value, change, subtitle, color, is_up):
        """Create a single metric card"""
        card = QFrame()
        card.setObjectName("MetricCard")
        card.setProperty("color", color)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("MetricTitle")
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("MetricValue")
        layout.addWidget(value_label)
        
        # Change indicator
        if change:
            change_container = QWidget()
            change_layout = QHBoxLayout(change_container)
            change_layout.setContentsMargins(0, 0, 0, 0)
            change_layout.setSpacing(4)
            
            arrow = QLabel("↑" if is_up else "↓")
            arrow.setObjectName("MetricArrow")
            arrow.setProperty("direction", "up" if is_up else "down")
            
            change_label = QLabel(change)
            change_label.setObjectName("MetricChange")
            change_label.setProperty("direction", "up" if is_up else "down")
            
            change_layout.addWidget(arrow)
            change_layout.addWidget(change_label)
            change_layout.addStretch()
            
            layout.addWidget(change_container)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("MetricSubtitle")
        layout.addWidget(subtitle_label)
        
        layout.addStretch()
        return card
    
    def create_insights(self, parent_layout):
        """Create customer insights section"""
        section = QWidget()
        section.setObjectName("InsightsSection")
        section_layout = QVBoxLayout(section)
        section_layout.setSpacing(16)
        section_layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("Customer Insights")
        title.setObjectName("SectionTitle")
        section_layout.addWidget(title)
        
        # Cards container
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        cards_data = [
            ("Total Customers", "With Loyalty Points", "1685", False, 0),
            ("Today New Customers", "With Loyalty Points", "32", False, 0),
            ("Returning Customers", "With Loyalty Points", "500", True, 63),
            ("Active Members", "Last 30 Days", "850", True, 33),
        ]
        
        for title, subtitle, value, has_chart, percentage in cards_data:
            card = self.create_insight_card(title, subtitle, value, has_chart, percentage)
            cards_layout.addWidget(card)
        
        section_layout.addLayout(cards_layout)
        parent_layout.addWidget(section)
    
    def create_insight_card(self, title, subtitle, value, has_chart, percentage):
        """Create a single insight card"""
        card = QFrame()
        card.setObjectName("InsightCard")
        
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("InsightTitle")
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("InsightSubtitle")
        layout.addWidget(subtitle_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("InsightValue")
        layout.addWidget(value_label)
        
        # Chart placeholder (if needed)
        if has_chart:
            chart_label = QLabel(f"📊 {percentage}%")
            chart_label.setObjectName("InsightChart")
            layout.addWidget(chart_label)
        
        layout.addStretch()
        return card
    
    def create_product_section(self, parent_layout):
        """Create product performance section"""
        section = QWidget()
        section.setObjectName("ProductSection")
        section_layout = QVBoxLayout(section)
        section_layout.setSpacing(15)
        section_layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("Product Performance")
        title.setObjectName("SectionTitle")
        section_layout.addWidget(title)
        
        # Charts container
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Top-selling products
        top_chart = self.create_chart_card("Top-Selling Products", "📊 Bar Chart")
        charts_layout.addWidget(top_chart)
        
        # Least-selling products
        least_chart = self.create_chart_card("Least-Selling Products", "📊 Bar Chart")
        charts_layout.addWidget(least_chart)
        
        section_layout.addLayout(charts_layout)
        parent_layout.addWidget(section)
    
    def create_financial_section(self, parent_layout):
        """Create financial summary section"""
        section = QWidget()
        section.setObjectName("FinancialSection")
        section_layout = QVBoxLayout(section)
        section_layout.setSpacing(15)
        section_layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        title = QLabel("Financial Summary")
        title.setObjectName("SectionTitle")
        section_layout.addWidget(title)
        
        # Charts container
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Revenue trend
        revenue_chart = self.create_chart_card("Gross Revenue", "📈 Line Chart")
        charts_layout.addWidget(revenue_chart)
        
        # Loyalty discount
        loyalty_chart = self.create_chart_card("Loyalty Discount", "📊 Bar Chart")
        charts_layout.addWidget(loyalty_chart)
        
        section_layout.addLayout(charts_layout)
        parent_layout.addWidget(section)
    
    def create_chart_card(self, title, chart_placeholder):
        """Create a chart card with title and placeholder"""
        card = QFrame()
        card.setObjectName("ChartCard")
        
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("ChartTitle")
        layout.addWidget(title_label)
        
        # Chart placeholder
        chart = QLabel(chart_placeholder)
        chart.setObjectName("ChartPlaceholder")
        chart.setAlignment(Qt.AlignCenter)
        chart.setMinimumHeight(200)
        layout.addWidget(chart)
        
        return card
    
    def update_theme(self):
        """Refresh styles when theme changes"""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()