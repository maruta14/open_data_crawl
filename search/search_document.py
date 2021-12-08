from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

host_name = 'datasearchj-es.kasys.org'
port = 80


def main():

    es = Elasticsearch([
    {'host': host_name, 
    'port': port}
    ])
    
    s = Search(using=es, index="website") \
    .query("match", title="人口")   \

    response = s.execute()

    for hit in response:
        print(hit.meta.score, hit.title)

    es.close()


if __name__=="__main__":
    main()