import os
import json
import argparse

def main():
    parser = argparse.ArgumentParser(
        description = 'Create corpus folder containing json document for each wiki pages'
    )
    parser.add_argument(
        '-i', '--input_filepath', 
        default='wikipedia_20220620_cleaned.jsonl',
        help='Path to .jsonl wikipedia file'
    )
    parser.add_argument(
        '-o', '--output_dir',
        default='corpus/',
        help='Output folder'
    )
    args = parser.parse_args()
    
    WIKI_CORPUS_FILEPATH = args.input_filepath
    OUTPUT = args.output_dir

    os.makedirs(OUTPUT, exist_ok=True)

    id2title_dict = {}

    with open(WIKI_CORPUS_FILEPATH, 'r') as json_file:
        json_list = list(json_file)
        
    for json_str in json_list:
        result = json.loads(json_str)
        id = int(result['id'])
        filename = f"{id}.json"
        print(id, result['title'])
        id2title_dict[id] = result['title']
        with open(os.path.join(OUTPUT, filename), 'w', encoding='utf8') as json_file:
            json.dump(result, json_file, ensure_ascii=False)
            
    with open(os.path.join(OUTPUT, 'id2title.json'), 'w', encoding='utf8') as json_file:
            json.dump(id2title_dict, json_file, ensure_ascii=False)
            
    title2id_dict = {v: k for k, v in id2title_dict.items()}

    with open(os.path.join(OUTPUT, 'title2id.json'), 'w', encoding='utf8') as json_file:
            json.dump(title2id_dict, json_file, ensure_ascii=False)
    
if __name__ == '__main__':
    main()