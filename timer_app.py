import sys
import yaml
from dataclasses import dataclass
from PySide6.QtCore import QTimer, Qt, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox,
    QSystemTrayIcon, QMenu, QStyle
)

@dataclass
class WorkflowStep:
    name: str
    description: str
    duration_sec: int

class OnTrack(QWidget):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self.index = 0
        self.remaining = 0
        self.paused = True
        self.drag_pos = QPoint()

        self._init_ui()
        self._load_step(0)
        self._snap_to_corner()

    def _init_ui(self):
        # Frameless, transparent, always-on-top widget
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Fixed compact size
        self.setFixedSize(300, 180)

        # Header
        self.label_header = QLabel("", self)
        self.label_header.setAlignment(Qt.AlignCenter)
        self.label_header.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 200);
        """)

        # Description
        self.label_desc = QLabel("", self)
        self.label_desc.setAlignment(Qt.AlignCenter)
        self.label_desc.setWordWrap(True)
        self.label_desc.setStyleSheet("""
            font-size: 12px;
            color: white;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 200);
        """)

        # Timer display
        self.label_timer = QLabel("", self)
        self.label_timer.setAlignment(Qt.AlignCenter)
        self.label_timer.setStyleSheet("""
            font-size: 36px;
            color: white;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 200);
        """)

        # Buttons
        self.btn_start = QPushButton("Start", self)
        self.btn_start.clicked.connect(self.start_pause)

        self.btn_next = QPushButton("Next", self)
        self.btn_next.clicked.connect(self.next_step)

        self.btn_minimize = QPushButton("—", self)
        self.btn_minimize.clicked.connect(self.hide)

        self.btn_pin = QPushButton("Unpin", self)
        self.btn_pin.clicked.connect(self.toggle_pin)

        self.btn_quit = QPushButton("Quit", self)
        self.btn_quit.clicked.connect(self._quit)

        # Layout
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(8, 8, 8, 8)
        vbox.setSpacing(4)
        vbox.addWidget(self.label_header)
        vbox.addWidget(self.label_desc)
        vbox.addWidget(self.label_timer)

        hbox = QHBoxLayout()
        hbox.setSpacing(4)
        for btn in (self.btn_start, self.btn_next,
                    self.btn_minimize, self.btn_pin, self.btn_quit):
            btn.setFixedHeight(24)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(50, 50, 50, 220);
                    color: white;
                    border: 1px solid rgba(100, 100, 100, 180);
                    border-radius: 4px;
                    padding: 2px 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(70, 70, 70, 240);
                    border: 1px solid rgba(150, 150, 150, 200);
                }
                QPushButton:pressed {
                    background-color: rgba(30, 30, 30, 250);
                }
            """)
            hbox.addWidget(btn)
        vbox.addLayout(hbox)

        # Transparent background style
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 20, 240);
                color: white;
                border: 2px solid rgba(100, 100, 100, 150);
                border-radius: 8px;
            }
        """)

        # Timer tick
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

        # System tray icon
        icon = QApplication.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray = QSystemTrayIcon(icon, self)
        self.tray.setToolTip("Workflow Timer")
        menu = QMenu()
        menu.addAction("Restore", self.show)
        menu.addAction("Quit", self._quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(lambda reason: self.show() if reason == QSystemTrayIcon.Trigger else None)
        self.tray.show()

    def _snap_to_corner(self):
        screen = QApplication.primaryScreen().availableGeometry()
        margin = 20
        x = screen.width() - self.width() - margin
        y = screen.height() - self.height() - margin
        self.move(x, y)

    def _load_step(self, idx):
        if idx >= len(self.steps):
            QMessageBox.information(self, "Done", "Workflow complete!")
            self.fade_out()
            return

        step = self.steps[idx]
        self.label_header.setText(f"Step {idx+1}/{len(self.steps)}: {step.name}")
        self.label_desc.setText(step.description)
        self.remaining = step.duration_sec
        self._update_timer_display()

        self.paused = True
        self.btn_start.setText("Start")
        self.timer.stop()

    def _update_timer_display(self):
        m, s = divmod(self.remaining, 60)
        self.label_timer.setText(f"{m:02d}:{s:02d}")

    def _tick(self):
        if not self.paused and self.remaining > 0:
            self.remaining -= 1
            self._update_timer_display()
        elif self.remaining == 0:
            QMessageBox.information(
                self, "Step Complete",
                f"Finished: {self.steps[self.index].name}"
            )
            self.next_step()

    def start_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.timer.stop()
            self.btn_start.setText("Start")
        else:
            self.timer.start(1000)
            self.btn_start.setText("Pause")

    def next_step(self):
        self.index += 1
        self._load_step(self.index)

    def toggle_pin(self):
        flags = self.windowFlags()
        if flags & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
            self.btn_pin.setText("Pin")
        else:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
            self.btn_pin.setText("Unpin")
        self.show()

    def fade_out(self):
        for i in range(10):
            QTimer.singleShot(i * 50, lambda alpha=1 - i/10: self.setWindowOpacity(alpha))
        QTimer.singleShot(600, self.hide)

    def _quit(self):
        self.tray.hide()
        QApplication.quit()

    # Make widget draggable
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

def load_workflow(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    steps = []
    for item in data.get('workflow', []):
        steps.append(WorkflowStep(
            name=item.get('name', ''),
            description=item.get('description', ''),
            duration_sec=item.get('duration_min', 0) * 60
        ))
    return steps

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if len(sys.argv) > 1:
        yaml_path = sys.argv[1]
    else:
        yaml_path, _ = QFileDialog.getOpenFileName(
            None, "Select workflow YAML", "", "YAML Files (*.yaml *.yml)"
        )
        if not yaml_path:
            sys.exit()

    try:
        steps = load_workflow(yaml_path)
        if not steps:
            raise ValueError("No steps defined in workflow.")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to load workflow:\n{e}")
        sys.exit()

    widget = OnTrack(steps)
    widget.show()
    sys.exit(app.exec())
