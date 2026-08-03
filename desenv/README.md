# Class-Based Development Version

This folder contains the class-based project derived from `04_fourth_version.ipynb`. The original notebook remains unchanged at the repository root and is also copied here as the implementation reference.

## Files

| File | Purpose |
|---|---|
| `04_fourth_version.ipynb` | Unmodified source notebook used for the refactoring |
| `number_types_visualizer.py` | Documented `NumberTypesVisualizer` class |
| `example_usage.py` | Minimal executable usage example |
| `requirements.yml` | Reproducible Conda environment |
| `tests/` | Mathematical regression tests |

## Setup

```bash
conda env create -f desenv/requirements.yml
conda activate number-types-desenv
```

## Example

From the repository root:

```bash
python desenv/example_usage.py
```

The example creates a static prime-number preview and returns animation metadata without rendering a long video. To export media, change the corresponding flags:

```python
from desenv import NumberTypesVisualizer

visualizer = NumberTypesVisualizer(fps=30)
result = visualizer.render(
    output_dir="output",
    save_mp4=True,
    save_gif=False,
    save_previews=True,
)
print(result)
```

MP4 export requires FFmpeg. GIF export uses Pillow. SciPy is used for minimum-cost matching between cells; the class retains a deterministic fallback when SciPy is unavailable.

## Tests

```bash
python -m unittest discover -s desenv/tests -v
```
