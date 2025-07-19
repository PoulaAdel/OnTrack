import sys
import yaml
from dataclasses import dataclass
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)

@dataclass
class WorkflowStep:
    name: str
    description: str
    duration_sec: int

class WorkflowTimer(QWidget):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self.index = 0
        self.remaining = 0
        self.paused = True

        self._init_ui()
        self._load_step(0)

    def _init_ui(self):
        self.setWindowTitle("Workflow Timer")
        self.resize(500, 300)

        # Header and Description
        self.label_header = QLabel("", self)
        self.label_header.setAlignment(Qt.AlignCenter)
        self.label_header.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.label_desc = QLabel("", self)
        self.label_desc.setAlignment(Qt.AlignCenter)
        self.label_desc.setWordWrap(True)

        # Timer Display
        self.label_timer = QLabel("", self)
        self.label_timer.setAlignment(Qt.AlignCenter)
        self.label_timer.setStyleSheet("font-size: 48px;")

        # Control Buttons
        self.btn_start = QPushButton("Start", self)
        self.btn_start.clicked.connect(self.start_pause)

        self.btn_next = QPushButton("Next", self)
        self.btn_next.clicked.connect(self.next_step)

        self.btn_quit = QPushButton("Quit", self)
        self.btn_quit.clicked.connect(self.close)

        # Layout setup
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_header)
        vbox.addWidget(self.label_desc)
        vbox.addWidget(self.label_timer)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_start)
        hbox.addWidget(self.btn_next)
        hbox.addWidget(self.btn_quit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Timer logic
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

    def _load_step(self, idx):
        if idx >= len(self.steps):
            QMessageBox.information(self, "Done", "Workflow complete!")
            self.close()
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

def load_workflow(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    steps = []
    for item in data.get('workflow', []):
        name = item.get('name', '')
        desc = item.get('description', '')
        sec = item.get('duration_min', 0) * 60
        steps.append(WorkflowStep(name, desc, sec))
    return steps

def main():
    app = QApplication(sys.argv)

    # Select YAML if not provided as argument
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path, _ = QFileDialog.getOpenFileName(
            None, "Select workflow YAML", "", "YAML Files (*.yaml *.yml)"
        )
        if not path:
            return

    try:
        steps = load_workflow(path)
        if not steps:
            raise ValueError("No steps defined.")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to load workflow:\n{e}")
        return

    timer = WorkflowTimer(steps)
    timer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
