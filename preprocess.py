import pandas as pd

from ingest_dialogue import Dialogue, ingest_dialogue


def extract_valid_utterances(dialogue: Dialogue):
    uttrs = []
    keywords = []
    for uttr in dialogue.utterances:
        if not uttr.is_researcher and (uttr.contain_block_name or uttr.contain_pronouns):
            uttrs.append(uttr)
            keywords.append(uttr.contain_block_name + uttr.contain_pronouns)
    return uttrs, keywords


if __name__ == '__main__':
    group_number = 1
    dialogue = ingest_dialogue(group_number)
    uttrs, keywords = extract_valid_utterances(dialogue)
    out_rows = []
    for u, k in zip(uttrs, keywords):
        # print(k, u.text, sep="\t")
        out_rows.append([u.speaker_id, u.text, ", ".join(k)])
    pd.DataFrame(out_rows, columns="Participant Transcript keywords".split()).to_csv(f"out_{group_number}.csv", index=False)
