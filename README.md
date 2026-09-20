# Cable Dynamics Plugin for MuJoCo

This repository hosts the static academic project page for the Cable Dynamics
Plugin for MuJoCo.

Project page: <https://mujocable.github.io/>

## Windows tutorial

- English (default): <https://mujocable.github.io/tutorials/windows/>
- 中文: <https://mujocable.github.io/tutorials/windows/zh.html>

Edit `docs/windows/en.md` and `docs/windows/zh.md`, then rebuild:

```sh
python -m pip install -r requirements-docs.txt
python tools/build_windows_tutorial.py
python tools/check_windows_tutorial.py
```

The pages are static HTML, with matching section anchors and language links.
Downloads are attached to the `windows-tutorial-v1` release of this repository.
The reference video is served from `tutorials/windows/media`.

The homepage is supplied as a compiled React bundle. Its tutorial links are added
by the small `assets/windows-tutorial-links.js` module; the generated bundle is
unchanged. When the homepage source is rebuilt elsewhere, retain that module or
move its English/Chinese links into the source navigation and resource buttons.
