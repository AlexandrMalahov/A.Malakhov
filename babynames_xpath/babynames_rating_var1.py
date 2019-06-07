from lxml import html
import re


def extract_names(filename):
    with open(filename, 'r') as f:
        tree = html.fromstring(f.read())
    year = tree.xpath('body/table/tr/td/'
                      'table/caption/h2')[0].text # такой xpath не подходит для остальных файлов, он для каждого свой.
    print((re.search(r'\d{4}', year).group()))
    baby_list = []
    for rating in tree.xpath('body/table/tr/td/table/tr[@align="right"]'):
        baby_list.append(rating[1].text + ' ' + rating[0].text)
        baby_list.append(rating[2].text + ' ' + rating[0].text)
    for baby in sorted(baby_list):
        print(baby)


extract_names('baby2008.html')
