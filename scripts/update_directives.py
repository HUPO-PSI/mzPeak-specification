import re
from pathlib import Path

MUST_PATTERN = re.compile(r"\*\*MUST\*\*")
SHOULD_PATTERN = re.compile(r"\*\*SHOULD\*\*")
MAY_PATTERN = re.compile(r"\*\*MAY\*\*")

MUST_CHIP = """[MUST]{class="must-chip"}"""
SHOULD_CHIP = """[SHOULD]{class="should-chip"}"""
MAY_CHIP = """[MAY]{class="may-chip"}"""

for root, _, files in Path("./docs/").walk():
    for f in files:
        if f.endswith('.md'):
            source = text = (root / f).read_text()
            text = MUST_PATTERN.sub(MUST_CHIP, text)
            text = SHOULD_PATTERN.sub(SHOULD_CHIP, text)
            text = MAY_PATTERN.sub(MAY_CHIP, text)
            if source != text:
                print("Updating", root / f)
                (root / f).write_text(text)
