from pydantic import BaseModel
from pathlib import Path


class PreprocessingConfig(BaseModel):
    blur_kernel: int = 0
    invert_colors: bool = False
    otsu_threshold_1: int = 0
    otsu_threshold_2: int = 255


class AlignmentConfig(BaseModel):
    fix_rotation: bool = True
    hough_max_threshold: int = 500
    hough_min_lines: int = 10
    hough_max_lines: int = 30
    hough_angle_range: float = 0.5
    hough_angle_step: int = 1


class TextAreasConfig(BaseModel):
    cell_size_multiplier: int = 2
    canny_threshold_1: float = 255 / 3
    canny_threshold_2: float = 255
    text_assumption_threshold_1: float = 0.2
    text_assumption_threshold_2: float = 0.6
    text_assumption_min_occurrences: int = 2
    text_areas_deviation: float = 1.0
    text_area_padding: float = 0.5


class DenoisingConfig(BaseModel):
    text_denoising_threshold: float = 0.08


class LinesConfig(BaseModel):
    lines_hist_window: float = 0.25
    lines_hist_frequency: float = 1.6


class WordsConfig(BaseModel):
    space_threshold: float = 0.15
    paragraph_spaces: int = 4


class OcrConfig(BaseModel):
    preprocessing: PreprocessingConfig = PreprocessingConfig()
    alignment: AlignmentConfig = AlignmentConfig()
    text_areas: TextAreasConfig = TextAreasConfig()
    denoising: DenoisingConfig = DenoisingConfig()
    lines: LinesConfig = LinesConfig()
    words: WordsConfig = WordsConfig()

    model_config = {
        "populate_by_name": True,
        "json_encoders": {Path: lambda p: str(p)},
    }

    def to_json(self, **kwargs) -> str:
        """Return JSON string."""
        return self.model_dump_json(**kwargs)

    def to_json_file(self, file_path: str, **kwargs) -> None:
        Path(file_path).write_text(self.to_json(**kwargs), encoding="utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "OcrConfig":
        """Load from JSON string."""
        return cls.model_validate_json(json_str)

    @classmethod
    def from_json_file(cls, file_path: str) -> "OcrConfig":
        """Load from JSON file."""
        json_str = Path(file_path).read_text(encoding="utf-8")
        return cls.model_validate_json(json_str)
