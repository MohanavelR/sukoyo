"""
Dashboard Page Module
Displays overview metrics, customer insights, product performance, and financial summaries
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPainterPath, QBrush

from config.theme_manager import ThemeManager
from components.button import PrimaryButton

class CircularProgress(QWidget):
    """Circular progress indicator with percentage display"""
    
    def __init__(self, percentage, color, size=120):
        super().__init__()
        self.percentage = max(0, min(100, percentage))
        self.color = color
        self.setFixedSize(size, size)
    
    def paintEvent(self, event):
        """Draw circular progress arc"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Calculate dimensions
            pen_width = 10
            margin = pen_width // 2 + 5
            diameter = min(self.width(), self.height()) - (margin * 2)
            
            # Background circle
            painter.setPen(QPen(QColor("#f0f0f0"), pen_width))
            painter.drawEllipse(margin, margin, diameter, diameter)
            
            # Progress arc
            painter.setPen(QPen(QColor(self.color), pen_width, Qt.SolidLine, Qt.RoundCap))
            span_angle = int(360 * (self.percentage / 100) * 16)
            painter.drawArc(margin, margin, diameter, diameter, 90 * 16, -span_angle)
            
            # Percentage text
            painter.setPen(QColor(self.color))
            font = QFont("Segoe UI", 18, QFont.Bold)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, f"{int(self.percentage)}%")
            
        except Exception as e:
            print(f"Error drawing circular progress: {e}")


class BarChartWidget(QWidget):
    """Vertical bar chart for product sales"""
    
    def __init__(self, products=None, values=None):
        super().__init__()
        self.setObjectName("ChartPlaceholder")
        self.setMinimumHeight(280)
        
        self.products = products or ["Biscuits", "Baby Powder", "Chocolates", "Shampoo", "Toothpaste"]
        self.values = values or [12000, 33567, 40000, 22000, 14000]
        self.highlight_index = 2
        
    def paintEvent(self, event):
        """Draw vertical bar chart"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            if not self.products or not self.values:
                return
            
            max_val = max(self.values) * 1.1 if self.values else 1
            width = self.width()
            height = self.height() - 40
            bar_width = min(50, (width - 40) // len(self.products))
            spacing = (width - len(self.products) * bar_width) / (len(self.products) + 1)
            
            for i, (product, value) in enumerate(zip(self.products, self.values)):
                x = spacing + i * (bar_width + spacing)
                bar_height = (value / max_val) * height if max_val > 0 else 0
                y = height - bar_height
                
                color = QColor("#4f46e5")
                painter.fillRect(int(x), int(y), bar_width, int(bar_height), color)
                
                if i == self.highlight_index:
                    painter.setPen(QPen(QColor("#4f46e5"), 2, Qt.DashLine))
                    painter.drawLine(int(x + bar_width / 2), 10, int(x + bar_width / 2), int(y))
                    
                    painter.setPen(QColor("#111827"))
                    font = QFont("Segoe UI", 10, QFont.Bold)
                    painter.setFont(font)
                    painter.drawText(int(x - 15), 25, f"₹{value:,}")
                
                painter.setPen(QColor("#6b7280"))
                font = QFont("Segoe UI", 9)
                painter.setFont(font)
                painter.drawText(int(x), height + 30, bar_width, 20, Qt.AlignCenter, product)
                
        except Exception as e:
            print(f"Error drawing bar chart: {e}")


class HorizontalBarWidget(QWidget):
    """Horizontal bar chart for product comparison"""
    
    def __init__(self, products=None):
        super().__init__()
        self.setObjectName("ChartPlaceholder")
        self.setMinimumHeight(280)
        
        self.products = products or [
            ("Noodles", 50799, "#6366f1"),
            ("Pasta", 30799, "#9ca3af"),
            ("Bread", 25567, "#9ca3af"),
            ("Garbage Bags", 5789, "#9ca3af")
        ]
        
    def paintEvent(self, event):
        """Draw horizontal bar chart"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            if not self.products:
                return
            
            max_val = max(p[1] for p in self.products) * 1.1 if self.products else 1
            y_pos = 30
            bar_height = 32
            spacing = 45
            available_width = self.width() - 250
            
            for name, value, color in self.products:
                painter.setPen(QColor("#6b7280"))
                font = QFont("Segoe UI", 11)
                painter.setFont(font)
                painter.drawText(10, y_pos, 100, bar_height, Qt.AlignVCenter, name)
                
                bar_width = int((value / max_val) * available_width) if max_val > 0 else 0
                painter.fillRect(120, y_pos + 6, bar_width, bar_height - 12, QColor(color))
                
                painter.drawText(bar_width + 130, y_pos, 100, bar_height, Qt.AlignVCenter, f"{value:,}")
                
                y_pos += spacing
                
        except Exception as e:
            print(f"Error drawing horizontal bar chart: {e}")


class LineChartWidget(QWidget):
    """Line chart for trends over time"""
    
    def __init__(self, show_series2=True):
        super().__init__()
        self.setObjectName("ChartPlaceholder")
        self.show_series2 = show_series2
        self.setMinimumHeight(280)
        
        self.months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN"]
        self.series1 = [1, 3, 5, 7, 5, 8]
        self.series2 = [0.5, 2, 3, 2.5, 5, 6]
        self.highlight_index = 2
        
    def paintEvent(self, event):
        """Draw line chart with optional second series"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            width = self.width() - 60
            height = self.height() - 60
            x_start = 40
            y_start = 20
            max_y = 10
            
            if width <= 0 or height <= 0:
                return
            
            painter.setPen(QPen(QColor("#f3f4f6"), 1))
            for i in range(6):
                y = y_start + (i * height / 5)
                painter.drawLine(x_start, int(y), x_start + width, int(y))
            
            self._draw_series(painter, self.series1, width, height, x_start, y_start, 
                            max_y, QColor("#111827"), is_primary=True)
            
            if self.show_series2 and self.series2:
                self._draw_series(painter, self.series2, width, height, x_start, y_start, 
                                max_y, QColor("#6366f1"), is_primary=False)
            
            painter.setPen(QColor("#6b7280"))
            font = QFont("Segoe UI", 9)
            painter.setFont(font)
            for i, month in enumerate(self.months):
                x = x_start + (i * width / (len(self.months) - 1))
                painter.drawText(int(x - 20), height + y_start + 10, 40, 20, Qt.AlignCenter, month)
                
        except Exception as e:
            print(f"Error drawing line chart: {e}")
    
    def _draw_series(self, painter, data, width, height, x_start, y_start, max_y, color, is_primary=False):
        """Helper method to draw a data series"""
        if not data:
            return
        
        try:
            line_style = Qt.SolidLine if is_primary else Qt.DashLine
            painter.setPen(QPen(color, 2, line_style))
            path = QPainterPath()
            
            for i, val in enumerate(data):
                x = x_start + (i * width / (len(data) - 1))
                y = y_start + height - (val / max_y * height)
                
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
                
                if is_primary:
                    painter.setBrush(QBrush(color))
                    painter.drawEllipse(QPointF(x, y), 4, 4)
                    
                    if i == self.highlight_index:
                        painter.setBrush(QBrush(QColor("white")))
                        painter.drawEllipse(QPointF(x, y), 6, 6)
                        painter.setBrush(QBrush(color))
                        painter.drawEllipse(QPointF(x, y), 4, 4)
                        
                        label_bg = QRectF(x - 35, y - 35, 70, 25)
                        painter.setBrush(QBrush(color))
                        painter.drawRoundedRect(label_bg, 4, 4)
                        painter.setPen(QColor("white"))
                        font = QFont("Segoe UI", 10, QFont.Bold)
                        painter.setFont(font)
                        painter.drawText(label_bg, Qt.AlignCenter, "₹55,567")
                        painter.setPen(QPen(color, 2, line_style))
            
            painter.drawPath(path)
            
        except Exception as e:
            print(f"Error drawing series: {e}")


class DualBarChartWidget(QWidget):
    """Dual bar chart for comparing two datasets"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("ChartPlaceholder")
        self.setMinimumHeight(280)
        
        self.months = ["Jan", "Feb", "Mar", "April"]
        self.redeemed = [3000, 3300, 4500, 2000]
        self.not_redeemed = [2300, 2500, 3700, 1000]
        self.highlight_index = 2
        
    def paintEvent(self, event):
        """Draw dual bar chart"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            max_val = max(max(self.redeemed), max(self.not_redeemed)) * 1.2
            width = self.width() - 80
            height = self.height() - 60
            x_start = 40
            y_start = 20
            bar_width = 40
            group_spacing = width / len(self.months) if len(self.months) > 0 else width
            
            if width <= 0 or height <= 0:
                return
            
            for i, month in enumerate(self.months):
                x = x_start + i * group_spacing
                
                h1 = (self.redeemed[i] / max_val) * height if max_val > 0 else 0
                painter.fillRect(int(x), int(y_start + height - h1), bar_width, int(h1), QColor("#6366f1"))
                
                h2 = (self.not_redeemed[i] / max_val) * height if max_val > 0 else 0
                painter.fillRect(int(x + bar_width + 5), int(y_start + height - h2), bar_width, int(h2), QColor("#c084fc"))
                
                painter.setPen(QColor("#6b7280"))
                font = QFont("Segoe UI", 10)
                painter.setFont(font)
                painter.drawText(int(x), height + y_start + 10, bar_width * 2, 20, Qt.AlignCenter, month)
                
                if i == self.highlight_index:
                    painter.setPen(QColor("#6366f1"))
                    font = QFont("Segoe UI", 9, QFont.Bold)
                    painter.setFont(font)
                    painter.drawText(int(x - 5), int(y_start + height - h1 - 10), "3.1k")
                    painter.setPen(QColor("#c084fc"))
                    painter.drawText(int(x + bar_width), int(y_start + height - h2 - 10), "2.3k")
                    
        except Exception as e:
            print(f"Error drawing dual bar chart: {e}")


class DashboardPage(QWidget):
    """Main dashboard page with metrics, insights, and charts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardPage")
        self.current_tab = "Overview"
        
        self._init_ui()
        
        try:
            ThemeManager().theme_changed.connect(self.update_theme)
        except Exception as e:
            print(f"Error connecting to theme manager: {e}")
    
    def _init_ui(self):
        """Initialize dashboard UI"""
        try:
            layout = QVBoxLayout(self)
            layout.setSpacing(24)
            layout.setContentsMargins(0, 0, 0, 0)
            
            self.create_tabs(layout)
            self.create_metrics(layout)
            self.create_insights(layout)
            self.create_product_section(layout)
            self.create_financial_section(layout)
            
            layout.addStretch()
            
        except Exception as e:
            print(f"Error initializing dashboard UI: {e}")
    
    def create_tabs(self, parent_layout):
        """Create tab navigation"""
        try:
            tabs_widget = QWidget()
            tabs_widget.setObjectName("TabsWidget")
            layout = QHBoxLayout(tabs_widget)
            layout.setSpacing(10)
            layout.setContentsMargins(0, 0, 0, 0)
            
            tabs = ["Overview", "POS Dashboard", "ABC Dashboard"]
            self.tab_buttons = []
            
            for tab_name in tabs:
                btn =PrimaryButton (tab_name)
                # btn.setObjectName(f"TabButton_{tab_name.replace(' ', '')}")
                # btn.setProperty("class", "tab-button")
                btn.setCheckable(True)
                btn.setChecked(tab_name == self.current_tab)
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(lambda checked, t=tab_name: self.switch_tab(t))
                layout.addWidget(btn)
                self.tab_buttons.append((tab_name, btn))
            
            layout.addStretch()
            parent_layout.addWidget(tabs_widget)
            
        except Exception as e:
            print(f"Error creating tabs: {e}")
    
    def switch_tab(self, tab_name):
        """Switch active tab"""
        try:
            self.current_tab = tab_name
            for name, btn in self.tab_buttons:
                btn.setChecked(name == tab_name)
        except Exception as e:
            print(f"Error switching tab: {e}")
    
    def create_metrics(self, parent_layout):
        """Create metric cards section"""
        try:
            container = QWidget()
            container.setObjectName("MetricsContainer")
            layout = QHBoxLayout(container)
            layout.setSpacing(20)
            layout.setContentsMargins(0, 0, 0, 0)
            
            metrics = [
                ("Today Sales", "₹89,000", "+4.3%", "Down from yesterday", "💰", "red"),
                ("Today Purchase", "₹1,00,293", "+1.3%", "Up from past week", "🛒", "yellow"),
                ("Today Bills", "1805", "+1.3%", "Up from Yesterday", "📄", "purple"),
                ("To Pay", "₹40,689", "", "For 3 Vendors", "💸", "pink"),
            ]
            
            for title, value, change, subtitle, icon, color in metrics:
                card = self.create_metric_card(title, value, change, subtitle, icon, color)
                layout.addWidget(card)
            
            parent_layout.addWidget(container)
            
        except Exception as e:
            print(f"Error creating metrics: {e}")
    
    def create_metric_card(self, title, value, change, subtitle, icon, color):
        """Create a single metric card"""
        try:
            card = QFrame()
            card.setObjectName("MetricCard")
            card.setProperty("color", color)
            card.setSizePolicy(QWidget().sizePolicy().Expanding, QWidget().sizePolicy().Fixed)
            
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(15)
            
            # Left side: Text content
            text_layout = QVBoxLayout()
            text_layout.setSpacing(4)
            
            title_label = QLabel(title)
            title_label.setObjectName("MetricTitle")
            text_layout.addWidget(title_label)
            
            value_label = QLabel(value)
            value_label.setObjectName("MetricValue")
            text_layout.addWidget(value_label)
            
            if change:
                direction = "up" if "+" in change else "down"
                
                change_container = QWidget()
                change_layout = QHBoxLayout(change_container)
                change_layout.setContentsMargins(0, 0, 0, 0)
                change_layout.setSpacing(4)
                
                arrow_label = QLabel("↑" if direction == "up" else "↓")
                arrow_label.setObjectName("MetricArrow")
                arrow_label.setProperty("direction", direction)
                change_layout.addWidget(arrow_label)
                
                change_label = QLabel(change)
                change_label.setObjectName("MetricChange")
                change_label.setProperty("direction", direction)
                change_layout.addWidget(change_label)
                
                change_layout.addStretch()
                text_layout.addWidget(change_container)
            
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("MetricSubtitle")
            text_layout.addWidget(subtitle_label)
            
            text_layout.addStretch()
            
            # Right side: Icon
            icon_label = QLabel(icon)
            icon_label.setFixedSize(48, 48)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setObjectName("MetricIcon")
            
            card_layout.addLayout(text_layout)
            card_layout.addWidget(icon_label, 0, Qt.AlignTop)
            
            return card
            
        except Exception as e:
            print(f"Error creating metric card: {e}")
            return QFrame()
    
    def create_insights(self, parent_layout):
        """Create customer insights section"""
        try:
            section = QWidget()
            section.setObjectName("InsightsSection")
            section_layout = QVBoxLayout(section)
            section_layout.setSpacing(16)
            section_layout.setContentsMargins(0, 0, 0, 0)
            
            title = QLabel("Customer Insights")
            title.setObjectName("SectionTitle")
            section_layout.addWidget(title)
            
            cards_layout = QHBoxLayout()
            cards_layout.setSpacing(20)
            
            cards_data = [
                ("Total Customers", "With Loyalty Points", "1,685", False, 0, "#6366f1", "👥"),
                ("New Customers", "Today", "32", False, 0, "#10b981", "✨"),
                ("Returning", "Loyalty Points", "63%", True, 63, "#6366f1", None),
                ("Active Members", "Last 30 Days", "33%", True, 33, "#10b981", None),
            ]
            
            for card_title, subtitle, value, has_chart, percentage, color, icon in cards_data:
                card = self.create_insight_card(card_title, subtitle, value, has_chart, percentage, color, icon)
                cards_layout.addWidget(card)
            
            section_layout.addLayout(cards_layout)
            parent_layout.addWidget(section)
            
        except Exception as e:
            print(f"Error creating insights section: {e}")
    
    def create_insight_card(self, title, subtitle, value, has_chart, percentage, color, icon=None):
        """Create a single insight card"""
        try:
            card = QFrame()
            card.setObjectName("InsightCard")
            card.setSizePolicy(QWidget().sizePolicy().Expanding, QWidget().sizePolicy().Fixed)
            card.setMinimumHeight(200)
            
            layout = QVBoxLayout(card)
            layout.setSpacing(8)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title_label = QLabel(title)
            title_label.setObjectName("InsightTitle")
            layout.addWidget(title_label)
            
            # Subtitle
            subtitle_label = QLabel(subtitle)
            subtitle_label.setObjectName("InsightSubtitle")
            layout.addWidget(subtitle_label)
            
            layout.addSpacing(12)
            
            if has_chart:
                # Circular progress chart
                chart_container = QWidget()
                chart_container.setObjectName("InsightChart")
                chart_layout = QHBoxLayout(chart_container)
                chart_layout.setContentsMargins(0, 0, 0, 0)
                chart_layout.addStretch()
                
                progress = CircularProgress(percentage, color, 80)
                chart_layout.addWidget(progress)
                chart_layout.addStretch()
                
                layout.addWidget(chart_container)
            else:
                # Value with optional icon
                value_container = QWidget()
                value_layout = QHBoxLayout(value_container)
                value_layout.setContentsMargins(0, 0, 0, 0)
                value_layout.setSpacing(12)
                
                value_label = QLabel(value)
                value_label.setObjectName("InsightValue")
                value_layout.addWidget(value_label)
                
                value_layout.addStretch()
                
                # Add icon if provided
                if icon:
                    # Get color from the card's color parameter
                    icon_bg_color = f"{color}20"  # 20% opacity
                    
                    icon_container = QWidget()
                    icon_container.setFixedSize(48, 48)
                    icon_container.setStyleSheet(f"""
                        QWidget {{
                            background-color: {icon_bg_color};
                            border-radius: 24px;
                        }}
                    """)
                    
                    icon_container_layout = QVBoxLayout(icon_container)
                    icon_container_layout.setContentsMargins(0, 0, 0, 0)
                    
                    icon_label = QLabel(icon)
                    icon_label.setAlignment(Qt.AlignCenter)
                    icon_label.setStyleSheet(f"""
                        QLabel {{
                            font-size: 24px;
                            background: transparent;
                            border: none;
                        }}
                    """)
                    icon_container_layout.addWidget(icon_label)
                    
                    value_layout.addWidget(icon_container)
                
                layout.addWidget(value_container)
            
            layout.addStretch()
            
            return card
            
        except Exception as e:
            print(f"Error creating insight card: {e}")
            return QFrame()

    def create_product_section(self, parent_layout):
        """Create product performance section"""
        try:
            section = QWidget()
            section.setObjectName("ProductSection")
            section_layout = QVBoxLayout(section)
            section_layout.setSpacing(16)
            section_layout.setContentsMargins(0, 0, 0, 0)
            
            title = QLabel("Product Performance")
            title.setObjectName("SectionTitle")
            section_layout.addWidget(title)
            
            charts_container = QWidget()
            charts_layout = QHBoxLayout(charts_container)
            charts_layout.setSpacing(20)
            charts_layout.setContentsMargins(0, 0, 0, 0)
            
            top_selling_widget = BarChartWidget()
            top_chart = self.create_chart_card("Top-Selling Products", top_selling_widget)
            charts_layout.addWidget(top_chart, 1)
            
            least_selling_widget = HorizontalBarWidget()
            least_chart = self.create_chart_card("Least-Selling Products", least_selling_widget)
            charts_layout.addWidget(least_chart, 1)
            
            section_layout.addWidget(charts_container)
            parent_layout.addWidget(section)
            
        except Exception as e:
            print(f"Error creating product section: {e}")
    
    def create_financial_section(self, parent_layout):
        """Create financial summary section"""
        try:
            section = QWidget()
            section.setObjectName("FinancialSection")
            section_layout = QVBoxLayout(section)
            section_layout.setSpacing(16)
            section_layout.setContentsMargins(0, 0, 0, 0)
            
            title = QLabel("Financial Summary")
            title.setObjectName("SectionTitle")
            section_layout.addWidget(title)
            
            charts_layout = QHBoxLayout()
            charts_layout.setSpacing(20)
            
            revenue_chart = self.create_chart_card("Gross Revenue", LineChartWidget(show_series2=True))
            charts_layout.addWidget(revenue_chart)
            
            loyalty_chart = self.create_chart_card("Loyalty Discount", DualBarChartWidget())
            charts_layout.addWidget(loyalty_chart)
            
            section_layout.addLayout(charts_layout)
            parent_layout.addWidget(section)
            
        except Exception as e:
            print(f"Error creating financial section: {e}")
    
    def create_chart_card(self, title, chart_widget):
        """Create a chart card with title and chart"""
        try:
            card = QFrame()
            card.setObjectName("ChartCard")
            card.setSizePolicy(QWidget().sizePolicy().Expanding, QWidget().sizePolicy().Expanding)
            
            layout = QVBoxLayout(card)
            layout.setSpacing(16)
            layout.setContentsMargins(20, 20, 20, 20)
            
            # Title
            title_label = QLabel(title)
            title_label.setObjectName("ChartTitle")
            layout.addWidget(title_label)
            
            # Chart widget
            layout.addWidget(chart_widget, 1)
            
            return card
            
        except Exception as e:
            print(f"Error creating chart card: {e}")
            return QFrame()
    
    def update_theme(self):
        """Refresh styles when theme changes"""
        try:
            self.style().unpolish(self)
            self.style().polish(self)
            self.update()
        except Exception as e:
            print(f"Error updating theme: {e}")