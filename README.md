# iSAT-DP

## Data Preprocessing
### Filtering Utterances
- Get utterance transcripts from `Group_[00-10]_Oracle.csv`
- Remove utterances after phase 1
- Remove utterances from `Participant 4` (researcher)
- Remove utterances without explicitly mentioning the predefined pronouns and block colors
  ```
  BLOCK_NAME = {"red", "yellow", "green", "blue", "purple", "brown", "mystery"}
  PRONOUNS = {"it", "they", "them", "this", "that", "these", "those"}
  ```
  
### Aligning actions to the utterance
- Extract action annotation from `Group_[00-10]_Actions.eaf` (`ALIGNABLE_ANNOTATION` element)
- Align the actions to each filtered utterance with the longest overlapped time interval
- Output csv files to `data/filtered_aligned/`
  ```
  # Exmaple edited from std output of the Utterance Python class
  
  Utterance(id=60, speaker_id=1, start=189.91, end=196.44, text='ok and then put that on that one')
  Aligned_actions = [
            Action(annotation_id='a36', tier_id='Actions', start_ts=190.58, end_ts=192.8, component=ActionComponent(verb='put', obj='BlueBlock', prep='on', loc='Table', other_text='- 1-3'))
            Action(annotation_id='a37', tier_id='Actions', start_ts=193.38, end_ts=197.56, component=ActionComponent(verb='put', obj='BlueBlock', prep='on', loc='LeftScale', other_text='- 1-3'))
            Action(annotation_id='a228', tier_id='Object action', start_ts=190.59, end_ts=191.58, component=ActionComponent(verb='put', obj='BlueBlock', prep='on', loc='LeftScale', other_text='- Scale: lean(left)'))
            Action(annotation_id='a229', tier_id='Object action', start_ts=191.67, end_ts=192.71, component=ActionComponent(verb='put', obj='GreenBlock', prep='on', loc='LeftScale', other_text='- Scale: lean(right)'))
            Action(annotation_id='a49', tier_id='Object action', start_ts=193.39, end_ts=198.75, component=ActionComponent(verb='put', obj='BlueBlock', prep='on', loc='RightScale', other_text='- Scale: lean(zero)'))
            Action(annotation_id='a58', tier_id='Action2', start_ts=191.67, end_ts=192.71, component=ActionComponent(verb='put', obj='GreenBlock', prep='on', loc='LeftScale', other_text='- 1-1'))
             ]
  ```
  
## Block Pronoun Annotation Task
This annotation task is about identifying the actual blocks the pronouns are
referring to in the utterance transcripts.
For example, in the utterance `"yeah ok so now we know [that] [this] is also ten"`,
we want to annotate `[this]` with `red block` based on the text and video context.

### Data
The starter files are located in `data/filtered_aligned/Group_[01-10].csv`.
Here is the description of the columns:
```
Utterance       utterance id inherited from Group_[xx]_Oracle.csv
Participant     participant id inherited from Group_[xx]_Oracle.csv
Start           utterance start time (in seconds)
End             utterance end time (in seconds)
Transcript      transcript with pronouns wrapped in '[]'
Action_Objects  block objects mentioned in the aligned actions
Annotation      placeholders for the pronoun annotation
```

### Annotation
You will examine every bracket-wrapped pronoun from the `Transcript` column to check whether
it's referring to any block objects and add your annotation to the `Anntotation` column.

For each bracket-wrapped pronoun, the `Annotation` column has the placeholder in the format of `[-]`.
- Replace the `-` with a single letter from the following list if the pronoun is referring to a single block object (e.g., `[-] -> [r]`):
  ```
  r - red
  g - green
  b - blue
  p - purple
  y - yellow
  m - mystery
  ```
- Replace the `-` with a combination of multiple letters (order doesn't matter) from the list if the pronoun is referring to a group of block objects (e.g., `[-] -> [rb]`)
- Leave the placeholder unchanged if the pronoun has nothing to do with the block objects (e.g., it's referring to the scale; it's a clause connective, etc)

You may use any resources (video context, transcript context, objects from aligned actions) that can help you with the annotation.
