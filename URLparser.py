import requests
import re

key_words = ["career", "vacancy", "vacancies", "hiring", "Job"]

input = open('input.csv', 'r')

urls = input.read().split('\n')

input.close()

last_link = ''

for url in urls:
    url = 'http://'+url
    try:
        r = requests.get(url)
        domain = r.url
        html = r.text
        tuples = re.findall(r'(<a[^>]+/>)|(<a[^>]+>.+?</a>)', html)
        counter = 0
        for tuple in tuples:
            for line in tuple:
                #output = open('output.csv', 'a')
                output = open('strong_parse.csv', 'a')
                if (counter>5):
                    output.close()
                    break
                for key_word in key_words:
###################################link########################################
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
################################magento########################################
                        if (link != '' and link[0] == '/'):
                            if (domain[len(domain)-1] == '/'
                                    and last_link != domain + link[1:]):
                                link = domain + link[1:]
                            else:
                                link = domain + link
                            try:
                                link_r = requests.get(link)
                                link_html = link_r.text
                                # pattern = r'src=[\"\'][^>]+[\"\']'
                                pattern = r'<[^>]+>'
                                re.sub(pattern, "", link_html)
                                if(last_link!= link and link_r.status_code == 200
                                        and re.search(r'magento', link_html, re.IGNORECASE)):
                                    output.write(link + '\n')
                                    last_link = link
                                    counter += 1
                            except:
                                print('Bad sublink')
                        elif (link != '' and last_link != link):
                            try:
                                link_r = requests.get(link)
                                link_html = link_r.text
                                # pattern = r'src=[\"\'][^>]+[\"\']'
                                pattern = r'<[^>]+>'
                                re.sub(pattern, "", link_html)
                                if(link_r.status_code == 200
                                        and re.search(r'magento', link_html, re.IGNORECASE)):
                                    output.write(link + '\n')
                                    last_link = link
                                    counter += 1
                            except:
                                print('Bad sublink')
                output.close()
    except :
        if (url != 'http://'):
            print(url + " is a bad one\n")
