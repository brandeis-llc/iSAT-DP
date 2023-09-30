import os
from typing import List, Tuple, Union

from file_path import DATA_FOLDER
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


def load_annotation_csv(csv_file_path: Union[os.PathLike, str]):
    csv_df = pd.read_csv(csv_file_path)
    csv_df.fillna("", inplace=True)
    annotations = csv_df.Annotation.values.tolist()
    return annotations


def parse_block_annotation(annotation_str: str):
    comps = annotation_str.split()
    comps = [[BLOCK_ANNOTATION_MAPPING[l] for l in c[1:-1]] for c in comps]
    return comps


def replace_pronouns(
    uttr_txt: str, annotation_str: str, pronoun_lst: List[Tuple[str, int, int]]
) -> List[str]:
    block_names = parse_block_annotation(annotation_str)
    comps = []
    global_s = 0
    for i, (pronoun, s, e) in enumerate(pronoun_lst):
        comps.append(uttr_txt[global_s:s])
        block_name_str = ", ".join(block_names[i])
        if block_name_str:
            comps.append(block_name_str)
        else:
            comps.append(pronoun)

        global_s = e
    if global_s:
        comps.append(uttr_txt[global_s:])
    return comps


def paraphrase(csv_file_path: Union[os.PathLike, str], group_number: int) -> List[str]:
    dialogue = ingest_dialogue(group_number)

    uttrs, pronouns = extract_phase1_valid_utterances(dialogue)
    annotations = load_annotation_csv(csv_file_path)
    dp_text_lst = []

    assert len(uttrs) == len(annotations)

    for uttr, ann_str, p_lst in zip(uttrs, annotations, pronouns):
        if p_lst:
            comps = replace_pronouns(uttr.text, ann_str, p_lst)
            dp_text = "".join(comps).strip()
        else:
            dp_text = uttr.text
        dp_text_lst.append(dp_text)
    return dp_text_lst


def dump_annotation2csv(in_file_path, group_number, out_file_path):
    csv_df = pd.read_csv(in_file_path)
    dp_text_lst = paraphrase(in_file_path, group_number)
    csv_df["DPed"] = dp_text_lst
    csv_df.to_csv(out_file_path)


if __name__ == "__main__":
    for ann_i in [1, 2]:
        for group_i in range(1, 11):
            if ann_i == 1:
                in_csv_file_path = DATA_FOLDER.joinpath(
                    f"annotated_a{ann_i}/Group_{str(group_i).zfill(2)}_DP_AG.csv"
                )
                out_csv_file_path = DATA_FOLDER.joinpath(
                    f"dped_a{ann_i}/Group_{str(group_i).zfill(2)}_DPed_AG.csv"
                )

            else:
                in_csv_file_path = DATA_FOLDER.joinpath(
                    f"annotated_a{ann_i}/Group_{str(group_i).zfill(2)}_DP_CM.csv"
                )
                out_csv_file_path = DATA_FOLDER.joinpath(
                    f"dped_a{ann_i}/Group_{str(group_i).zfill(2)}_DPed_CM.csv"
                )

            dump_annotation2csv(in_csv_file_path, group_i, out_csv_file_path)
