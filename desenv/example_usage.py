"""Minimal executable example for NumberTypesVisualizer."""

from number_types_visualizer import NumberTypesVisualizer


visualizer = NumberTypesVisualizer(
    width_pixels=720,
    height_pixels=1280,
    fps=30,
    hold_seconds=0.6,
    transition_seconds=0.6,
)

# Create one inexpensive static image first.
visualizer.save_preview("Prime Numbers", "output/example_prime_numbers.png")

# Enable MP4 or GIF only when the corresponding output is required.
result = visualizer.render(
    output_dir="output",
    save_mp4=False,
    save_gif=False,
    save_previews=False,
)

print(result)
