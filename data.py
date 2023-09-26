import re
from typing import List
from attrs import define, field

BLOCK_NAME = {"red", "yellow", "green", "blue", "purple", "brown", "mystery"}
PRONOUNS = {
    "it",
    # "its",
    "they",
    "them",
    # "their",
    "this",
    "that",
    "these",
    "those",
}

BLOCK_NAME_PATTERN = rf"\b({'|'.join(BLOCK_NAME)})\b"
PRONOUN_PATTERN = rf"\b({'|'.join(PRONOUNS)})\b"


@define
class ActionComponent:
    verb: str
    obj: str
    prep: str = field(default=None)
    loc: str = field(default=None)
    other_text: str = field(default=None)

    @classmethod
    def from_str(cls, action_str: str):
        parts = action_str.split("-", 1)
        if len(parts) == 2:
            comp, other = parts
        else:
            comp = parts[0]
            other = None
        comp_lst = [c for c in re.split(r"\(|\)|,", comp.strip()) if c]
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
    def contain_block_name(self) -> List[str]:
        return re.findall(BLOCK_NAME_PATTERN, self.text)

    @property
    def contain_pronouns(self) -> List[str]:
        return re.findall(PRONOUN_PATTERN, self.text)


@define
class Dialogue:
    group_id: int
    utterances: List[Utterance]


if __name__ == "__main__":
    pass
