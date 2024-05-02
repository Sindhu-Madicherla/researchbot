from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig():
    root_dir: Path
    papers_path: Path
    papers: list
 
@dataclass(frozen=True)   
class VectorIndexConfig():
    root_dir: Path
    embedding_model: str
    cache_dir: Path
    db_name: str
    batch_size: int
