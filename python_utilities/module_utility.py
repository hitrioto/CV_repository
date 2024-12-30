import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def import_from_path(path_to_file) -> ModuleType:
    spec = importlib.util.spec_from_file_location(Path(path_to_file).stem, path_to_file)

    # Check if the spec was successfully created
    if spec is None or spec.loader is None:
        msg = f"Could not load module spec for {path_to_file}"
        raise ImportError(msg)

    # Now using ModuleType for the type hint of the module variable
    module: ModuleType = importlib.util.module_from_spec(spec)

    # The loader is checked above, so this should be safe now
    spec.loader.exec_module(module)

    return module


def find_project_root():
    # Logic to find the project root (e.g., looking for pyproject.toml)
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    msg = "Project root not found."
    raise FileNotFoundError(msg)


def get_dynamic_import_path(relative_path):
    """Construct a full path for dynamic imports, adjusting based on the current working directory.

    :param relative_path: Path relative to the project root or the script's directory.
    :return: Adjusted full path as a string.
    """
    project_root = find_project_root()
    full_path = project_root / relative_path

    # If not running from the project root, adjust the path as needed
    if Path.cwd() != project_root:
        # Example adjustment, customize based on your logic
        full_path = Path(__file__).parent / relative_path

    # Ensure the path is absolute and return it as a string
    return str(full_path.resolve())


if __name__ == "__main__":
    # Usage in your script
    dynamic_imported_file = get_dynamic_import_path("folder/some_file.py")

    # Example of dynamically importing based on the calculated path
    if dynamic_imported_file not in sys.path:
        sys.path.append(dynamic_imported_file)  # Adjust the sys.path temporarily

    # Proceed with dynamic import logic
