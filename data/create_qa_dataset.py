import argparse
import json
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser(
        description = 'Create QA dataset'
    )
    parser.add_argument(
        '-i', '--input_filepath', 
        default='full_annotation.csv',
        help='Path to .csv annotations'
    )
    parser.add_argument(
        '-c', '--corpus_dir',
        default='corpus/',
        help='file path to title2id dictionary'
    )
    parser.add_argument(
        '-d', '--dict_title2id_path',
        default='title2id.json',
        help='file path to title2id dictionary'
    )
    parser.add_argument(
        '-o', '--output_dir',
        default='qa',
        help='Output dir for dataset'
    )
    args = parser.parse_args()
    
    INPUT_FILEPATH = args.input_filepath
    corpus_dir = args.corpus_dir
    title2id_path = os.path.join(corpus_dir, args.dict_title2id_path)
    OUTPUT_FOLDER = args.output_dir

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    title2id = json.load(open(title2id_path, 'r'))

    def get_text_from_wiki(title):
        id = title2id[title]
        data_wiki = json.load(
            open(os.path.join(corpus_dir, f'{id}.json'), 'r')
        )
        text = data_wiki['text']
        return text

    full_annotation_df = pd.read_csv(INPUT_FILEPATH)

    annotations = []
    is_wikis = []


    for idx, row in full_annotation_df.iterrows():
        question = row['question']
        candidate = row['short_candidate']
        candidate_start_text = row['short_candidate_start']
        text = row['text']
        answer = row['answer']
        id = row['id']
        
        title = row['title']
        if title == '' or title not in title2id.keys():
            # not found title in wiki pages
            if 'wiki' in answer:
                # not have wiki in answer
                title = ' '.join(answer.replace('wiki/', '').split('_'))
                context = get_text_from_wiki(title)
            else:
                context = row['text']
        else:
            context = get_text_from_wiki(title)
        is_wiki = ('wiki' in answer)
        
        candidate_start_context = context.find(candidate)
        
        if candidate_start_context == -1:
            context = text
            candidate_start_context = candidate_start_text

        annotations.append(
            {
                'id': id,
                'question': question,
                'context': context,
                'text': text,
                'candidate': candidate,
                'candidate_start_text': candidate_start_text,
                'candidate_start_context': candidate_start_context,
                'answer': answer,
                'title': title
            }
        )
        is_wikis.append(is_wiki)
        print(question, context, candidate, answer)

    train_annotations, test_annotations, _, _ = train_test_split(annotations, is_wikis, test_size=0.2, random_state=42, stratify=is_wikis)

    train_dict = {
        'name': 'train',
        'data': train_annotations
    }
    with open(os.path.join(OUTPUT_FOLDER, 'train.json'), 'w', encoding='utf8') as f:
        json.dump(train_dict, f, ensure_ascii=False)

    test_dict = {
        'name': 'test',
        'data': test_annotations
    }
    with open(os.path.join(OUTPUT_FOLDER, 'test.json'), 'w', encoding='utf8') as f:
        json.dump(test_dict, f, ensure_ascii=False)
        
if __name__ == '__main__':
    main()