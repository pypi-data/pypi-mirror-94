from pathlib import Path

TESTS_PATH = Path(__file__).parent
GENERATED_FILES_DIR = TESTS_PATH / 'generated_files'
INPUT_FILES_DIR = TESTS_PATH / 'input_files'

for path in [GENERATED_FILES_DIR, INPUT_FILES_DIR]:
    if not path.exists():
        path.mkdir()