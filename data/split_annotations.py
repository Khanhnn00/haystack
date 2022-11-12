import os
import pandas as pd
import json

TRAIN_FILEPATH = 'e2eqa-train+public_test-v1/zac2022_train_merged_final.json'

train_dict = json.load(open(TRAIN_FILEPATH, 'r'))
data = train_dict['data']
full_df = pd.DataFrame.from_dict(data)

full_annotation_df = full_df[full_df['category'] == 'FULL_ANNOTATION']
partial_annotation_df = full_df[full_df['category'] == 'PARTIAL_ANNOTATION']
false_long_annotation_df = full_df[full_df['category'] == 'FALSE_LONG_ANSWER']

full_annotation_df.to_csv('full_annotation.csv')
partial_annotation_df.to_csv('partial_annotation.csv')
false_long_annotation_df.to_csv('false_long_answer.csv')