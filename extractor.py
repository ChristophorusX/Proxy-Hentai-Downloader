#! /usr/bin/python

import re
import os

def parse(document_name):
    with open(document_name, 'r') as html_file:
        pattern = re.compile('https://exhentai.org/g/[0-9]+/[0-9a-z]{10}/')
        file_text = html_file.read()
        matches = re.findall(pattern, file_text)
        return matches


if __name__ == "__main__":
    with open("urls.txt", 'w') as result_file:
        document_name = "/Users/christophorus/Downloads/php/view-source_https___exhentai.org_favorites.php.html"
        if os.path.isfile(document_name):
            print("Now parsing document " + document_name)
            result_url_list = parse(document_name)
            for line in result_url_list[1::2]:
                result_file.write(" " + line)
            print("Document " + document_name + " has been parsed!")

        for index in range(1, 100):
            document_name = "/Users/christophorus/Downloads/php/view-source_https___exhentai.org_favorites.php_page={}.html".format(index)
            if os.path.isfile(document_name):
                print("Now parsing document " + document_name)
                result_url_list = parse(document_name)
                for line in result_url_list[1::2]:
                    result_file.write(" " + line)
                print("Document " + document_name + " has been parsed!")

        print("All documents are parsed!!!")
