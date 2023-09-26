import os
from typing import Union
import pandas as pd
from data import Utterance, Dialogue, DATA_FOLDER

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


def read_transcript_csv(csv_file: Union[str, os.PathLike]):
    csv_df = pd.read_csv(csv_file, header=0)
    return csv_df


def ingest_dialogue(group_id: int) -> Dialogue:
    csv_file = DATA_FOLDER.joinpath(f"Group_{str(group_id).zfill(2)}_Oracle.csv")
    csv_df = read_transcript_csv(csv_file)
    utterances = []
    for _, row in csv_df.iterrows():
        utt = Utterance(
            row.Utterance,
            row.Participant,
            row.Start,
            row.End,
            row.Transcript.strip().lower(),
        )
        utterances.append(utt)
    dialogue = Dialogue(group_id, utterances)
    return dialogue


if __name__ == "__main__":
    dialogue = ingest_dialogue(1)
