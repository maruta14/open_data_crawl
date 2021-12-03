import csv


def main():

    processed_data = []
    with open("crawl_data/yamanashi_pre.csv", "r") as f, open("crawl_data/yamanashi.csv", "w") as f2:
        reader = csv.reader(f)
        writer = csv.writer(f2)
        for row in reader:
            if '山梨県／山梨県オープンデータ検索' not in row:
                writer.writerow(row)

                



if __name__=="__main__":
    main()