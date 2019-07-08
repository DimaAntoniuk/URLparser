import requests
import re

key_words = ["career", "vacancy", "vacancies", "hiring", "Job"]

input = open('input.csv', 'r')

urls = input.read().split('\n')

input.close()

last_link = ''

for url in urls:
    try:
        url = 'http://'+url
        r = requests.get(url)
        domain = r.url
        html = r.text
        tuples = re.findall(r'(<a[^>]+/>)|(<a[^>]+>.+?</a>)', html)
        counter = 0
        for tuple in tuples:
            for line in tuple:
                output = open('output.csv', 'a')
                if (counter>5):
                    break
                for key_word in key_words:
                    if (re.search('>.*' + key_word, line)
                            or re.search('href\s*=\s*".*' + key_word, line)
                            or re.search("href\s*=\s*'.*" + key_word, line)):
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

                        if (link[0] == '/'):
                            if (domain[len(domain)-1] == '/'
                                    and last_link != domain + link[1:]):
                                link = domain + link[1:]
                            else:
                                link = domain + link
                            if(link != ''
                                    and requests.get(link).status_code == 200
                                    and requests.get(link).text.find('magento')):
                                output.write(link + '\n')
                                last_link = link
                                counter += 1
                        elif (link != '' and last_link != link
                                and requests.get(link).status_code == 200
                                and requests.get(link).text.find('magento')):
                            output.write(link + '\n')
                            last_link = link
                            counter += 1
                output.close()
    except:
        if (url != 'http://'):
            print(url + " is a bad one\n")
