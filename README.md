# Eloqium — Webcam Gaze-Tracking Prototype

A Python/OpenCV prototype that estimates gaze direction and blinking from webcam frames. It includes a gaze-tracking package, an annotated demo, and an alternate script that reports the proportion of captured frames classified as looking toward the center.

## Capabilities

- Detects a face and locates eye landmarks using dlib.
- Calibrates pupil detection and estimates pupil coordinates.
- Reports left, right, center, and blinking states.
- Draws pupil markers and text on webcam frames.
- Calculates a simple center-looking frame ratio on exit.

The ratio is an experimental image-based metric. It does not independently measure attention, engagement, or verified eye contact.

## Files

| Path | Responsibility |
| --- | --- |
| `example.py` | Annotated demo on camera index 0 |
| `gaze_tracking.py` | Alternate demo on camera index 1 and frame-ratio summary |
| `gaze_tracking/gaze_tracking.py` | Main GazeTracking interface |
| `gaze_tracking/eye.py`, `pupil.py` | Eye-region/pupil processing |
| `gaze_tracking/calibration.py` | Calibration support |
| `gaze_tracking/trained_models/` | Required facial-landmark predictor |
| `requirements.txt` | Pinned pip dependencies |
| `environment.yml` | Older, different conda environment |
| `Dockerfile` | Legacy Ubuntu-based dependency image |

## Setup

Use Python with a desktop GUI, a webcam, and a working C++ build environment if dlib must compile. Requirements pin dlib 19.24.4, NumPy 1.26.4, OpenCV 4.10.0.82, and setuptools 70.0.0.

```bash
git clone https://github.com/AbdelilahNossair/Eloqium.git
cd Eloqium
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python example.py
```

Allow camera access when the operating system requests it. Press **Escape** to stop and release the camera. If dlib installation fails, inspect compiler/CMake availability and Python/platform compatibility.

The conda file pins much older dependencies than requirements.txt; treat it as a historical alternative, not an equivalent reproducible environment.

## Alternative eye-contact demo

```bash
python gaze_tracking.py
```

This script uses `cv2.VideoCapture(1)`. If your system exposes only one camera, change it to index 0 in a local copy. It increments the denominator for every successfully captured frame, and the numerator when `is_center()` is true, then prints the percentage on exit. Frames without a detected face still contribute to the denominator.

## Library usage

```python
from gaze_tracking import GazeTracking

gaze = GazeTracking()
# frame is a valid BGR OpenCV image
# gaze.refresh(frame)
# print(gaze.pupil_left_coords(), gaze.pupil_right_coords())
# print(gaze.is_left(), gaze.is_center(), gaze.is_right())
```

Call `refresh(frame)` before reading results. Coordinates and ratios may be unavailable when pupils cannot be located. Horizontal classification uses thresholds around 0.35 and 0.65; blink detection uses an eye-ratio threshold.

## Troubleshooting and limitations

Lighting, glasses, head pose, camera quality, and calibration affect output. The basic example does not robustly recover from failed frame capture. A GUI display is required for OpenCV windows; headless Docker execution alone will not provide camera/display access.

The Dockerfile uses Ubuntu 18.04 and does not configure webcam or display forwarding. The landmark model is duplicated at the repository root and inside the package; the package loads the latter. No automated validation suite or measured accuracy benchmark is included.

## Attribution and license

The package identifies itself as GazeTracking in its source/environment. Preserve the notices in [LICENSE](LICENSE) and any upstream attribution when modifying or redistributing it. The bundled landmark data may have separate provenance and usage terms; review those before redistribution.
