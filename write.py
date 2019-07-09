import requests
import re

link_html = requests.get('https://www.bulkpowders.co.uk/careers-at-bulk-powders').text
pattern = r'src=[\"\'][^>]+[\"\']'
link_html = re.sub(pattern, "", link_html)
if(link_html.find('magento') or link_html.find('Magento')):
    print("YES")
