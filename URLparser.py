import requests
import re

key_words = ["career", "vacancy", "vacancies", "hiring", "jobs"]

input = open('input.csv', 'r')

urls = input.read().split('\n')

last_home_url = 'last home url'
for url in urls:
    try:
        output = open('output.csv', 'a')
        url = 'http://'+url
        r = requests.get(url)
        html = r.text
        lines = re.split('\\n', html)
        for line in lines:
            if(len(line)>200):
                continue
            for key_word in key_words:
                if(re.search(key_word, line)
                        and re.search(r'href=(")(.*?)\1', line)):
                    row = line[line.find('href')+6:]
                    link = row[:row.find('"')]
                    if(link[0] == '/'):
                        if(last_home_url[len(last_home_url)-1]=='/'):
                            output.write(last_home_url + link[1:] + '\n')
                        else:
                            output.write(last_home_url + link + '\n')
                    elif(link != last_home_url
                            and link != last_home_url[:len(last_home_url)-1]
                            and link[:len(link)-1] != last_home_url):
                        output.write(link + '\n')
                        last_home_url = link
        output.close()
    except:
        pass

input.close()
