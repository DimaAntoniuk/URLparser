import requests
import re

class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()


key_words = ["career", "vacancy", "vacancies", "hiring", "Job", "recruit", "opportunit"]

with File("test.csv", "r") as input:
    urls = input.read().split('\n')

last_link = ''
counter = 0

def delete_from_js(text):
    magento_in_js = ["Magento_", "-magento-", "/Magento/"]
    for magento in magento_in_js:
        text = text.replace(magento, '')
    pattern = r'(?i){[^}]+magento[^}]+}'
    text = re.sub(pattern, '', text)
    return text

def after_party(link):
    global last_link
    global counter
    last_link = link
    counter += 1

after_party("string")
def process_link(link):
    try:
        link_r = requests.get(link)
        link_html = link_r.text
        pattern = r'<[^>]+>'
        link_html = re.sub(pattern, "", link_html)
        link_html = delete_from_js(link_html)
        if(last_link!= link and link_r.status_code == 200
                and re.search(r'magento', link_html, re.IGNORECASE)):
            with File("strong_parse.csv", "a") as output:
                output.write(link + '\n')
            after_party(link)
    except:
        print('Bad sublink')


for url in urls:
    url = 'http://'+url
    try:
        r = requests.get(url)
        domain = r.url
        html = r.text
        pattern = r'(<a[^>]+/>)|(<a[^>]+>.+?</a>)'
        tuples = re.findall(pattern, html)
        counter = 0
        for tuple in tuples:
            for line in tuple:
                if (counter>5):
                    break
                for key_word in key_words:
                    if (re.search(r'>.*' + key_word, line)
                            or re.search(r'href\s*=\s*".*' + key_word, line, re.IGNORECASE)
                            or re.search(r"href\s*=\s*'.*" + key_word, line, re.IGNORECASE)):
                        line = line[line.find('href'):]
                        single_quotes=''
                        if (line.find("'")>=0):
                            single_quotes = line[line.find("'")+1:]
                        double_quotes = ''
                        if (line.find('"')>=0):
                            double_quotes = line[line.find('"')+1:]
                        link = ''
                        if (single_quotes):
                            link = single_quotes[:single_quotes.find("'")]
                        elif (link==''):
                            link = double_quotes[:double_quotes.find('"')]
                        link = link.strip()
                        if (link != '' and link[0] == '/'):
                            if (domain[len(domain)-1] == '/'):
                                link = domain + link[1:]
                            else:
                                link = domain + link
                            process_link(link)
                        elif (link != '' and last_link != link):
                            process_link(link)
    except :
        if (url != 'http://'):
            print(url + " is a bad one\n")
