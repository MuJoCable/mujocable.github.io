# MuJoCable on Windows: from setup to an elbow simulation

For Windows users setting up MuJoCable for the first time and editing models in VS Code. Tutorial version: September 20, 2026.

By the end, you will have an isolated Python environment, a working four-cable elbow model, and a repeatable workflow for flexing, returning, releasing the drive cables, and exporting data and video.

**Workflow: VS Code → Python → project files → virtual environment → MuJoCo → cable plugin → elbow demo → results.** This guide uses native Windows. WSL, Linux, Conda, and a C++ compiler are not required.

## 0. Choose a package and check your computer

### What each component does

| Component | Role | Installation |
|---|---|---|
| VS Code | Edit Python and MJCF; run and debug scripts | Windows desktop installer |
| Python | Execute the simulation controller | Python 3.12.10 x64 installer |
| MuJoCo | Rigid-body physics engine | Install version 3.4.0 with pip in the project environment |
| MuJoCable | Cable mechanics, surface routing, and cable-length actuation | Project-local Windows DLL loaded by Python |
| Elbow demo | MJCF, meshes, four cables, and controller | Tutorial project archive |

The **VS Code Python extension** and **MuJoCable** are different components. Install the former from the VS Code Extensions view. MuJoCable is a MuJoCo engine plugin, not a VS Code extension.

### Requirements

- Windows 10 or 11 on an Intel/AMD x64 computer. Check **Settings → System → About → System type**. This is not a 32-bit Python or native Windows ARM64 package.
- A working OpenGL graphics driver for the viewer and video export. You can check headless simulation separately.
- Internet access to download VS Code, Python, and pip dependencies. Once installed, the supplied simulation runs offline.
- A short, writable path is recommended, such as `C:\work\elbow_demo`. **C: is not required**: `D:\work\elbow_demo` or another drive works too. Short ASCII paths avoid problems in third-party file interfaces.

### Downloads

| Resource | Download | Use |
|---|---|---|
| VS Code | [Official download page](https://code.visualstudio.com/download) | Windows → User Installer → x64 |
| Python 3.12.10 | [Release page](https://www.python.org/downloads/release/python-31210/) · [64-bit installer](https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe) | Windows installer (64-bit) |
| **Tutorial project** | [MuJoCable_Elbow_Windows_Project.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_Elbow_Windows_Project.zip) | Recommended for development; includes model, DLL, scripts, and VS Code configuration, without Python |
| Portable demo | [MuJoCable_Windows_x64.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_Windows_x64.zip) | Includes Python; quick-start option in section 13 |
| Plugin only | [MuJoCable_plugin_Windows_x64.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_plugin_Windows_x64.zip) | For an existing MuJoCo project; section 12 |
| Upstream plugin source | [MuJoCable v0.2.0 Release](https://github.com/MuJoCable/mujoco-cable-dynamics/releases/tag/v0.2.0) | Source used for this DLL; no compilation needed for this guide |

Archives are distributed through a GitHub Release of this website repository. Choose the tutorial project for the main workflow; you do not need all three packages.

This Windows DLL is an **adapted build of upstream v0.2.0 plus the elbow cylinder-routing patch**, not an unchanged upstream prebuilt asset. Source, patches, and license notices are included.

## 1. Install VS Code

1. Open the [VS Code download page](https://code.visualstudio.com/download). Select **Windows / User Installer / x64** to download the desktop `.exe` installer.
2. Run `VSCodeUserSetup-…-x64.exe` and follow the installer. User Installer installs for the current account.
3. Keep **Add to PATH** selected if shown. Explorer context-menu entries are optional.
4. Start VS Code. Reopen any terminals that were already running so they receive the updated PATH.
5. Open Extensions with `Ctrl+Shift+X`. Search for **Python**, published by **Microsoft**, with extension ID `ms-python.python`, and install it.
6. Check that Microsoft's **Python Debugger** (`ms-python.debugpy`) is also installed; it is used for F5 debugging.

**Checkpoint:** VS Code opens and the Microsoft Python extension is installed. The Python interpreter is installed separately in the next section.

References: [VS Code Windows installation](https://code.visualstudio.com/docs/setup/windows), [Microsoft Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

## 2. Install Python 3.12.10, 64-bit

This guide pins Python 3.12.10 x64 to match the tested baseline. It is not a claim that this is the latest Python release.

1. On the [Python 3.12.10 release page](https://www.python.org/downloads/release/python-31210/), choose **Windows installer (64-bit)** under Files. The filename is `python-3.12.10-amd64.exe`.
2. Run it, select **Add python.exe to PATH**, and choose **Install Now**. Retain pip and the Python launcher installation options.
3. When installation finishes, reopen VS Code.
4. Select **Terminal → New Terminal** and use a PowerShell terminal.
5. Run these commands, one line at a time:

```powershell
py -3.12 --version
py -3.12 -c "import struct; print(struct.calcsize('P') * 8)"
```

Expected output: `Python 3.12.10`, then `64`. The `py -3.12` command explicitly selects Python 3.12 when several versions are installed.

**Use the standard installer, not the embeddable package, for this workflow.** The standard installation supplies pip and venv. The embedded interpreter in the portable demo serves a different purpose.

If `py` is not recognized, reopen the terminal and check that the Python launcher is installed. Alternatively, use the interpreter's actual full path. A common per-user installation path is:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" --version
```

If you chose another installation directory, use that path instead.

## 3. Extract the project and open the correct folder

1. Download **MuJoCable_Elbow_Windows_Project.zip** from section 0.
2. In File Explorer, right-click the archive and select **Extract All**.
3. Locate the extracted folder that directly contains `run_demo.py`. Move it to `C:\work` and rename it `elbow_demo`, or choose another writable location.
4. In VS Code, select **File → Open Folder** and open that project folder.
5. Accept Workspace Trust only after confirming that the files came from the linked MuJoCable repository.

The project layout is:

```text
C:\work\elbow_demo\
├─ .vscode\                    Interpreter and debugging configuration
├─ requirements-windows.txt    Pinned Python dependencies
├─ check_mujoco.py             Check base MuJoCo only
├─ check_env.py                Check cable plugin and elbow model
├─ mujocable_plugin.py         Windows DLL loader
├─ runtime.py                  Project model-loading entry point
├─ run_demo.py                 Elbow controller and data recording
├─ verify_results.py           Compare results with the reference
├─ render_video.py             Export video, GIF, and snapshots
├─ open_model.py               Generic viewer for other XML models
├─ plugin\cable_unilateral.dll Cable plugin
├─ msvcp140.dll                App-local C++ runtime libraries
├─ vcruntime140.dll
├─ vcruntime140_1.dll
├─ model\elbow.xml             Elbow MJCF
├─ model\assets\               Exported meshes
├─ examples\single_pulley.xml  Small cable example
├─ reference\                  Baseline data and video
└─ validation\                 Test evidence
```

The commands below use C: as an example. If you chose D:, change the path after `Set-Location`; subsequent relative commands starting with `.\` stay the same. VS Code, Python, and the project may reside on different drives.

```powershell
Set-Location C:\work\elbow_demo
Test-Path .\run_demo.py
Test-Path .\plugin\cable_unilateral.dll
```

Both checks should return `True`. If either returns `False`, fix the working directory before continuing. Open the folder containing `run_demo.py`, not its parent.

## 4. Create an isolated Python environment

From the project root, run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
```

The last command should print your project's `.venv\Scripts\python.exe`. If `py` is unavailable, replace `py -3.12` in the first command with the standard Python interpreter's full path.

**All subsequent commands explicitly use `.\.venv\Scripts\python.exe`.** You do not need to run `Activate.ps1` or change PowerShell execution policy. Do not copy the terminal's `PS C:\…>` prompt into commands.

Select the same interpreter in VS Code:

1. Press `Ctrl+Shift+P`.
2. Run **Python: Select Interpreter**.
3. Select the project's `.venv`. If missing, choose **Enter interpreter path** and locate its `Scripts\python.exe`.

The selected interpreter controls VS Code execution and language features. Explicit terminal paths ensure that installation and execution use the intended environment. See [Python venv](https://docs.python.org/3.12/library/venv.html) and [VS Code environments](https://code.visualstudio.com/docs/python/environments).

If you move the project after creating `.venv`, recreate the environment and reinstall dependencies at the new location. Do not transfer an existing `.venv` between directories or computers.

## 5. Install MuJoCo and dependencies

Run each line only after the preceding command succeeds:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r .\requirements-windows.txt
.\.venv\Scripts\python.exe -m pip check
```

The requirements include **MuJoCo 3.4.0, NumPy 2.2.6, Pillow 11.3.0, and imageio-ffmpeg 0.6.0**, with pinned supporting packages. `--only-binary=:all:` uses prebuilt wheels and avoids an unexpected compiler setup. If no matching wheel is available, check Python version, architecture, and package-index connectivity.

The last command should report `No broken requirements found.` Then check the base engine:

```powershell
.\.venv\Scripts\python.exe .\check_mujoco.py
```

Expected output includes:

```text
MuJoCo: 3.4.0
PASS: base MuJoCo advanced 100 steps; no cable plugin loaded.
```

This simulates a small sphere without registering the cable plugin. It distinguishes engine-installation problems from cable-plugin or model problems. The script configures the project-local runtime-library directory first.

The MuJoCo Python wheel includes the engine library; no separate engine download or legacy `mujoco-py` installation is needed. Keep **3.4.0** with this DLL. See the [official MuJoCo Python installation guide](https://mujoco.readthedocs.io/en/3.4.0/python.html#installation).

## 6. Install and verify the MuJoCable plugin

### Project-local installation

Extraction in section 3 already placed the required files:

- `plugin/cable_unilateral.dll`: Windows x64 cable plugin.
- `mujocable_plugin.py`: configures DLL directories and loads the plugin.
- The three runtime DLLs at the project root: retain their locations.
- `runtime.py`: loads models for this project.

There is **no additional MuJoCable pip-install step** in this workflow. Do not copy DLLs into Windows/System32. No administrator privileges, registry edits, or C++ compilation are required for ordinary use.

### Verify a small example, then the elbow

```powershell
.\.venv\Scripts\python.exe .\open_model.py .\examples\single_pulley.xml --check
.\.venv\Scripts\python.exe .\check_env.py
```

The first command should print `PASS` after advancing a one-cable example by 1000 steps. The elbow check should include:

```json
{
  "passed": true,
  "mujoco": "3.4.0",
  "cables": 4,
  "actuators": 2
}
```

The actual report also contains dependency versions, routing status, and the DLL hash. It is saved as `results/environment_check.json`. The elbow has two driven cables and two passive cables.

Plugin registration is per process: **load the DLL before compiling XML that references the plugin**. `runtime.py` handles this ordering. Opening the XML in an ordinary viewer that has not loaded the DLL may produce an unknown-plugin error.

## 7. Run the elbow demo

```powershell
.\.venv\Scripts\python.exe .\run_demo.py
```

After loading, a MuJoCo window opens. The controller changes the two drive cables' free lengths; structural contact participates in the simulation.

| Simulation time | Expected motion |
|---|---|
| 0–0.5 s | Initial state |
| 0.5–12.5 s | Large flexion |
| 12.5–14.5 s | Hold near maximum flexion |
| 14.5–26.5 s | Return to the initial position |
| 26.5–27.5 s | Brief hold |
| 27.5–29 s | Pay out the drive cables |
| 29–32 s | Remain released; low-tension cables appear gray |

The nominal target is 180°, but contact limits the baseline peak to approximately **178.8°**. Do not force joint coordinates to reach 180°. Gray indicates tension below 0.02 N for display purposes, not deletion of a cable.

- **Space:** pause or resume.
- **R:** reset and run again.
- **Close the window:** exit. At 32 simulated seconds the demo pauses without closing automatically.
- Simulation time need not equal wall-clock time; speed depends on the computer.

Interactive mode is for observation. **It does not generate the CSV used for verification.** Use headless mode in section 8 to record data. Opening `model/elbow.xml` with the generic viewer also does not attach the dedicated elbow controller.

Reference motion:

<video controls preload="metadata" poster="media/elbow-maximum.png" src="media/elbow.mp4" aria-label="Reference elbow motion"></video>

### Run with F5 in VS Code

The project includes `.vscode/launch.json`. Once `.venv` and dependencies exist, open **Run and Debug**, choose **Elbow demo**, and press F5.

Other configurations are **Environment check**, **Elbow headless**, **Verify results**, and **Single pulley**. They explicitly use the project environment. Code Runner is unnecessary and may select a different interpreter.

## 8. Record a full run and verify results

Close the interactive viewer, then run:

```powershell
.\.venv\Scripts\python.exe .\run_demo.py --headless
.\.venv\Scripts\python.exe .\verify_results.py
```

**Wait for the first command to finish successfully before running the second.** The simulation prints progress roughly every two simulated seconds and writes results after the 32-second run. Verification compares them with the supplied reference.

| Output | Contents |
|---|---|
| `results/motion.csv` | Angles, cable commands, tensions, and contact data sampled about every 0.02 s |
| `results/summary.json` | Peak flexion, return angle, released tension, warnings, and other summaries |
| `results/environment.json` | Interpreter/dependency versions and model/DLL hashes |
| `results/verification.json` | Individual checks and overall `passed` status |

| Metric | Baseline / acceptance condition |
|---|---|
| Peak flexion | Baseline about 178.8146°; within 1° of reference |
| Return angle | Baseline about −0.0165°; absolute value below 1° |
| Released drive-cable tension | Baseline 0 N; maximum below 0.02 N |
| Duration | 32 s within floating-point integration tolerance |
| Angle-trajectory RMSE | Below 2° relative to reference |
| Dynamics warnings | None |
| Maximum contact-proxy penetration | Below 0.05 mm |
| Route status | Below 2; status 1 is accepted for this baseline |

A successful report contains `"passed": true` and nine individual checks. Small floating-point differences across platforms are expected; identical CSV bytes are not required. Preserve failed results for diagnosis rather than immediately relaxing thresholds.

New runs overwrite files with the same names in `results`. Before another experiment, copy the results into a separate directory, such as `experiments/baseline/results`, together with the corresponding model, controller, and environment record.

## 9. Export video, GIF, and snapshots

Complete section 8 first. Ensure `results/motion.csv` is the run you want to visualize. In PowerShell:

```powershell
$env:ELBOW_FONT = "$env:WINDIR\Fonts\times.ttf"
$env:ELBOW_FONT_BOLD = "$env:WINDIR\Fonts\timesbd.ttf"
Test-Path $env:ELBOW_FONT
Test-Path $env:ELBOW_FONT_BOLD
```

If both checks return `True`, run:

```powershell
.\.venv\Scripts\python.exe .\render_video.py
```

If the regular face exists but the bold face does not, set the bold path to the regular face before export:

```powershell
$env:ELBOW_FONT_BOLD = $env:ELBOW_FONT
```

If Times New Roman is unavailable, install a legitimately obtained copy or point these variables to your existing font files. Fonts are not redistributed in the archive.

Outputs are `results/elbow_flexion.mp4`, `elbow_flexion.gif`, `maximum.png`, `return.png`, and `release.png`. The model occupies the left side; English Times New Roman labels on the right report time, flexion, four cable tensions, and the friction coefficient. FFmpeg comes with the Python dependency package.

Video export visualizes the recorded states; it is not a new dynamics experiment. After changing the model, rerun section 8 before exporting to avoid combining a changed model with old data.

## 10. Understand the data and editing points

### Useful CSV fields

| Field | Meaning / units |
|---|---|
| `time_s`, `stage` | Simulation time (s) and motion stage |
| `flexion_deg` | Positive flexion angle for plotting (degrees) |
| `upper_deg`, `lower_deg` | Internal joint coordinates with the model's sign convention |
| `02_ctrl_mm`, `03_ctrl_mm` | Commands for the driven cables, recorded in mm |
| `02_tension_N`, `03_tension_N` | Driven-cable tensions (N) |
| `fixed_right_tension_N`, `fixed_left_tension_N` | Passive-cable tensions (N) |
| `*_length_mm`, `*_free_length_mm` | Routed and free cable lengths (mm) |
| `contact_count`, `contact_normal_force_N` | Contact count and normal-force statistics for the selected structural proxies |
| `max_penetration_mm` | Maximum structural-proxy penetration at that sample (mm) |
| `cable_friction_mu` | Recorded cable friction coefficient; zero in this baseline |

Internal lengths generally use meters, while the indicated CSV fields use millimeters. Positive flexion is the negative sum of the internal angles. Prefer `flexion_deg` for plots; `angle_deg` uses the opposite sign convention.

| Task | File to inspect |
|---|---|
| Motion timing and control | `schedule()` and `Controller` in `run_demo.py` |
| Pulleys, guides, routing, and collision proxies | `model/elbow.xml` |
| A minimal cable MJCF example | `examples/single_pulley.xml` |
| Model and DLL loading | `runtime.py`, `mujocable_plugin.py` |
| Camera and video layout | `render_video.py` |
| Baseline acceptance checks | `verify_results.py` |
| Cylinder-routing modifications | `patches` and `source` |

**Changing geometry can invalidate the existing controller lookup table.** The controller reads an angle–length scan from `model/mobility_route_scan.json`. Changes to pulley position, radius, or cable routing require a new scan and controller calibration. This package does not include a one-click script to regenerate that scan. Reproduce the baseline first; a failure after geometry edits is not automatically a plugin fault.

The recording code also writes `cable_friction_mu` as zero. If you later change physical friction, update parameter logging as well; changing only the figure label or one model setting is insufficient.

## 11. Troubleshooting

| Symptom | Check / action |
|---|---|
| `py` is not recognized | Reopen the terminal; check the standard Python installation and launcher, or use the interpreter's full path |
| `.venv\Scripts\python.exe` is missing | Confirm the project root and successful environment creation |
| PowerShell blocks `Activate.ps1` | Skip activation and use the explicit interpreter paths in this guide |
| `No module named mujoco` | Install with the same `.venv` interpreter used to run the program; check VS Code's selection |
| pip download failure | Check network, proxy, and package index; retry without disabling TLS verification |
| `No matching distribution` | Check Python 3.12 x64 and availability of the pinned wheels on your package index |
| DLL load failure / WinError 126 | Check the three project-local runtime DLLs and plugin; use the supplied diagnostic scripts. If needed, install or repair the x64 runtime through [Microsoft's official page](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170), not an arbitrary DLL download site |
| Unknown `mujoco.cable.unilateral` plugin | Load the plugin before compiling XML; use the supplied loaders |
| WinError 193 | Check binary architecture: x64 Python and Windows DLL; macOS `.dylib` and Linux `.so` files are incompatible |
| Mesh file not found | Preserve `model/assets`; do not copy only the XML |
| Headless run works, viewer fails | Check vendor graphics drivers and desktop OpenGL support; remote desktops and VMs may differ |
| Font missing during export | Set font paths as in section 9 and confirm with `Test-Path` |
| Video shows an old experiment | Regenerate the CSV and check its modification time |
| Model opens but does not follow the motion | Use `run_demo.py`; the generic viewer does not supply this controller |
| Peak is not exactly 180° | The contact-limited baseline peaks near 178.8° |
| F5 cannot find the interpreter | Open the correct project root and create `.venv` |

Run `check_mujoco.py`, then the single-pulley check, then `check_env.py` to isolate engine, plugin, and elbow-model problems. When reporting a problem, include terminal output and `results/environment_check.json`. For verification failures, also include the summary, verification report, and motion CSV.

## 12. Add the plugin to an existing project

This is an alternative for users who already have a MuJoCo environment. It is not an extra step in the main workflow.

1. Download and fully extract the [plugin-only archive](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_plugin_Windows_x64.zip).
2. Use your project's 64-bit Python to install its `requirements.txt`, retaining MuJoCo 3.4.0.
3. Run `example.py` from the plugin-package directory to check the single pulley.
4. Retain the complete plugin-package layout and make its module directory importable in your project. Assuming `mujocable_plugin.py` is on the Python module search path:

```python
from mujocable_plugin import load_plugin
load_plugin()  # Before compiling XML that references this plugin
import mujoco

m = mujoco.MjModel.from_xml_path("your_model.xml")
d = mujoco.MjData(m)
```

Your MJCF must still define plugin instances, endpoints/guides, wrapping geometry, and actuators. Installing a DLL does not automatically route cables. Control units depend on configuration: the single-pulley example uses `target_contraction`, where positive commands shorten the free cable length in meters.

## 13. Quick start with the portable package

Download and extract [MuJoCable_Windows_x64.zip](https://github.com/MuJoCable/mujocable.github.io/releases/download/windows-tutorial-v1/MuJoCable_Windows_x64.zip), then:

1. Double-click `CHECK_ENV.cmd` and check for `passed: true`.
2. Double-click `START_ELBOW.cmd` to see the motion.
3. Use `RUN_HEADLESS.cmd` to record and verify data.
4. Use `EXPORT_VIDEO.cmd` to export video.

This option needs neither VS Code nor a separately installed Python. Its launchers use the bundled `python/python.exe`; the main tutorial uses `.venv`. Running the portable demo does not validate your separately created environment.

You may inspect the portable scripts in VS Code, but its embedded Python is not the starting point for this guide's venv and pip workflow. Use the development project for ongoing model edits and experiments.

## 14. Reproduction checklist

- Base MuJoCo reports version 3.4.0 and passes its dynamics check.
- The elbow environment check reports four cable plugins, two actuators, and `passed: true`.
- The viewer completes flexion, return, and release with low-tension cables turning gray.
- Save `motion.csv`, `summary.json`, `environment.json`, and `verification.json`; the unchanged baseline passes verification.
- Export an MP4 and peak-flexion snapshot; retain the experiment date and version.
- Record any model or script edits. Preserve the unchanged baseline before parameter studies.

## 15. Validation status and model scope

The Windows x64 DLL and Windows Python/MuJoCo binaries have been tested under **Wine 11.0 on macOS**, including a 32-second rollout, the single-pulley example, viewer, and video export. Peak baseline flexion was approximately 178.8146°. Evidence is included in `validation`.

The development project also passed base-engine, single-pulley, elbow-loading, and full-rollout verification checks with an independent Windows interpreter and project-local DLL loading. See `project_guide_checks.json` and `project_rollout_verification.json` in `validation`.

**Native Windows 10/11 installation and GUI acceptance testing remains outstanding.** The standard Python installer, venv creation, pip network installation, and VS Code GUI steps are documented from official sources rather than tested on a native Windows machine. Wine does not establish compatibility with every Windows graphics driver or system policy. The Wine video test logged an OpenGL 0x506 context warning but completed export; a snapshot was inspected.

This demo uses zero gravity and zero cable friction, and accepts route status 1 under the existing model thresholds. Low tension after release does not independently establish mechanical self-locking under load. The demo is also not a maximum-load-versus-angle experiment: that requires explicitly specified gravity, external loads, actuator limits, and acceptance conditions.

Official documentation is linked alongside the relevant steps. Package versions, binary hashes, and patch provenance are recorded in `BUILD_MANIFEST.json` and the included build-provenance files.
