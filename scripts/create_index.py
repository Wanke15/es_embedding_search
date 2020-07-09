from elasticsearch import Elasticsearch


index_setting = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "word": {
                "type": "text"
            },
            "category": {
                "type": "keyword"
            },
            "word_vector": {
                "type": "dense_vector",
                "dims": 50
            }
        }
    }
}

# client = Elasticsearch("localhost:9200")
client = Elasticsearch("localhost:9292")

client.indices.create(index="word_vector_index", body=index_setting)
