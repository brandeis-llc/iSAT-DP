from typing import List

from data import Dialogue, Utterance, Action, DATA_FOLDER
from ingest_action import ingest_action_xml
from ingest_dialogue import ingest_dialogue
import pandas as pd


def extract_valid_utterances(dialogue: Dialogue):
    uttrs = []
    keywords = []

    for uttr in dialogue.utterances:
        if not uttr.is_researcher and (
            uttr.contain_block_name or uttr.contain_pronouns
        ):
            uttrs.append(uttr)
            keywords.append(uttr.contain_block_name + uttr.contain_pronouns)
    return uttrs, keywords


def overlap_sec(start1, end1, start2, end2):
    if start1 <= end2 and end1 >= start2:
        return min(end1, end2) - max(start1, start2)
    else:
        return 0


def align_action_utterance(
    actions: List[Action], utterances: List[Utterance]
) -> List[Utterance]:
    for action in actions:
        overlapped = -1
        for i, utt in enumerate(utterances):
            new_overlapped = overlap_sec(
                action.start_ts, action.end_ts, utt.start, utt.end
            )
            if new_overlapped >= overlapped:
                overlapped = new_overlapped
            else:
                utterances[i - 1].actions.append(action)
                break
            if overlapped > 0 and i == len(utterances) - 1:
                utterances[-1].actions.append(action)

    return utterances


if __name__ == "__main__":
    for n in range(1, 11):
        dialogue = ingest_dialogue(n)
        actions = ingest_action_xml(n)

        uttrs, keywords = extract_valid_utterances(dialogue)
        uttrs = align_action_utterance(actions, uttrs)

        out_rows = []
        for u, k in zip(uttrs, keywords):
            action_str = ", ".join(
                f"{action.annotation_id}-{action.component.obj}" for action in u.actions
            )
            out_rows.append(
                [u.speaker_id, u.start, u.end, u.text, ", ".join(k), action_str]
            )
        pd.DataFrame(
            out_rows,
            columns="Participant Start End Transcript keywords Action_Objects".split(),
        ).to_csv(DATA_FOLDER.joinpath(f"filtered_aligned/Group_0{n}.csv"), index=False)
