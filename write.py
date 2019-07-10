import requests
import re

input  = open('test.csv', 'r')
output = open('test.csv', 'a')

text = input.read()
text = re.sub(r'^http://www.', '', text)
text = re.sub(r'^https://www.', '', text)
output.write(text)
output.close()

# def delete_from_js(text):
#     text = text.replace('Magento_', '')
#     text = text.replace('-magento-', '')
#     text = text.replace('/Magento/', '')
#     text = re.sub(r'(?i){[^}]+magento[^}]+}', '', text)
#     return text
#
# text = requests.get('http://www.bugarttia.co.uk/jobs/').text
# pattern = r'<[^>]+>'
# text = re.sub(pattern, '', text)
# text = re.sub(r'\s+', '', text)
# text = delete_from_js(text)
# print(text)
# if(re.search('magento', text, re.IGNORECASE)):
#     print(str(text[text.find('agento')-100:text.find('agento')+100]))
# else:
#     print("NONE")
