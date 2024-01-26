import pandas as pd

from dense_paraphrase import load_annotation_csv
from file_path import DATA_FOLDER
from sklearn.metrics import cohen_kappa_score, f1_score


def process_annotation(annotation_str: str):
    comps = annotation_str.split()
    comps = ["".join(sorted(c[1:-1])) for c in comps]
    return comps


def get_iaa(data_type: str):
    iaa_dict = dict()
    all_anns1 = []
    all_anns2 = []
    for group_i in range(1, 11):
        if data_type == "oracle":
            a1_file_path = DATA_FOLDER.joinpath(f"annotated_a1/Group_{str(group_i).zfill(2)}_DP_AG.csv")
            a2_file_path = DATA_FOLDER.joinpath(f"annotated_a2/Group_{str(group_i).zfill(2)}_DP_CM.csv")
        elif data_type == "google":
            a1_file_path = DATA_FOLDER.joinpath(f"google_annotated_a1/Group_{str(group_i).zfill(2)}_G_AG.csv")
            a2_file_path = DATA_FOLDER.joinpath(f"google_annotated_a2/Group_{str(group_i).zfill(2)}_G_CM.csv")
        elif data_type == "whisper":
            a1_file_path = DATA_FOLDER.joinpath(f"whisper_annotated_a1/Group_{str(group_i).zfill(2)}_W_AG.csv")
            a2_file_path = DATA_FOLDER.joinpath(f"whisper_annotated_a2/Group_{str(group_i).zfill(2)}_W_CM.csv")
        else:
            raise ValueError(f"Unknown data type: {data_type}")

        ann_lst1 = load_annotation_csv(a1_file_path)
        ann_lst2 = load_annotation_csv(a2_file_path)
        anns1 = []
        anns2 = []

        for ann in ann_lst1:
            anns1.extend(process_annotation(ann))
        for ann in ann_lst2:
            anns2.extend(process_annotation(ann))

        assert len(anns1) == len(anns2)
        all_anns1.extend(anns1)
        all_anns2.extend(anns2)
        iaa_dict[group_i] = cohen_kappa_score(anns1, anns2)
    iaa_dict["all"] = cohen_kappa_score(all_anns1, all_anns2)
    return iaa_dict


def get_f1_with_gold(data_type: str, ann_id: int):
    f1_dict = dict()

    all_anns1 = []
    all_anns2 = []
    for group_i in range(1, 11):
        if data_type == "oracle":
            if ann_id == 1:
                ann_file_path = DATA_FOLDER.joinpath(f"annotated_a{ann_id}/Group_{str(group_i).zfill(2)}_DP_AG.csv")
            else:
                ann_file_path = DATA_FOLDER.joinpath(f"annotated_a{ann_id}/Group_{str(group_i).zfill(2)}_DP_CM.csv")
            gold_file_path = DATA_FOLDER.joinpath(f"annotated_adjudicated/Group_{str(group_i).zfill(2)}_DP.csv")
        elif data_type == "google":
            if ann_id == 1:
                ann_file_path = DATA_FOLDER.joinpath(
                    f"google_annotated_a{ann_id}/Group_{str(group_i).zfill(2)}_G_AG.csv")
            else:
                ann_file_path = DATA_FOLDER.joinpath(
                    f"google_annotated_a{ann_id}/Group_{str(group_i).zfill(2)}_G_CM.csv")
            gold_file_path = DATA_FOLDER.joinpath(f"google_annotated_adjudicated/Group_{str(group_i).zfill(2)}_G.csv")
        elif data_type == "whisper":
            if ann_id == 1:
                ann_file_path = DATA_FOLDER.joinpath(
                    f"whisper_annotated_a{ann_id}/Group_{str(group_i).zfill(2)}_W_AG.csv")
            else:
                ann_file_path = DATA_FOLDER.joinpath(
                    f"whisper_annotated_a{ann_id}/Group_{str(group_i).zfill(2)}_W_CM.csv")
            gold_file_path = DATA_FOLDER.joinpath(f"whisper_annotated_adjudicated/Group_{str(group_i).zfill(2)}_W.csv")
        else:
            raise ValueError(f"Unknown data type: {data_type}")

        ann_lst = load_annotation_csv(ann_file_path)
        gold_lst = load_annotation_csv(gold_file_path)
        anns1 = []
        anns2 = []

        for ann in ann_lst:
            anns1.extend(process_annotation(ann))
        for ann in gold_lst:
            anns2.extend(process_annotation(ann))

        assert len(anns1) == len(anns2)
        all_anns1.extend(anns1)
        all_anns2.extend(anns2)
        f1_dict[group_i] = f1_score(anns1, anns2, average="weighted")
    f1_dict["all"] = f1_score(all_anns1, all_anns2, average="weighted")
    return f1_dict


def iaa2csv(data_type: str, out_csv_file: str):
    rows = []
    iaa = get_iaa(data_type)
    f1_a1 = get_f1_with_gold(data_type, 1)
    f1_a2 = get_f1_with_gold(data_type, 2)
    rows.append([round(i, 3) for i in iaa.values()])
    rows.append([round(f * 100, 2) for f in f1_a1.values()])
    rows.append([round(f * 100, 2) for f in f1_a2.values()])
    csv_df = pd.DataFrame(rows, columns=list(iaa.keys()))
    csv_df.index = "Kappa F1-a1 F1-s2".split()
    print(csv_df)
    csv_df.to_csv(out_csv_file)


if __name__ == "__main__":
    iaa2csv("google", "data/IAA_on_google.csv")
    iaa2csv("whisper", "data/IAA_on_whisper.csv")

