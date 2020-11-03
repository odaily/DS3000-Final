from lxml import html
import requests

r = requests.get("https://www.theguardian.com/news/datablog/2012/oct/15/us-presidents-listed")
r.encoding = 'utf-8'
tree = html.fromstring(r.content)

table = tree.xpath('//table[@class="in-article sortable"]')[0]
table = table.xpath('./tbody')[0]
rows = table.xpath('./tr')

data = []

for row in rows:
    cols = row.xpath('./td')
    year = cols[0].xpath('./text()')[0].strip()
    party = cols[2].xpath('./text()')[0].strip()
    print(year, party)
    data.append(f"{year}, {party}")

f = open("year_party_data.txt", "w+", encoding='utf-8')
f.write('\n'.join(data))
f.close()