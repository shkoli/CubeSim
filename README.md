# CubeSim — Minimal Package (ready-to-import)

This archive contains a minimal Python package `cubesim` with:
- `cubesim.create_circular_orbit(...)`
- `cubesim.propagate_orbit(...)`
- `cubesim.plot_orbit_2d(...)`
- `cubesim.power_profile(...)`

There's also `app.py` which is a Streamlit demo that uses the package.

## Quick usage (after installing requirements)

```bash
pip install -r requirements.txt
python -c "import cubesim; print(cubesim.create_circular_orbit(500,51))"
# or run the demo:
streamlit run app.py
```

## Notes
- The calculations and eclipse check are simplified for demo and teaching purposes.
- For production / research use, integrate SGP4/sgp4 library and more accurate coordinate transforms.
