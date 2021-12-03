from elasticsearch import Elasticsearch
import glob
import csv

DATA_PATH = "../crawl_data/a*.csv"
host_name = 'datasearchj-es.kasys.org'
port = 80


def main():
    files = glob.glob(DATA_PATH)

    es = Elasticsearch([
    {'host': host_name, 
    'port': port}
    ])
    
    for file in files:
        with open(file, "r") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                doc = {
                    
                }





if __name__=="__main__":
    main()