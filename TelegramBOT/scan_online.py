from queue import Queue
import socket
import threading
from bs4 import BeautifulSoup
import requests
import send_text

def doScan(target, chat_id):
        target_ip = socket.gethostbyname(target)
        #Port Scanning
        send_text.send_msg("Port Scanning Started", chat_id)
        print_lock = threading.Lock()
        def scan(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                con = s.connect((target, port))
                with print_lock:
                    global result
                    result = []
                    result.append(str(port))
                con.close()
            except:
                pass

        def threader():
            while True:
                worker = q.get()
                scan(worker)
                q.task_done()

        q = Queue()
        for x in range(100):
            t = threading.Thread(target=threader)
            t.daemon = True
            t.start()
        for worker in range(1, 30):
            q.put(worker)
        q.join()

        ports = ""
        for port in result:
            ports += str(port) + "\n"
        

        send_text.send_msg("Port Scanning Done", chat_id)

#---------------------[]CORS SCAN[]--------------------------------------------------------------------------------------------------------#
       
        headers = {'origin': 'https://evil.com',
                'user-agent': "'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'"}
        response = requests.get(url='http://' + target, headers=headers)
        check = response.headers
        result2 = ""
        try:
            check['Access-Control-Allow-Origin'] == 'https://evil.com'
            result2 += '[+] The target ' + target + 'is vulnerable'
            try:
                check['Access-Control-Allow-Credentials'] == 'True'
                result2 += '\n[+] Severity: High'
            except:
                result2 += '\n[*] Severity: Low'
        except:
            result2 += '[-] The target ' + target + ' is not vulnerable!'
        
        send_text.send_msg("CORS SCAN Done", chat_id)

#---------------------[]SSL SCAN[]--------------------------------------------------------------------------------------------------------#
        result3 = ""
        headers = {'Host': 'www.digicert.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Length': '35',
                'Origin': 'https://www.digicert.com',
                'Referer': 'https://www.digicert.com/help/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Te': 'trailers',
                }
        r = requests.post(url='https://www.digicert.com/api/check-host.php', headers=headers,
                        data='r=133&host=' + target + '&order_id=')
        r2 = requests.post(url='https://www.digicert.com/api/check-vuln.php', headers=headers, data='r=133&host=' + target)
        code = BeautifulSoup(r.content, 'html.parser')
        code2 = BeautifulSoup(r2.content, 'html.parser')
        prt = code.prettify()
        prt2 = code2.prettify()
        SSL_result = prt.splitlines()
        SSL_result2 = prt2.splitlines()
        for lines2 in SSL_result:
            if lines2.__contains__('<') is False:
                result3 += "\n" + str(lines2) + "\n"
            else:
                pass
        result3 += "\n[*]Looking for Common SSL/TLS Vulnerabilities"
        for lines3 in SSL_result2:
            if lines3.__contains__('<') is False:
                result3 += "\n" + str(lines3) + "\n"
            else:
                pass
        
        send_text.send_msg("SSL SCAN Done", chat_id)
#---------------------[]UCP (Unauthenticated Cache Purging) Scan[]--------------------------------------------------------------------------------------------------------#
        result4 = ""
        res = requests.get(url= 'https://' + target)

        check = res.headers
        if check.__contains__("X-Cache-Hits") or check.__contains__("X-Cache"):
            result4 += "[*] The target "+ str(target) +" is vulnerable to Unauthenticated Cache Purging."
        else:
            result4 += "[*] The target "+ str(target) +" is not vulnerable."

        send_text.send_msg("UCP SCAN Done", chat_id)

        send_text.send_msg("Scanning Completed For Target "+ target, chat_id)

        done = '[*]----- Scanning Completed -----[*]\n\n[*] Target : ' + target + '\n[*] Target IP : ' + target_ip + '\n\n[*]---------- Port Scanning ----------[*]\n' + ports + '\n\n[*]---------- CORS Scan ----------[*]\n' + result2 + '\n\n[*]---------- SSL Scan ----------[*]\n' + result3 + '\n\n[*]---------- UCP Scan ----------[*]\n' + result4
        return done
