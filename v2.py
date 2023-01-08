#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import os
import sys
import subprocess


def get_allsubdomains(domain):

    url = "https://rapiddns.io/subdomain/{}?full=1#result".format(domain)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    website_table = soup.find(
        "table", {"class": "table table-striped table-bordered"})
    website_table_items = website_table.find_all('tr')

    subdomains_to_file(website_table_items)


def subdomains_to_file(data):

    file_to_write = 'subdomains.txt'

    if os.path.exists(file_to_write) == True:
        subprocess.Popen(['rm {}'.format(file_to_write)],
                         shell=True, stdin=subprocess.PIPE)
        subprocess.Popen(['touch {}'.format(file_to_write)],
                         shell=True, stdin=subprocess.PIPE)

    else:
        subprocess.Popen(['touch {}'.format(file_to_write)],
                         shell=True, stdin=subprocess.PIPE)
    for rows in data:
        d = rows.find_all('td', limit=1)
        with open(file_to_write, 'a') as file:
            for i in d:
                file.write(i.text+'\n')
                print(i.text)

if __name__ == '__main__':


	if len(sys.argv) < 2:
		print("way to use: python3 " + sys.argv[0] +" <domain> OR ./rapiddns.py <domain>")	
		sys.exit()
	get_allsubdomains(sys.argv[1])
