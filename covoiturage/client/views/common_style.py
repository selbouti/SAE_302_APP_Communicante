COMMON_STYLE = """
    QWidget {
        background: #ffffff;
        color: #1e1e1e;
        font-family: "Open Sans", "Segoe UI", Arial, sans-serif;
        font-size: 14px;
    }
    QLabel#titleLabel {
        color: #b00020;
        font-size: 22px;
        font-weight: 700;
        padding: 4px 0 8px 0;
    }
    QLabel {
        color: #4a4a4a;
    }
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QDateTimeEdit,
    QTimeEdit, QTextEdit, QListWidget {
        border: 1px solid #d9d9d9;
        border-radius: 6px;
        padding: 6px;
        background: #ffffff;
    }
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus,
    QDateEdit:focus, QDateTimeEdit:focus, QTimeEdit:focus, QTextEdit:focus,
    QListWidget:focus {
        border: 1px solid #c21807;
    }
    QLineEdit:read-only, QSpinBox:read-only, QDoubleSpinBox:read-only,
    QTextEdit:read-only, QComboBox:disabled, QDateEdit:disabled,
    QDateTimeEdit:disabled, QTimeEdit:disabled {
        background: #f5f5f5;
        color: #666666;
    }
    QComboBox::drop-down {
        border-left: 1px solid #d9d9d9;
    }
    QPushButton {
        background-color: #c21807;
        color: #ffffff;
        border: 1px solid #9c1a06;
        border-radius: 6px;
        padding: 8px 12px;
        font-weight: 600;
    }
    QPushButton:hover {
        background-color: #d6281a;
    }
    QPushButton:pressed {
        background-color: #8c1505;
    }
    QTableWidget {
        border: 1px solid #e6e6e6;
        border-radius: 6px;
        gridline-color: #e6e6e6;
        selection-background-color: #ffe6e6;
        selection-color: #b30000;
    }
    QHeaderView::section {
        background: #f7f7f7;
        color: #b00020;
        padding: 6px;
        border: 1px solid #e6e6e6;
        font-weight: 600;
    }
    QTabWidget::pane {
        border: 1px solid #e6e6e6;
        border-radius: 6px;
        top: -1px;
    }
    QTabBar::tab {
        background: #f7f7f7;
        color: #b00020;
        padding: 6px 10px;
        border: 1px solid #e6e6e6;
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    QTabBar::tab:selected {
        background: #ffffff;
        color: #b00020;
        font-weight: 600;
    }
    QFrame#loginCard, QFrame#homeCard {
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        background: #ffffff;
    }
"""
