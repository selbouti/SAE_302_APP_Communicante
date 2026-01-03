from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, views):
        super().__init__()
        self.setWindowTitle("Covoiturage Daily - BlaBlaCar")
        self.setGeometry(100, 100, 1000, 700)

        self.current_user = None
        self.views = views

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.setCentralWidget(central_widget)

        for view in views.values():
            self.stack.addWidget(view)

    def set_current_user(self, user):
        self.current_user = user

    def switch_to(self, view_name):
        if view_name in self.views:
            view = self.views[view_name]

            if hasattr(view, "load"):
                view.load()
            elif hasattr(view, "refresh"):
                view.refresh()

            self.stack.setCurrentWidget(view)
