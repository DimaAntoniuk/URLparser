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
        for tuple in tuples:
            for line in tuple:
                output = open('output.csv', 'a')
                for key_word in key_words:
                    if(re.search('>.*' + key_word, line)
                            or re.search('href\s*=\s*".*' + key_word, line)
                            or re.search("href\s*=\s*'.*" + key_word, line)):
                        line = line[line.find('href'):]
                        single_quotes=''
                        if(line.find("'")>=0):
                            single_quotes = line[line.find("'")+1:]
                        double_quotes = ''
                        if(line.find('"')>=0):
                            double_quotes = line[line.find('"')+1:]
                        link = ''
                        if(single_quotes):
                            link = single_quotes[:single_quotes.find("'")]
                        elif(link==''):
                            link = double_quotes[:double_quotes.find('"')]
                        link = link.strip()

                        if(link!='' and link[0] == '/'):
                            if(domain[len(domain)-1]=='/' and last_link!=domain + link[1:]):
                                output.write(domain + link[1:] + '\n')
                                last_link = domain + link[1:]
                            elif(last_link != domain + link):
                                output.write(domain + link + '\n')
                                last_link = domain + link
                        elif(link!='' and last_link != link):
                            output.write(link + '\n')
                            last_link = link
                output.close()
    except:
        if(url!='http://'):
            print(url + " is a bad one\n")
