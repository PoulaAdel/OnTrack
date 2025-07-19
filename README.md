```markdown
# Workflow Timer

An on-screen, YAML-driven workflow timer with a modern PySide6 UI. Define your study or work process in a simple YAML file, then let the app guide you through each step with countdown timers, step titles, and descriptions.

---

## Features

- Load a multi-step workflow from YAML  
- Display step **name** and **description**  
- Start/Pause and skip to the next step  
- Automatic pop-up when a step completes  
- Packaged as a single EXE with PyInstaller  
- Windows installer via NSIS  
- CI/CD pipeline with GitHub Actions  

---

## Requirements

- **Python** 3.8+ (tested on 3.10)  
- **Packages** (see `requirements.txt`):  
  - PySide6  
  - PyYAML  
- **Build tools** (Windows):  
  - PyInstaller (bundled via `build.bat`)  
  - NSIS (for `installer.nsi`)  

---

## Installation

1. Clone this repo  
2. Install Python dependencies  
   ```bash
   pip install -r requirements.txt
   ```

---

## Defining Your Workflow

Create a `workflow.yaml`:

```yaml
workflow:
  - name: "Intro & Headings"
    description: "Skim chapter intros and note key concepts"
    duration_min: 15

  - name: "First-Pass Skim"
    description: "Quickly scan for sections needing deeper study"
    duration_min: 30

  - name: "Deep Read"
    description: "Carefully read the flagged sections"
    duration_min: 60

  - name: "Hands-On Exercise"
    description: "Implement code examples in your IDE"
    duration_min: 60

  - name: "Quick Review"
    description: "Review your summaries and flashcards"
    duration_min: 15
```

---

## Running the App

```bash
python timer_app.py workflow.yaml
```

- If you omit the `workflow.yaml` path, a file dialog will prompt you to select one.  
- The UI presents the step title, description, and a large countdown timer.  
- Click **Start** to begin, **Pause** to stop, and **Next** to skip.  

---

## Building a Standalone Executable

On Windows, run:

```bat
build.bat
```

- Installs dependencies  
- Cleans old builds  
- Bundles `timer_app.py` into `dist\WorkflowTimer.exe`  

---

## Creating a Windows Installer

With NSIS installed:

```bat
makensis installer.nsi
```

This produces `dist\WorkflowTimer_Installer.exe` which:

- Installs the EXE into `Program Files\WorkflowTimer`  
- Creates Start menu and desktop shortcuts  

---

## CI/CD (GitHub Actions)

The included `.github/workflows/build.yml` does:

1. Checkout code  
2. Set up Python  
3. Install dependencies and PyInstaller  
4. Build the EXE via `build.bat`  
5. Install NSIS and create an installer  
6. Upload both the EXE and installer as build artifacts  

---

## Key Code Snippets

### Loading the Workflow

```python
def load_workflow(path: str) -> list[WorkflowStep]:
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return [
        WorkflowStep(
            name=item["name"],
            description=item.get("description", ""),
            duration_sec=item["duration_min"] * 60
        )
        for item in data.get("workflow", [])
    ]
```

### Starting and Pausing the Timer

```python
def start_pause(self):
    self.paused = not self.paused
    if self.paused:
        self.timer.stop()
        self.btn_start.setText("Start")
    else:
        self.timer.start(1000)
        self.btn_start.setText("Pause")
```

---

## Contribution & License

- **License**: MIT  
- Contributions via GitHub issues and pull requests are welcome!  
```