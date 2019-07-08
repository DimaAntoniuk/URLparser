import requests
import re

string = requests.get('https://za.pearson.com/careers/career-opportunities.html').text
if(string.find('magento')):
    print('found')
