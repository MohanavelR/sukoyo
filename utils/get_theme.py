import platform
import subprocess

class SystemTheme:
    DARK = "dark"
    LIGHT = "light"

    def __init__(self):
        self.theme = self._detect_theme()

    def _detect_theme(self):
        os_name = platform.system()
        if os_name == "Linux":
            return self._detect_linux_theme()
        elif os_name == "Windows":
            return self._detect_windows_theme()
        elif os_name == "Darwin":
            return self._detect_macos_theme()
        return self.LIGHT

    def _detect_linux_theme(self):
        try:
            gtk_theme = subprocess.check_output(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                stderr=subprocess.DEVNULL
            ).decode().strip().strip("'")
            return self.DARK if "dark" in gtk_theme.lower() else self.LIGHT
        except subprocess.SubprocessError:
            return self.LIGHT

    def _detect_windows_theme(self):
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            ) as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return self.DARK if value == 0 else self.LIGHT
        except OSError:
            return self.LIGHT

    def _detect_macos_theme(self):
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return self.DARK if result.returncode == 0 else self.LIGHT
        except subprocess.SubprocessError:
            return self.LIGHT

    # Public API
    def get_theme(self):
        return self.theme

    def is_dark_mode(self):
        return self.theme == self.DARK

    def is_light_mode(self):
        return self.theme == self.LIGHT

    def override_theme(self, theme_name):
        if theme_name in (self.DARK, self.LIGHT):
            self.theme = theme_name

    def refresh(self):
        self.theme = self._detect_theme()
        return self.theme
