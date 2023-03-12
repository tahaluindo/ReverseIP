from ast import Or
import socket
import requests
import send_text
import builtwith
import os

def doEnum(target, chat_id):
    target_ip = socket.gethostbyname(target)
    
    #Enumerating Subdomains
    r = requests.get('https://api.hackertarget.com/hostsearch/?q=' +target)
    sub = r.text
    string = ''.join((element for element in sub if not element.isdigit()))
    final_subdomain = string.replace(',...', '')
    send_text.send_msg("Enumerating Subdomains Done....", chat_id)
    

    #Finding WaybackUrls
    r = requests.get(url='http://web.archive.org/cdx/search/cdx?url=*.' + target + '/*&output=json&fl=original&collapse=urlkey')
    r1 = r.text
    r2 = r1.replace('[', '')
    r3 = r2.replace(']', '')
    r4 = r3.replace('"', '')
    result_waybackurl = r4.replace(',', '')
    send_text.send_msg("Finding WaybackUrls Done....", chat_id)

    #Smart Fuzzing
    dict = {
    0:"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/Apache.fuzz.txt",
    1:"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/nginx.txt",
    2:"https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/IIS.fuzz.txt",
    3:'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/PHP.fuzz.txt',
    4:'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/oracle.txt'
    }

    if target.startswith('https://') is False or target.startswith('http://') is False:
        target = 'https://' + target
    if target.endswith('/') is False:
        target = target+'/'
    built = builtwith.builtwith(target)
    ws = ''
    for keys in built:
        if keys == 'web-servers':
                ws = str(built[keys])

    global result
    result = ""
    
    def fuzz(file):
        for lines in file:
            code = 404
            if lines.startswith('/'):
                lines = lines[1:]
                req = requests.get(target+lines)
                code = req.status_code

            if code == 200 | code == 403 | code == 301:
                result = str(target+lines+' : ' + str(code))

    def perform(name, res):
        r = requests.get(res)
        filename = str(name)
        with open(filename, 'w') as f:
            f.write(r.text)
        fuzz(filename)
        os.remove(filename)

        if ws.__contains__('Apache'):
            res = dict[0]
            perform('apache', res)
        
        elif ws.__contains__('Nginx'):
            res = dict[1]
            perform('nginx', res)
        
        elif ws.__contains__('IIS'):
            res = dict[2]
            perform('IIS', res)
        
        elif ws.__contains__('PHP'):
            res = dict[3]
            perform('PHP', res)
        
        elif ws.__contains__('Oracle'):
            res = dict[4]
            perform('oracle', res)
    
    if result == "":
        r = requests.get(target)
        result = "Status : " + str(r.status_code)

    send_text.send_msg("Smart Fuzzing Completed For Target " + target, chat_id)

    send_text.send_msg("Enumeration Completed For Target " + target, chat_id)
    

    done = '[*]----- Enumeration Completed -----[*]\n\n[*] Target : ' + target + '\n[*] Target IP : ' + target_ip + '\n\n[*]---------- Enumerating Subdomains ----------[*]\n' + final_subdomain + '\n\n[*]---------- Finding WaybackUrls ----------[*]\n' + result_waybackurl + '\n\n[*]---------- Smart Fuzzing ----------[*]\n' + result
    
    return done
