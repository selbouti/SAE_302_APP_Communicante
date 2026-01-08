COMMON_STYLE = """
    QWidget {
        background: #ffffff;
        color: #1e1e1e;
        font-family: "Open Sans", "Segoe UI", Arial, sans-serif;
        font-size: 14px;
    }
    QLabel#titleLabel {
        color: #7a1111;
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
        border: 1px solid #8b1a1a;
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
        background-color: #8b1a1a;
        color: #ffffff;
        border: 1px solid #6f1212;
        border-radius: 6px;
        padding: 8px 12px;
        font-weight: 600;
    }
    QPushButton:hover {
        background-color: #a32020;
    }
    QPushButton:pressed {
        background-color: #6b1212;
    }
    QTableWidget {
        border: 1px solid #e6e6e6;
        border-radius: 6px;
        gridline-color: #e6e6e6;
        selection-background-color: #f3dede;
        selection-color: #7a1111;
    }
    QHeaderView::section {
        background: #f7f7f7;
        color: #7a1111;
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
        color: #7a1111;
        padding: 6px 10px;
        border: 1px solid #e6e6e6;
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    QTabBar::tab:selected {
        background: #ffffff;
        color: #7a1111;
        font-weight: 600;
    }
    QFrame#loginCard, QFrame#homeCard {
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        background: #ffffff;
    }
    QGroupBox {
        border: 1px solid #e6e6e6;
        border-radius: 6px;
        margin-top: 10px;
        padding: 8px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
        color: #7a1111;
        font-weight: 600;
    }
"""
