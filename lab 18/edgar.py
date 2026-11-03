"""Import the same implementation bundled with the skill; do not duplicate math."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('skill_edgar', Path(__file__).parent / 'buffett-edgar/scripts/edgar.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
for name in dir(core):
    if not name.startswith('_'):
        globals()[name] = getattr(core, name)
if __name__ == '__main__':
    core.main()
