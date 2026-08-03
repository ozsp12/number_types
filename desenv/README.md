# Development Notebooks

This folder preserves the four pre-existing notebooks that record the development of the number-category visualization. Their contents have not been rewritten during the class-based refactoring.

| Notebook | Role in the development history |
|---|---|
| `01_first_version.ipynb` | Initial direct implementation and first category animation |
| `02_second_version.ipynb` | Expanded category catalog and reusable generation function |
| `03_third_version.ipynb` | Intermediate transition and rendering experiments |
| `04_fourth_version.ipynb` | Reference implementation used to design the root class |

The production project is located at the repository root:

- `number_types_visualizer.py`: documented class implementation;
- `example_usage.py`: executable example;
- `requirements.yml`: Conda environment;
- `tests/`: mathematical regression tests;
- `README.md`: installation and usage documentation.

The notebooks remain useful as an audit trail and for comparing design decisions. New production changes should be made in the root class. A new notebook should be added here only when it records a distinct exploratory or pedagogical stage.
