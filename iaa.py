from dense_paraphrase import load_annotation_csv
from file_path import DATA_FOLDER
from sklearn.metrics import cohen_kappa_score



def process_annotation(annotation_str: str):
    comps = annotation_str.split()
    comps = ["".join(sorted(c[1:-1])) for c in comps]
    return comps


def get_iaa():
    for group_i in range(1, 11):
        a1_file_path = DATA_FOLDER.joinpath(f"annotated_a1/Group_{str(group_i).zfill(2)}_DP_AG.csv")
        a2_file_path = DATA_FOLDER.joinpath(f"annotated_a2/Group_{str(group_i).zfill(2)}_DP_CM.csv")
        ann_lst1 = load_annotation_csv(a1_file_path)
        ann_lst2 = load_annotation_csv(a2_file_path)
        anns1 = []
        anns2 = []

        for ann in ann_lst1:
            anns1.extend(process_annotation(ann))
        for ann in ann_lst2:
            anns2.extend(process_annotation(ann))
        print(anns1)
        print(anns2)
        assert len(anns1) == len(anns2)
        print(cohen_kappa_score(anns1, anns2))


if __name__ == "__main__":
    get_iaa()
