from pathlib import Path
import shutil
from typing import Optional, Tuple
from pydantic import BaseModel, PrivateAttr


class OcrStatsConfig(BaseModel):
    """Handles optional OCR statistics output."""
    _folder_path: Optional[Path] = PrivateAttr(None)
    _is_enabled: bool = PrivateAttr(False)

    first_color: Tuple[int, int, int] = (0, 0, 255)
    second_color: Tuple[int, int, int] = (0, 255, 0)
    histograms_color: Tuple[int, int, int] = (100, 100, 100)
    overlay_opacity: float = 0.25
    padding: int = 0
    lines_thickness: int = 2
    text_denoise_indicators_width: int = 20

    model_config = {"json_encoders": {Path: lambda p: str(p)}}

    @property
    def is_enabled(self) -> bool:
        return bool(self._is_enabled)

    def enable(self, folder_path: str):
        self._is_enabled = True
        p = Path(folder_path)
        self._folder_path = p
        if p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True, exist_ok=True)

    def disable(self):
        self._is_enabled = False

    @property
    def folder_path(self) -> Optional[Path]:
        return self._folder_path

    def to_json(self, **kwargs) -> str:
        """Return JSON string."""
        return self.model_dump_json(**kwargs)

    def to_json_file(self, file_path: str, **kwargs) -> None:
        Path(file_path).write_text(self.to_json(**kwargs), encoding="utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "OcrStatsConfig":
        """Load from JSON string."""
        return cls.model_validate_json(json_str)

    @classmethod
    def from_json_file(cls, file_path: str) -> "OcrStatsConfig":
        """Load from JSON file."""
        json_str = Path(file_path).read_text(encoding="utf-8")
        return cls.model_validate_json(json_str)
