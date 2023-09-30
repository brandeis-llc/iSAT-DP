from typing import List

from data import Dialogue, Utterance, Action
from file_path import DATA_FOLDER
from ingest_action import ingest_action_xml
from ingest_dialogue import ingest_dialogue
import pandas as pd

# manually annotated phase1 end utterance (inclusive)
PHASE1_END_UTTERANCE = {
    # group number: utterance_id
    1: 101,
    2: 80,
    3: 88,
    4: 63,
    5: 82,
    6: 74,
    7: 144,
    8: 118,
    9: 41,
    10: 209,
}


def extract_phase1_valid_utterances(dialogue: Dialogue):
    uttrs = []
    pronouns = []

    phase1_end_uttr_id = PHASE1_END_UTTERANCE[dialogue.group_id]

    for uttr in dialogue.utterances:
        if uttr.id > phase1_end_uttr_id:
            break
        block_matches = uttr.contain_block_name
        pronoun_matches = uttr.contain_pronouns
        if not uttr.is_researcher and (block_matches or pronoun_matches):
            uttrs.append(uttr)
            pronouns.append(pronoun_matches)
    return uttrs, pronouns


def overlap_sec(start1, end1, start2, end2):
    if start1 <= end2 and end1 >= start2:
        return min(end1, end2) - max(start1, start2)
    else:
        return 0


def align_action_utterance(actions: List[Action], utterances: List[Utterance]) -> List[Utterance]:
    for action in actions:
        overlapped = -1
        for i, utt in enumerate(utterances):
            new_overlapped = overlap_sec(action.start_ts, action.end_ts, utt.start, utt.end)
            if new_overlapped >= overlapped:
                overlapped = new_overlapped
            else:
                utterances[i - 1].actions.append(action)
                break
            if overlapped > 0 and i == len(utterances) - 1:
                utterances[-1].actions.append(action)

    return utterances


def prepare_pronoun_annotation_csv(group_number: int):
    dialogue = ingest_dialogue(group_number)
    actions = ingest_action_xml(group_number)

    uttrs, pronouns = extract_phase1_valid_utterances(dialogue)
    uttrs = align_action_utterance(actions, uttrs)
    out_rows = []
    for uttr, p_lst in zip(uttrs, pronouns):
        action_str = ", ".join(f"{action.annotation_id}-{action.component.obj}" for action in uttr.actions)
        uttr_chars = list(uttr.text)
        for pronoun, s, e in p_lst:
            uttr_chars[s] = f"[{pronoun[0]}"
            uttr_chars[e - 1] = f"{pronoun[-1]}]"

        annotation_placeholder = " ".join(["[-]"] * len(p_lst))
        out_rows.append(
            [
                uttr.id,
                uttr.speaker_id,
                uttr.start,
                uttr.end,
                "".join(uttr_chars),
                action_str,
                annotation_placeholder,
            ]
        )
    pd.DataFrame(
        out_rows,
        columns="Utterance Participant Start End Transcript Action_Objects Annotation".split(),
    ).to_csv(DATA_FOLDER.joinpath(f"filtered_aligned/Group_{str(group_number).zfill(2)}.csv"), index=False)


if __name__ == "__main__":
    for n in range(1, 11):
        prepare_pronoun_annotation_csv(n)
