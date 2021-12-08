from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import glob
import csv

DATA_PATH = "../crawl_data/e*.csv"
host_name = 'datasearchj-es.kasys.org'
port = 80


def main():
    files = glob.glob(DATA_PATH)

    es = Elasticsearch([
    {'host': host_name, 
    'port': port}
    ])
    
    data_id = 1
    for data_file in files:
        with open(data_file, "r") as f:
            reader = csv.reader(f)
            for row_idx, data_row in enumerate(reader):
                if row_idx == 0:
                    continue
                doc = {
                    'text': data_row[0],
                    'title': data_row[1],
                    'url': data_row[2]
                }
                es.create(index="website", body=doc, id=data_id)
                data_id += 1
    
    es.close()


if __name__=="__main__":
    main()