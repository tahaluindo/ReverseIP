import socket
import requests
from bs4 import BeautifulSoup
import builtwith
from telegram.ext.updater import Updater
import send_text
updater = Updater("DAPATKAN TOKEN BOT DARI FATHERBOT", use_context=True)


def doRecon(target, chat_id):
    targetUrl = target
    if target.startswith('https://') is True:
        target = target.replace('https://', '')
    elif target.startswith('http://') is True:
        target = target.replace('http://', '')
    target_ip = socket.gethostbyname(target)

    
    # DNS Lookup
    r = requests.get('https://api.hackertarget.com/dnslookup/?q=' + target)
    dns = r.text
    send_text.send_msg("DNS Lookup Done....",chat_id)

    # Reverse DNS
    r = requests.get('https://api.hackertarget.com/reversedns/?q=' + target)
    revdns = r.text
    send_text.send_msg("Reverse DNS Lookup Done....", chat_id)

    # Zone Transfer
    r = requests.get('http://api.hackertarget.com/zonetransfer/?q=' + target)
    zt = r.text
    send_text.send_msg("Zone Transfer Done....", chat_id)

    # Headers Detection
    r = requests.get('http://api.hackertarget.com/httpheaders/?q=' + target)
    hd = r.text
    send_text.send_msg("Headers Detection Done....", chat_id)

    # Built with
    if targetUrl.startswith('https://') or targetUrl.startswith('http://') is False:
        targetUrl = "https://" + targetUrl
    built1 = ''
    built2 = ''
    built3 = ''
    built4 = ''
    built5 = ''
    try:
        output = builtwith.builtwith(targetUrl)
        built = []
        for i in output:
            key = str(i)
            built.append(key)
        for new in built:
            ok = dict(filter(lambda item: new in item[0], output.items()))
            count = len(ok[new])
            new = str(new)
            x = 0
            if count == 1:
                built1 = '[+] ' + new.capitalize() + ': ' + str(ok[new][0]) + '\n'
            elif count == 2:
                built2 = '[+] ' + new.capitalize() + ': ' + str(ok[new][0]) + ', ' + str(ok[new][1]) + '\n'
            elif count == 3:
                built3 = '[+] ' + new.capitalize() + ': ' + str(ok[new][0]) + ', ' + str(ok[new][1]) + ',' + str(
                    ok[new][2]) + '\n'
            elif count == 4:
                built4 = '[+] ' + new.capitalize() + ': ' + str(ok[new][0]) + ', ' + str(ok[new][1]) + ',' + str(
                    ok[new][2]) + ',' + str(ok[new][3]) + '\n'
            elif count == 5:
                built5 = '[+] ' + new.capitalize() + ': ' + str(ok[new][0]) + ',' + str(ok[new][1]) + ',' + str(
                    ok[new][2]) + ',' + str(ok[new][3]) + ',' + str(ok[new][4]) + '\n'
            else:
                pass
    except UnicodeError as e:
        built1 = '[+]No technology found'
        built2 = ''
        built3 = ''
        built4 = ''
        built5 = ''
    send_text.send_msg("Technology Lookup Done....", chat_id)

    # Reverse IP Lookup
    headers = {'Host': 'www.ipaddress.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Content-Length': '19',
               'Origin': 'https://www.ipaddress.com',
               'Referer': 'https://www.ipaddress.com/reverse-ip-lookup',
               'Upgrade-Insecure-Requests': '1',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-User': '?1',
               'Te': 'trailers',
               }
    r = requests.post(url='https://www.ipaddress.com/reverse-ip-lookup', headers=headers, data='host=' + target)
    try:
        code = BeautifulSoup(r.content, 'html.parser')
        main = code.find('main')
        p = main.find('p', class_='lead')
        ol = main.find('ol')
        result = p.getText()
        result2 = ol.getText()
    except AttributeError as ae:
        result = '[*] No results found'
        result2 = ''
    
    send_text.send_msg("Reverse IP Lookup Done....", chat_id)

    # SPF Records
    r = requests.get('https://easydmarc.com/tools/spf-lookup?domain=' + target)
    code = BeautifulSoup(r.content, 'html.parser')
    p = code.find('p', class_='sub-spf-record')
    try:
        spf = p.getText()
    except AttributeError as ae:
        spf = '[*]No SPF Record Publish.'
    
    send_text.send_msg("SPF Records Done....", chat_id)

    # DMARC Record
    r = requests.get('https://easydmarc.com/tools/dmarc-lookup/' + target + '?domain=' + target)
    code = BeautifulSoup(r.content, 'html.parser')
    div = code.find('div', class_='record-content')
    try:
        dmarc = div.getText()
    except AttributeError as ae:
        dmarc = '[*]No DMARC Record Publish.'
    
    send_text.send_msg("DMARC Record Done....", chat_id)


    # ASN Lookup
    r = requests.get('https://api.hackertarget.com/aslookup/?q=' + target_ip)
    asn = r.text

    send_text.send_msg("ASN Lookup Done....", chat_id)

    send_text.send_msg("Reconnaissance Completed For Target " + target, chat_id)

    done = '[*]----- Reconnaissance Completed -----[*]\n\n[*] Target : ' + target + '\n[*] Target IP : ' + target_ip + \
           '\n\n[*]---------- DNS Lookup ----------[*]\n' + dns + '\n\n[*]---------- Reverse DNS Lookup ----------[' \
                                                                  '*]\n' + revdns + '\n\n[*]---------- Zone Transfer ' \
                                                                                    '----------[*]\n' + zt + '\n\n[' \
                                                                                                             '*]---------- Header Detection ----------[*]\n' + hd + '\n\n[*]---------- Technology Lookup ----------[*]\n' + built1 + built2 + built3 + built4 + built5 + '\n\n[*]---------- Reverse IP Lookup ----------[*]\n' + result + '\n' + result2 + '\n' + '\n\n[*]---------- Checking SPF Record ----------[*]\n' + spf + '\n\n[*]---------- Checking DMARC Record ----------[*]\n' + dmarc + '\n\n[*]---------- ASN Finder ----------[*]\n' + asn
    return done
