import requests
import re

key_words = ["career", "vacancy", "vacancies", "hiring", "Job"]

input = open('input.csv', 'r')

urls = input.read().split('\n')

input.close()

last_home_url = 'last home url'
for url in urls:
    try:
        url = 'http://'+url
        r = requests.get(url)
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
                            if(last_home_url[len(last_home_url)-1]=='/'):
                                output.write(last_home_url + link[1:] + '\n')
                            else:
                                output.write(last_home_url + link + '\n')
                        elif(link!=''
                                and link != last_home_url
                                and link != last_home_url[:len(last_home_url)-1]
                                and link[:len(link)-1] != last_home_url):
                            output.write(link + '\n')
                            last_home_url = link
                output.close()
    except:
        if(url!='http://'):
            print(url + " is a bad one\n")
