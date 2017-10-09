import re


def parse(document_name):
    with open("/Users/christophorus/Downloads/php/" + document_name, 'r') as html_file:
        pattern = re.compile('https://exhentai.org/g/[0-9]+/[0-9a-z]{10}/')
        file_text = html_file.read()
        matches = re.findall(pattern, file_text)
        return matches


if __name__ == "__main__":
    with open("urls.txt", 'w') as result_file:
        for i in range(0, 17):
            # document_name = "view-source_https___exhentai.org_favorites.php_page=" + \
            #     str(i) + ".html"
            document_name = "view-source_https___exhentai.org_favorites.php.html"
            print("Now parsing document " + document_name)
            result_url_list = parse(document_name)
            for line in result_url_list[1::2]:
                result_file.write(" " + line)
            print("Document " + document_name + " has been parsed!")
