
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
import os
from config.theme import Theme
from utils.get_theme import SystemTheme

class ThemeManager(QObject):
    theme_changed = pyqtSignal()
    _instance = None
    _qss = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            QObject.__init__(cls._instance)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self._system = SystemTheme()
        self._theme_config = Theme()
        self._theme_name = "light"
        self._theme_data = self._theme_config.get_theme(self._theme_name)
        self.apply_theme()

    def load_qss(self):
        if self._qss is None:
            qss_path = os.path.join(os.path.dirname(__file__), "../styles/main.qss")
            qss_path = os.path.abspath(qss_path)
            with open(qss_path, "r") as f:
                self._qss = f.read()
        return self._qss

    def apply_theme(self):
        qss = self.load_qss()
        print("Original QSS snippet:", qss[:200])  
        
        for key, value in self._theme_data.items():
           qss = qss.replace(f"{{{{{key}}}}}", value)
           print(f"Replaced {{{{{key}}}}} with {value}")
    
        print("Final QSS snippet:", qss[:200])  # Check after replacement
        QApplication.instance().setStyleSheet(qss)
        self.theme_changed.emit()

    def get(self, key, default=None):
        return self._theme_data.get(key, default)

    def get_theme_name(self):
        return self._theme_name

    def set_theme(self, theme_name):
        if theme_name == self._theme_name:
            return
        self._theme_name = theme_name
        self._theme_data = self._theme_config.get_theme(theme_name)
        self.apply_theme()

    def toggle_theme(self):
        new_theme = "light" if self._theme_name == "dark" else "dark"
        self.set_theme(new_theme)
