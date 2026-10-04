# app.py
# Точка входа приложения «Ева-Мишлен»
# Запуск: python app.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QFont

from theme import get_stylesheet, FONT_BODY
from screens.login import LoginScreen
from screens.cashier import CashierScreen
from screens.admin import AdminScreen


class MainWindow(QMainWindow):
    """Главное окно приложения с навигацией между экранами"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ева-Мишлен · Прототип")
        self.resize(1440, 900)
        self.setStyleSheet(get_stylesheet())

        # Стек экранов: один активен, остальные скрыты
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Экран авторизации — стартовый
        self.login_screen = LoginScreen()
        self.login_screen.logged_in.connect(self._on_login)
        self.stack.addWidget(self.login_screen)

    def _on_login(self, user):
        """Пользователь успешно вошёл — открываем нужный экран"""
        # Удаляем старые экраны (если были)
        while self.stack.count() > 1:
            w = self.stack.widget(1)
            self.stack.removeWidget(w)
            w.deleteLater()

        # Выбираем экран по роли
        if user["role"] == "cashier":
            screen = CashierScreen(user)
        elif user["role"] == "admin":
            screen = AdminScreen(user)
        else:
            return

        screen.logout_requested.connect(self._logout)
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)

    def _logout(self):
        """Выход — возвращаемся на экран авторизации"""
        while self.stack.count() > 1:
            w = self.stack.widget(1)
            self.stack.removeWidget(w)
            w.deleteLater()
        self.stack.setCurrentWidget(self.login_screen)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont(FONT_BODY, 10))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()