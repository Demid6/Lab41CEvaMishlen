# screens/admin.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QInputDialog, QLineEdit
)
from PySide6.QtCore import Qt, Signal

from theme import (
    BG, WHITE, ACCENT, ACCENT_DARK, SOFT, TEXT, MUTED,
    FONT_HEAD, FONT_BODY
)
from logic.storage import load_products, load_orders, save_order


class AdminScreen(QWidget):
    logout_requested = Signal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setStyleSheet(f"background: {BG};")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        body = QHBoxLayout()
        body.setContentsMargins(28, 16, 28, 16)
        body.setSpacing(18)

        # Меню
        menu = QFrame()
        menu.setFixedWidth(220)
        menu.setStyleSheet(f"background: {WHITE}; border-radius: 20px;")
        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(14, 14, 14, 14)
        menu_layout.setSpacing(6)

        for item in ["📊 Отчёт по продажам", "🍰 Товары", "👥 Сотрудники"]:
            btn = QPushButton(item)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {TEXT};
                    text-align: left;
                    padding: 12px 14px;
                    border-radius: 12px;
                    font-weight: 700;
                }}
                QPushButton:hover {{
                    background: {SOFT};
                }}
            """)
            btn.clicked.connect(lambda checked, i=item: self._on_menu(i))
            menu_layout.addWidget(btn)

        menu_layout.addStretch()
        body.addWidget(menu)

        # Контент
        content = QFrame()
        content.setStyleSheet(f"background: {WHITE}; border-radius: 20px;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(12)

        title = QLabel("Отчёт по продажам")
        title.setObjectName("h2")
        content_layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["№ заказа", "Кассир", "Позиций", "Сумма", "Дата"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: {WHITE};
                border: 1px solid #eee;
                border-radius: 12px;
                gridline-color: #f0e0e6;
                font-size: 13px;
            }}
            QHeaderView::section {{
                background: {SOFT};
                color: {ACCENT_DARK};
                font-weight: 700;
                padding: 10px;
                border: none;
            }}
        """)
        content_layout.addWidget(self.table)

        # Итог
        self.total_label = QLabel("Итого: 0 ₽")
        self.total_label.setStyleSheet(f"""
            font-family: "{FONT_HEAD}";
            font-size: 20px;
            font-weight: 700;
            color: {ACCENT_DARK};
        """)
        content_layout.addWidget(self.total_label)

        body.addWidget(content, 1)
        root.addLayout(body, 1)

        self._load_orders()

    def _build_header(self):
        header = QFrame()
        header.setStyleSheet(f"background: {WHITE};")
        header.setFixedHeight(82)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(28, 0, 28, 0)

        logo = QLabel("👑")
        logo.setStyleSheet("font-size: 32px;")
        layout.addWidget(logo)

        title_box = QVBoxLayout()
        title = QLabel("Ева-Мишлен")
        title.setStyleSheet(f"""
            font-family: "{FONT_HEAD}";
            font-size: 26px;
            font-weight: 700;
            color: {ACCENT_DARK};
        """)
        sub = QLabel("Панель администратора")
        sub.setStyleSheet(f"font-size: 12px; color: {MUTED};")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        layout.addLayout(title_box)
        layout.addStretch()

        name = QLabel(self.user["name"])
        name.setStyleSheet("font-weight: 700; font-size: 15px;")
        layout.addWidget(name)

        exit_btn = QPushButton("Выход")
        exit_btn.setObjectName("accent")
        exit_btn.setFixedHeight(42)
        exit_btn.clicked.connect(self.logout_requested.emit)
        layout.addWidget(exit_btn)

        return header

    def _load_orders(self):
        orders = load_orders()
        self.table.setRowCount(len(orders))
        total = 0
        for row, order in enumerate(orders):
            self.table.setItem(row, 0, QTableWidgetItem(order["order_id"]))
            self.table.setItem(row, 1, QTableWidgetItem(order["cashier"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(len(order["items"]))))
            self.table.setItem(row, 3, QTableWidgetItem(f"{order['total']:,} ₽".replace(",", " ")))
            self.table.setItem(row, 4, QTableWidgetItem(order["created_at"][:16].replace("T", " ")))
            total += order["total"]
        self.total_label.setText(f"Итого: {total:,} ₽".replace(",", " "))

    def _on_menu(self, item):
        if "Отчёт" in item:
            self._load_orders()
        else:
            QMessageBox.information(self, "Раздел", f"Раздел «{item}» в разработке")