# ActivitySim Utility Scripts

All scripts in this repository can be run using Marimo.

The recommended way to run these scripts is to first install uv, then install `marimo` as a tool using uv.

```sh
# Install Marimo using UV
uv tool install marimo

# Running locally
uvx marimo edit convert_spec.py
uvx marimo run convert_spec.py # read-only mode

# Running inside Docker
uvx marimo edit https://github.com/asiripanich/activitysim-util-scripts/blob/main/convert_spec.py
uvx marimo run https://github.com/asiripanich/activitysim-util-scripts/blob/main/convert_spec.py # read-only mode
```
