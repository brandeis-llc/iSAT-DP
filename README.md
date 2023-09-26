# iSAT-DP

### Filtering Utterances
- Get utterance transcripts from `Group_[00-10]_Oracle.csv`
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