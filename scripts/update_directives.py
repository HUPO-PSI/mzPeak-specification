import re
from itertools import chain
from pathlib import Path

MUST_PATTERN = re.compile(r"\*+MUST\*+")
MUST_NOT_PATTERN = re.compile(r"\*+MUST NOT\*+|(?:\*+MUST\*+ not)")
SHOULD_PATTERN = re.compile(r"\*+SHOULD\*+")
SHOULD_NOT_PATTERN = re.compile(r"\*+SHOULD NOT\*+|(?:\*+SHOULD\*+ not)")
MAY_PATTERN = re.compile(r"\*+MAY\*+")
NOT_PATTERN = re.compile(r"\*+NOT\*+")

MUST_CHIP = """[MUST]{class="must-chip"}"""
MUST_NOT_CHIP = """[MUST NOT]{class="must-not-chip"}"""
SHOULD_CHIP = """[SHOULD]{class="should-chip"}"""
SHOULD_NOT_CHIP = """[SHOULD NOT]{class="should-chip"}"""
MAY_CHIP = """[MAY]{class="may-chip"}"""
NOT_CHIP = """[NOT]{class="not-chip"}"""

for root, _, files in chain(Path("./docs/").walk(), Path("schema/meta").walk()):
    for f in files:
        if f.endswith('.md'):
            source = text = (root / f).read_text()
            text = MUST_PATTERN.sub(MUST_CHIP, text)
            text = SHOULD_PATTERN.sub(SHOULD_CHIP, text)
            text = MAY_PATTERN.sub(MAY_CHIP, text)
            text = MUST_NOT_PATTERN.sub(MUST_NOT_CHIP, text)
            text = SHOULD_NOT_PATTERN.sub(SHOULD_NOT_CHIP, text)
            text = NOT_PATTERN.sub(NOT_CHIP, text)
            if source != text:
                print("Updating", root / f)
                (root / f).write_text(text)
