from app.window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from config.theme_manager import ThemeManager
import sys
def run_app():
    app=QApplication(sys.argv)
    app.setFont(QFont("inter"))
    theme=ThemeManager()
    theme.apply_theme()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()