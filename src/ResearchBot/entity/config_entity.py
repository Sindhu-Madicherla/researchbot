from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)

class DataIngestionConfig():
    root_dir: Path
    papers: str
