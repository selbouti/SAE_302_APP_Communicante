from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, views):
        super().__init__()
        self.setWindowTitle("Covoiturage Daily - BlaBlaCar")
        self.setGeometry(100, 100, 1000, 700)
        
        self.current_user = None
        self.views = views
        
        # Widget central avec layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # QStackedWidget pour naviguer entre les vues
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Ajouter les views si elles existent
        for view in views.values():
            self.stack.addWidget(view)
    
    def switch_to(self, view_name):
        if view_name in self.views:
            self.stack.setCurrentWidget(self.views[view_name])