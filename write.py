import requests
import re

if(requests.get('http://www.bugarttia.co.uk/jobs/').text.find('magento')>=0):
    print('!')
