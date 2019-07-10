import requests
import re

output = open('test.txt', 'w')

def delete_from_js(text):
    text = text.replace('Magento_', '')
    text = text.replace('-magento-', '')
    text = text.replace('/Magento/', '')
    text = re.sub(r'(?i){[^}]+magento[^}]+}', '', text)
    return text

text = requests.get('http://www.bugarttia.co.uk/jobs/').text
pattern = r'<[^>]+>'
text = re.sub(pattern, '', text)
text = re.sub(r'\s+', '', text)
text = delete_from_js(text)
print(text)
if(re.search('magento', text, re.IGNORECASE)):
    print(str(text[text.find('agento')-100:text.find('agento')+100]))
else:
    print("NONE")
