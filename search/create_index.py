from elasticsearch import Elasticsearch


def main():
    # Elasticsearchクライアント作成
    es = Elasticsearch([
        {'host': 'datasearchj-es.kasys.org', 'port': 80}
        ])

    # es.indices.delete(index="website")
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "text": {"type": "text"},
                "url": {"type": "keyword"}
            }
        }
    }
    es.indices.create(index="website", document=mapping)

    # # インデックス一覧の取得
    indices = es.cat.indices(index='*', h='index').splitlines()
    # # インデックスの表示
    for index in indices:
        print(index)
    print(es.indices.get_mapping(index="website"))
    es.close()


if __name__=="__main__":
    main()