# Cable Dynamics Plugin for MuJoCo

This repository hosts the static academic project page for the Cable Dynamics
Plugin for MuJoCo.

Project page: <https://mujocable.github.io/>

## Technical documentation

Manual: <https://mujocable.github.io/docs/>

The Sphinx/Furo manual is built from `docs/site` in the
[plugin repository](https://github.com/MuJoCable/mujoco-cable-dynamics).
Build it there with `python docs/site/build.py`, then copy the generated
`docs/site/_build/html/` into this repository's `docs/` directory, preserving
the existing `docs/windows/` tutorial sources. Do not edit generated HTML.

The manual includes installation, MJCF modeling, actuation, routing, friction,
interfaces, sensor reference, validation and downloadable model/video/data
resources. Homepage access is added by `assets/documentation-links.js` without
modifying the compiled React bundle.

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
