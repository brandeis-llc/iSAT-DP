from typing import List, Tuple

from data import Dialogue, Utterance, Action, DATA_FOLDER
from ingest_dialogue import ingest_dialogue
from preprocess import extract_phase1_valid_utterances
import pandas as pd

BLOCK_ANNOTATION_MAPPING = {
    "r": "red block",
    "y": "yellow block",
    "g": "green block",
    "p": "purple block",
    "b": "blue block",
    "m": "mystery block",
    "-": "",
}


def load_annotation_csv(ann_number, group_number):
    if ann_number == 1:
        csv_file_path = DATA_FOLDER.joinpath(f"annotated_a{ann_number}/Group_{str(group_number).zfill(2)}_DP_AG.csv")
    else:
        csv_file_path = DATA_FOLDER.joinpath(f"annotated_a{ann_number}/Group_{str(group_number).zfill(2)}_DP_CM.csv")
    csv_df = pd.read_csv(csv_file_path)
    csv_df.fillna("", inplace=True)
    annotations = csv_df.Annotation.values.tolist()
    return annotations


def parse_block_annotation(annotation_str: str):
    comps = annotation_str.split()
    comps = [[BLOCK_ANNOTATION_MAPPING[l] for l in c[1: -1]] for c in comps]
    return comps


def replace_pronouns(uttr_txt: str, annotation_str: str, pronoun_lst: List[Tuple[str, int, int]]):
    block_names = parse_block_annotation(annotation_str)
    comps = []
    global_s = 0
    for i, (pronoun, s, e) in enumerate(pronoun_lst):
        comps.append(uttr_txt[global_s: s])
        block_name_str = ", ".join(block_names[i])
        if block_name_str:
            comps.append(block_name_str)
        else:
            comps.append(pronoun)

        global_s = e
    if global_s:
        comps.append(uttr_txt[global_s:])
    return comps


def paraphrase(ann_number, group_number):
    dialogue = ingest_dialogue(group_number)

    uttrs, pronouns = extract_phase1_valid_utterances(dialogue)
    annotations = load_annotation_csv(ann_number, group_number)

    assert len(uttrs) == len(annotations)

    for uttr, ann_str, p_lst in zip(uttrs, annotations, pronouns):
        print(ann_number, group_number)
        print(uttr)
        print(p_lst)
        print(ann_str)
        if p_lst:
            comps = replace_pronouns(uttr.text, ann_str, p_lst)
            print("".join(comps).strip())
        else:
            print(uttr.text)
        print("====" * 10)


if __name__ == '__main__':
    for ann_i in [1, 2]:
        for group_i in range(1, 11):
            paraphrase(ann_i, group_i)
