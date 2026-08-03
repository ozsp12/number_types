"""Class-based number-category animation derived from 04_fourth_version.ipynb."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import re

import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, FuncAnimation, PillowWriter
from matplotlib.colors import to_rgb
from matplotlib.patches import Rectangle
import numpy as np


@dataclass(frozen=True, slots=True)
class NumberCategory:
    """One finite number class and its display color."""

    title: str
    values: frozenset[int]
    color: str


class NumberTypesVisualizer:
    """Build and render the 34 number classes used in the reference notebook.

    Parameters describe the output canvas and animation timing. Mathematical
    classification is performed once during initialization and stored in
    :attr:`categories`. The default limit is 100 because the visual layout is
    the notebook's fixed 10-by-10 grid.

    Parameters
    ----------
    limit:
        Largest positive integer included. The reference layout requires 100.
    width_pixels, height_pixels:
        Output resolution. Defaults to a vertical 9:16 canvas.
    dpi:
        Matplotlib resolution used to convert pixels into figure dimensions.
    fps:
        Frames per second for MP4 and animation timing.
    hold_seconds, transition_seconds:
        Duration of each static category and each interpolated transition.
    """

    PALETTE = (
        "#e53935", "#ef5350", "#f57c00", "#fb8c00", "#ff9800",
        "#ffb300", "#fbc02d", "#c0ca33", "#7cb342", "#43a047",
        "#00a65a", "#00b86b", "#00a878", "#00a896", "#00acc1",
        "#0097a7", "#039be5", "#1e88e5", "#3949ab", "#5e35b1",
        "#7e57c2", "#8e44ad", "#ab47bc", "#d63384", "#e91e63",
        "#f06292", "#ec407a", "#d81b60", "#c2185b", "#ad1457",
        "#e64a19", "#f4511e", "#ff5722", "#e53935",
    )

    def __init__(
        self,
        *,
        limit: int = 100,
        width_pixels: int = 720,
        height_pixels: int = 1280,
        dpi: int = 100,
        fps: int = 30,
        hold_seconds: float = 0.6,
        transition_seconds: float = 0.6,
    ) -> None:
        if limit != 100:
            raise ValueError("the reference 10-by-10 layout requires limit=100")
        if min(width_pixels, height_pixels, dpi, fps) <= 0:
            raise ValueError("resolution, dpi, and fps must be positive")
        if hold_seconds <= 0 or transition_seconds <= 0:
            raise ValueError("animation durations must be positive")

        self.limit = limit
        self.width_pixels = width_pixels
        self.height_pixels = height_pixels
        self.dpi = dpi
        self.fps = fps
        self.hold_seconds = hold_seconds
        self.transition_seconds = transition_seconds
        self.categories = self._build_categories()

    # ------------------------------------------------------------------
    # Number-theoretic helpers
    # ------------------------------------------------------------------
    @staticmethod
    def is_prime(number: int) -> bool:
        """Return whether ``number`` has exactly two positive divisors."""
        if number < 2:
            return False
        if number % 2 == 0:
            return number == 2
        return all(number % divisor for divisor in range(3, math.isqrt(number) + 1, 2))

    @staticmethod
    def prime_factors(number: int) -> list[int]:
        """Return prime factors with multiplicity in nondecreasing order."""
        if number < 1:
            raise ValueError("number must be positive")
        factors: list[int] = []
        divisor = 2
        while divisor * divisor <= number:
            while number % divisor == 0:
                factors.append(divisor)
                number //= divisor
            divisor += 1 if divisor == 2 else 2
        if number > 1:
            factors.append(number)
        return factors

    @staticmethod
    def digit_sum(number: int) -> int:
        """Return the sum of the decimal digits of a nonnegative integer."""
        return sum(int(digit) for digit in str(number))

    @staticmethod
    def proper_divisor_sum(number: int) -> int:
        """Return the sum of the positive divisors smaller than ``number``."""
        if number == 1:
            return 0
        total = 1
        for divisor in range(2, math.isqrt(number) + 1):
            if number % divisor == 0:
                quotient = number // divisor
                total += divisor
                if quotient != divisor:
                    total += quotient
        return total

    @classmethod
    def is_happy(cls, number: int) -> bool:
        """Return whether repeated squared-digit sums reach one."""
        visited: set[int] = set()
        while number != 1 and number not in visited:
            visited.add(number)
            number = sum(int(digit) ** 2 for digit in str(number))
        return number == 1

    @staticmethod
    def lucky_numbers(limit: int) -> set[int]:
        """Return the classical lucky-number sieve up to ``limit``."""
        values = list(range(1, limit + 1, 2))
        index = 1
        while index < len(values):
            step = values[index]
            if step > len(values):
                break
            values = [value for position, value in enumerate(values, 1) if position % step]
            index += 1
        return set(values)

    @staticmethod
    def is_kaprekar(number: int) -> bool:
        """Return whether ``number`` satisfies the standard decimal split."""
        if number == 1:
            return True
        left, right = divmod(number * number, 10 ** len(str(number)))
        return right > 0 and left + right == number

    @staticmethod
    def _sequence_values(formula, limit: int) -> set[int]:
        """Evaluate an increasing positive sequence formula up to a limit."""
        values: set[int] = set()
        index = 1
        while (value := formula(index)) <= limit:
            values.add(value)
            index += 1
        return values

    @staticmethod
    def _fibonacci_numbers(limit: int) -> set[int]:
        values: set[int] = set()
        first, second = 1, 2
        while first <= limit:
            values.add(first)
            first, second = second, first + second
        return values

    @staticmethod
    def _catalan_numbers(limit: int) -> set[int]:
        values: set[int] = set()
        index, catalan = 0, 1
        while catalan <= limit:
            values.add(catalan)
            catalan = catalan * 2 * (2 * index + 1) // (index + 2)
            index += 1
        return values

    @staticmethod
    def _pell_numbers(limit: int) -> set[int]:
        values: set[int] = set()
        previous, current = 0, 1
        while current <= limit:
            values.add(current)
            previous, current = current, 2 * current + previous
        return values

    def _build_categories(self) -> tuple[NumberCategory, ...]:
        """Construct the same ordered catalog used by the fourth notebook."""
        numbers = set(range(1, self.limit + 1))
        factors = self.prime_factors
        squares = {base**2 for base in range(1, math.isqrt(self.limit) + 1)}
        cubes = {base**3 for base in range(1, self.limit + 1) if base**3 <= self.limit}
        perfect_powers = {
            base**exponent
            for base in range(2, self.limit + 1)
            for exponent in range(2, int(math.log2(self.limit)) + 1)
            if base**exponent <= self.limit
        }
        data = [
            ("Natural Numbers", numbers),
            ("Odd Numbers", {n for n in numbers if n % 2 == 1}),
            ("Even Numbers", {n for n in numbers if n % 2 == 0}),
            ("Multiples of 3", {n for n in numbers if n % 3 == 0}),
            ("Multiples of 5", {n for n in numbers if n % 5 == 0}),
            ("Multiples of 7", {n for n in numbers if n % 7 == 0}),
            ("Multiples of 10", {n for n in numbers if n % 10 == 0}),
            ("Prime Numbers", {n for n in numbers if self.is_prime(n)}),
            ("Composite Numbers", {n for n in numbers if n > 1 and not self.is_prime(n)}),
            ("Semiprime Numbers", {n for n in numbers if n >= 4 and len(factors(n)) == 2}),
            ("Square Numbers", squares),
            ("Cube Numbers", cubes),
            ("Perfect Powers", perfect_powers),
            ("Triangular Numbers", self._sequence_values(lambda n: n * (n + 1) // 2, self.limit)),
            ("Tetrahedral Numbers", self._sequence_values(lambda n: n * (n + 1) * (n + 2) // 6, self.limit)),
            ("Square Pyramidal Numbers", self._sequence_values(lambda n: n * (n + 1) * (2*n + 1) // 6, self.limit)),
            ("Pentagonal Numbers", self._sequence_values(lambda n: n * (3*n - 1) // 2, self.limit)),
            ("Hexagonal Numbers", self._sequence_values(lambda n: n * (2*n - 1), self.limit)),
            ("Perfect Numbers", {n for n in numbers if n > 1 and self.proper_divisor_sum(n) == n}),
            ("Abundant Numbers", {n for n in numbers if self.proper_divisor_sum(n) > n}),
            ("Deficient Numbers", {n for n in numbers if self.proper_divisor_sum(n) < n}),
            ("Fibonacci Numbers", self._fibonacci_numbers(self.limit)),
            ("Decimal Harshad Numbers", {n for n in numbers if n % self.digit_sum(n) == 0}),
            ("Sphenic Numbers", {n for n in numbers if len(factors(n)) == 3 and len(set(factors(n))) == 3}),
            ("Smith Numbers", {n for n in numbers if n >= 4 and not self.is_prime(n) and self.digit_sum(n) == sum(self.digit_sum(f) for f in factors(n))}),
            ("Binary Palindromic Numbers", {n for n in numbers if (binary := bin(n)[2:]) == binary[::-1]}),
            ("Decimal Palindromic Numbers", {n for n in numbers if str(n) == str(n)[::-1]}),
            ("Happy Numbers", {n for n in numbers if self.is_happy(n)}),
            ("Lucky Numbers", self.lucky_numbers(self.limit)),
            ("Evil Numbers", {n for n in numbers if bin(n).count("1") % 2 == 0}),
            ("Automorphic Numbers", {n for n in numbers if str(n*n).endswith(str(n))}),
            ("Kaprekar Numbers", {n for n in numbers if self.is_kaprekar(n)}),
            ("Catalan Numbers", self._catalan_numbers(self.limit)),
            ("Pell Numbers", self._pell_numbers(self.limit)),
        ]
        return tuple(
            NumberCategory(title, frozenset(values), self.PALETTE[index])
            for index, (title, values) in enumerate(data)
        )

    # ------------------------------------------------------------------
    # Geometry and transition matching
    # ------------------------------------------------------------------
    @staticmethod
    def _cell_lower_left(number: int) -> np.ndarray:
        row, column = divmod(number - 1, 10)
        return np.array([float(column), float(9 - row)])

    @staticmethod
    def _ease_in_out(value: float) -> float:
        value = float(np.clip(value, 0.0, 1.0))
        return value * value * (3.0 - 2.0 * value)

    @classmethod
    def _match_positions(cls, old_values: set[int], new_values: set[int]) -> list[tuple[int, int]]:
        """Minimize cell travel using SciPy, with a deterministic fallback."""
        old = sorted(old_values)
        new = sorted(new_values)
        if not old or not new:
            return []
        old_positions = np.array([cls._cell_lower_left(n) for n in old])
        new_positions = np.array([cls._cell_lower_left(n) for n in new])
        costs = np.sum((old_positions[:, None] - new_positions[None, :]) ** 2, axis=2)
        try:
            from scipy.optimize import linear_sum_assignment
            old_indices, new_indices = linear_sum_assignment(costs)
            return [(old[i], new[j]) for i, j in zip(old_indices, new_indices)]
        except ImportError:
            matches: list[tuple[int, int]] = []
            available_old, available_new = set(range(len(old))), set(range(len(new)))
            while available_old and available_new:
                i, j = min(
                    ((i, j) for i in available_old for j in available_new),
                    key=lambda pair: costs[pair],
                )
                matches.append((old[i], new[j]))
                available_old.remove(i)
                available_new.remove(j)
            return matches

    @classmethod
    def _transition_tracks(cls, old_values, new_values) -> list[dict[str, float | int]]:
        old_values, new_values = set(old_values), set(new_values)
        common = old_values & new_values
        tracks = [dict(start=n, end=n, alpha_start=1.0, alpha_end=1.0) for n in sorted(common)]
        old_remaining, new_remaining = old_values - common, new_values - common
        matches = cls._match_positions(old_remaining, new_remaining)
        tracks.extend(dict(start=a, end=b, alpha_start=1.0, alpha_end=1.0) for a, b in matches)
        matched_old, matched_new = {a for a, _ in matches}, {b for _, b in matches}
        tracks.extend(dict(start=n, end=n, alpha_start=1.0, alpha_end=0.0) for n in sorted(old_remaining - matched_old))
        tracks.extend(dict(start=n, end=n, alpha_start=0.0, alpha_end=1.0) for n in sorted(new_remaining - matched_new))
        return tracks

    @staticmethod
    def _slugify(text: str) -> str:
        return re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")

    # ------------------------------------------------------------------
    # Rendering and export
    # ------------------------------------------------------------------
    def create_animation(self) -> tuple[FuncAnimation, plt.Figure, int]:
        """Create the Matplotlib animation without writing files."""
        transitions = [
            self._transition_tracks(current.values, following.values)
            for current, following in zip(self.categories, self.categories[1:])
        ]
        maximum_rectangles = max(
            max(len(category.values) for category in self.categories),
            max(len(transition) for transition in transitions),
        )
        hold_frames = max(1, round(self.hold_seconds * self.fps))
        transition_frames = max(2, round(self.transition_seconds * self.fps))
        segment_frames = hold_frames + transition_frames
        total_frames = (len(self.categories) - 1) * segment_frames + hold_frames

        fig = plt.figure(
            figsize=(self.width_pixels / self.dpi, self.height_pixels / self.dpi),
            dpi=self.dpi,
            facecolor="black",
        )
        axis = fig.add_axes([0.075, 0.105, 0.85, 0.75])
        axis.set(xlim=(0, 10), ylim=(0, 10), aspect="equal")
        axis.set_facecolor("black")
        axis.axis("off")
        old_title = fig.text(0.5, 0.915, "", ha="center", fontsize=34, fontweight="bold", color="white")
        new_title = fig.text(0.5, 0.915, "", ha="center", fontsize=34, fontweight="bold", color="white", alpha=0)

        rectangles = []
        for _ in range(maximum_rectangles):
            rectangle = Rectangle((0, 0), 1, 1, edgecolor="none", alpha=0, zorder=1)
            axis.add_patch(rectangle)
            rectangles.append(rectangle)
        for coordinate in range(11):
            axis.plot([coordinate, coordinate], [0, 10], color="#d8d8d8", linewidth=1.35, zorder=3)
            axis.plot([0, 10], [coordinate, coordinate], color="#d8d8d8", linewidth=1.35, zorder=3)
        number_texts = [
            axis.text(*(self._cell_lower_left(number) + 0.5), str(number), ha="center", va="center",
                      fontsize=15, fontweight="bold", color="white", zorder=4)
            for number in range(1, 101)
        ]

        def hide_rectangles() -> None:
            for rectangle in rectangles:
                rectangle.set_visible(False)
                rectangle.set_alpha(0)

        def render_static(index: int) -> None:
            hide_rectangles()
            category = self.categories[index]
            old_title.set_text(category.title)
            old_title.set_color(category.color)
            old_title.set_alpha(1)
            new_title.set_alpha(0)
            for rectangle, number in zip(rectangles, sorted(category.values)):
                rectangle.set_xy(self._cell_lower_left(number))
                rectangle.set_facecolor(category.color)
                rectangle.set_alpha(1)
                rectangle.set_visible(True)

        def render_transition(index: int, interpolation: float) -> None:
            hide_rectangles()
            eased = self._ease_in_out(interpolation)
            old_category, new_category = self.categories[index:index + 2]
            old_title.set_text(old_category.title)
            old_title.set_color(old_category.color)
            old_title.set_alpha(1 - eased)
            new_title.set_text(new_category.title)
            new_title.set_color(new_category.color)
            new_title.set_alpha(eased)
            color = (1 - eased) * np.array(to_rgb(old_category.color)) + eased * np.array(to_rgb(new_category.color))
            for rectangle, track in zip(rectangles, transitions[index]):
                start = self._cell_lower_left(int(track["start"]))
                end = self._cell_lower_left(int(track["end"]))
                alpha = (1 - eased) * float(track["alpha_start"]) + eased * float(track["alpha_end"])
                rectangle.set_xy((1 - eased) * start + eased * end)
                rectangle.set_facecolor(color)
                rectangle.set_alpha(alpha)
                rectangle.set_visible(alpha > 0.001)

        def update(frame: int):
            final_start = (len(self.categories) - 1) * segment_frames
            if frame >= final_start:
                render_static(len(self.categories) - 1)
            else:
                index, local_frame = divmod(frame, segment_frames)
                if local_frame < hold_frames:
                    render_static(index)
                else:
                    render_transition(index, (local_frame - hold_frames) / (transition_frames - 1))
            return [old_title, new_title, *rectangles, *number_texts]

        animation = FuncAnimation(fig, update, frames=total_frames, interval=1000 / self.fps, blit=False)
        return animation, fig, total_frames

    def save_preview(self, category_name: str, destination: str | Path) -> Path:
        """Save one static category grid as a PNG image."""
        lookup = {category.title.casefold(): category for category in self.categories}
        key = category_name.strip().casefold()
        if key not in lookup:
            raise ValueError(f"unknown category: {category_name}")
        category = lookup[key]
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        fig, axis = plt.subplots(figsize=(7.2, 7.2), dpi=self.dpi, facecolor="black")
        axis.set(xlim=(0, 10), ylim=(0, 10), aspect="equal")
        axis.set_facecolor("black")
        axis.axis("off")
        for number in range(1, 101):
            position = self._cell_lower_left(number)
            if number in category.values:
                axis.add_patch(Rectangle(position, 1, 1, facecolor=category.color, edgecolor="none"))
            axis.text(*(position + 0.5), str(number), ha="center", va="center", color="white", fontweight="bold")
        for coordinate in range(11):
            axis.plot([coordinate, coordinate], [0, 10], color="#d8d8d8", linewidth=1)
            axis.plot([0, 10], [coordinate, coordinate], color="#d8d8d8", linewidth=1)
        fig.suptitle(category.title, color=category.color, fontsize=22, fontweight="bold")
        fig.savefig(destination, facecolor="black", bbox_inches="tight")
        plt.close(fig)
        return destination

    def render(
        self,
        output_dir: str | Path = "output",
        *,
        save_mp4: bool = True,
        save_gif: bool = False,
        save_previews: bool = False,
    ) -> dict[str, object]:
        """Render selected outputs and return paths plus animation metadata."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        generated: dict[str, object] = {}

        if save_previews:
            preview_dir = output_dir / "previews"
            generated["previews"] = [
                str(self.save_preview(category.title, preview_dir / f"{index:02d}_{self._slugify(category.title)}.png"))
                for index, category in enumerate(self.categories, 1)
            ]

        if save_mp4 or save_gif:
            animation, figure, total_frames = self.create_animation()
            if save_mp4:
                mp4_path = output_dir / "number_categories.mp4"
                animation.save(mp4_path, writer=FFMpegWriter(fps=self.fps, bitrate=6000, codec="libx264",
                                                               extra_args=["-pix_fmt", "yuv420p"]), dpi=self.dpi)
                generated["mp4"] = str(mp4_path)
            if save_gif:
                gif_path = output_dir / "number_categories.gif"
                animation.save(gif_path, writer=PillowWriter(fps=min(self.fps, 15)), dpi=self.dpi)
                generated["gif"] = str(gif_path)
            plt.close(figure)
        else:
            total_frames = (len(self.categories) - 1) * (
                max(1, round(self.hold_seconds * self.fps))
                + max(2, round(self.transition_seconds * self.fps))
            ) + max(1, round(self.hold_seconds * self.fps))

        return {
            "generated_files": generated,
            "number_of_categories": len(self.categories),
            "frames": total_frames,
            "duration_seconds": total_frames / self.fps,
            "resolution": (self.width_pixels, self.height_pixels),
        }
