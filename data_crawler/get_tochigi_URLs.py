import re
import pickle

def main():
    processed_urls = []
    with open("./htmls/tochigi.txt", "r") as f:
        for line in f:
            urls = re.findall(r'表示する。" href=".+?"', line)
            for url in urls:
                processed_url = re.split('\"', url)[2]
                processed_urls.append(processed_url)

    with open('./urls/tochigi_ulrs.pickle', "wb") as f2:
        pickle.dump(processed_urls, f2)

if __name__ == '__main__':
    main()