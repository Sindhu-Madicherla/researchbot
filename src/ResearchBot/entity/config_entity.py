from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LoadDataConfig():
    root_dir: Path
    source_dir: Path