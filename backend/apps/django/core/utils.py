from pathlib import Path

__all__ = [
    "remove_empty_folders"
]


def remove_empty_folders(path: Path):
    elements = set(path.iterdir())
    folders = {
        element
        for element in elements
        if element.is_dir()
    }
    for folder in folders:
        if remove_empty_folders(folder):
            folder.rmdir()
    
    remaining_folders_exists = [element.is_dir() for element in path.iterdir()]
    files_exists = any(element.is_file() for element in elements)
    
    return not files_exists and not remaining_folders_exists
