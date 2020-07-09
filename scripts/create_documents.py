import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import gensim

selected_words = {"sports": ['basketball', 'football', 'swimming', 'volleyball', 'run'],
                  "food": ['cheese', 'bread', 'beer', 'milk', 'banana'],
                  "room_things": ['shoes', 'shirts', 'scarf', 'pillow', 'bed']}


def create_doc():
    import time
    print('Start loading...')
    start = time.time()
    model = gensim.models.KeyedVectors.load_word2vec_format("../data/glove.6B.50d.txt")
    print('Load model time consumed: {:.2f}'.format(time.time() - start))
    docs = []
    for cat in selected_words:
        for word in selected_words[cat]:
            _doc = {"word": word, "category": cat, "word_vector": model[word].tolist()}
            docs.append(_doc)
    with open('../data/documents.jsonl', 'w') as f:
        for _doc in docs:
            f.write(json.dumps(_doc) + '\n')


def insert_to_es(doc_path='../data/documents.jsonl', index_name='word_vector_index'):
    # client = Elasticsearch("localhost:9200")
    client = Elasticsearch("localhost:9292")

    docs = []
    with open(doc_path, 'r') as f:
        for idx, line in enumerate(f):
            record = json.loads(line.strip())
            docs.append({
                '_index': index_name,
                '_id': idx,
                "_source": {
                    'word': record['word'],
                    'category': record['category'],
                    'word_vector': record['word_vector']}
            })
    bulk(client, docs)


if __name__ == '__main__':
    # create_doc()

    insert_to_es()
