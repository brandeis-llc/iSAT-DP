import re
from typing import List, Tuple
from attrs import define, field


BLOCK_NAME = {"red", "yellow", "green", "blue", "purple", "brown", "mystery"}
PRONOUNS = {
    "it",
    "they",
    "them",
    "this",
    "that",
    "these",
    "those",
}

BLOCK_NAME_PATTERN = rf"\b({'|'.join(BLOCK_NAME)})\b"
PRONOUN_PATTERN = rf"\b({'|'.join(PRONOUNS)})\b"


@define
class ActionComponent:
    verb: str = field(default=None)
    obj: str = field(default=None)
    prep: str = field(default=None)
    loc: str = field(default=None)
    other_text: str = field(default=None)

    @classmethod
    def from_str(cls, action_str: str):
        # annotation errors will break this string parsing method
        parts = action_str.split(" ", 1)
        if len(parts) == 2:
            comp, other = parts
        else:
            comp = parts[0]
            other = None
        comp_lst = [c for c in re.split(r"\(|\)|,", comp.strip()) if c][:4]
        return cls(*comp_lst, other_text=other)


@define
class Action:
    annotation_id: str
    tier_id: str
    start_ts: float
    end_ts: float
    component: ActionComponent


@define
class Utterance:
    id: int
    speaker_id: int
    start: float
    end: float
    text: str  # in lowercase
    actions: List[Action] = field(factory=list)

    @property
    def is_researcher(self) -> bool:
        return self.speaker_id == 4

    @property
    def contain_block_name(self) -> List[Tuple]:
        matches = re.finditer(BLOCK_NAME_PATTERN, self.text)
        return [(m.group(), *m.span()) for m in matches]

    @property
    def contain_pronouns(self) -> List[Tuple]:
        matches = re.finditer(PRONOUN_PATTERN, self.text)
        return [(m.group(), *m.span()) for m in matches]


@define
class Dialogue:
    group_id: int
    utterances: List[Utterance]


if __name__ == "__main__":
    pass
