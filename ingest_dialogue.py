import os
import re
from typing import Union, List
from pathlib import Path
import pandas as pd
from attrs import define

DATA_FOLDER = Path("data")
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
class Utterance:
    id: int
    speaker_id: int
    start: float
    end: float
    text: str  # in lowercase

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


def read_transcript_csv(csv_file: Union[str, os.PathLike]):
    csv_df = pd.read_csv(csv_file, header=0)
    return csv_df


def ingest_dialogue(group_id: int) -> Dialogue:
    csv_file = DATA_FOLDER.joinpath(f"Group_0{group_id}_Oracle.csv")
    csv_df = read_transcript_csv(csv_file)
    utterances = []
    for _, row in csv_df.iterrows():
        utt = Utterance(row.Utterance, row.Participant, row.Start, row.End, row.Transcript.strip().lower())
        utterances.append(utt)
    dialogue = Dialogue(group_id, utterances)
    return dialogue


if __name__ == '__main__':
    ingest_dialogue(1)
