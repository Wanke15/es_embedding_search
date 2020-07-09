import json

import gensim
from elasticsearch import Elasticsearch

# client = Elasticsearch("localhost:9200")
client = Elasticsearch("localhost:9292")

import time

print('Start loading...')
start = time.time()
model = gensim.models.KeyedVectors.load_word2vec_format("./data/glove.6B.50d.txt")
print('Load model time consumed: {:.2f}'.format(time.time() - start))


def query(word, cat=None, index_name='word_vector_index', size=3):
    query_vector = model.get_vector(word).tolist()
    if cat is None:
        script_query = {
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, doc['word_vector']) + 1.0",
                        "params": {
                            "query_vector": query_vector
                        }
                    }
                }
            },
            "_source": ["word"]
        }
    else:
        script_query = {
            "query": {
                "script_score": {
                    "query": {
                        "match": {
                            "category": cat
                        }
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, doc['word_vector']) + 1.0",
                        "params": {
                            "query_vector": query_vector
                        }
                    }
                }
            },
            "_source": ["word"]
        }
    response = client.search(
        index=index_name,
        body=script_query,
        size=size
    )
    print(json.dumps(response['hits']['hits'], indent=4))


query("mice")
query("mice", 'sports')
query("mice", 'food')

