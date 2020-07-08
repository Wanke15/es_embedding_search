from elasticsearch import Elasticsearch

index_setting = {
  "mappings": {
      "word": {
        "type": "text"
      },
      "category": {
        "type": "text",
        "index": "not_analyzed"
      },
      "word_vector": {
        "type": "dense_vector",
        "dims": 50
      }
  }
}

# client = Elasticsearch("localhost:9200")
client = Elasticsearch("localhost:9292")


client.index(index="word_vector_index", body=index_setting)
