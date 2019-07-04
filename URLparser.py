import requests
import re

input = open("input.txt", "r+")

key_words = ["career", "vacancy", "vacancies", "hiring", "job", "jobs"]

url = input.readline()
output = open("output.txt", "w+")
pagecode_w = open("pagecode.txt", "w+")
pagecode_r = open("pagecode.txt", "r+")
while url:
    try:
        request = requests.get(url)
        pagecode_w.write(request.text.decode("utf-8"))
        for line in pagecode_r:
            href = re.search("href=", line)
            title = re.search('title=', line)
            key_word = False
            link_word = ""
            for word in key_words:
                if not key_word:
                    key_word = re.search(word, line)
                    if key_word:
                        link_word = word
            if counter>=5:
                break
            if((href and key_word) or (title and key_word)):
                link = line[line.find("href=")+6:]
                output.write(line[line.find("href=")+6:link.find('"')])
                counter = counter + 1
    except:
        pass

    url = input.readline()
