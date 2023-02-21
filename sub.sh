subfinder -d $1 -silent -t 200 | sort -u
curl -s https://jldc.me/anubis/subdomains/$1 | grep -Po "((http|https):\/\/)?(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u
curl -s "https://rapiddns.io/subdomain/$1?full=1#result" | grep "<td><a" | cut -d '"' -f 2 | grep http | cut -d '/' -f3 | sed 's/#results//g' | sort -u
curl -s "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=$1" | jq -r .subdomains[] | sort -u
curl -s  "https://dns.bufferover.run/dns?q=.$1" | jq -r .FDNS_A[] | cut -d ',' -f2 | sort -u
curl -s "https://riddler.io/search/exportcsv?q=pld:$1" | grep -Po "(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u
curl -s "https://www.virustotal.com/ui/domains/$1/subdomains?limit=400" | grep -Po "((http|https):\/\/)?(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | sort -u
curl -s "http://web.archive.org/cdx/search/cdx?url=*.$1/*&output=text&fl=original&collapse=urlkey" | sed -e 's_https*://__' -e "s/\/.*//" | sort -u
curl -s "https://securitytrails.com/list/apex_domain/$1" | grep -Po "((http|https):\/\/)?(([\w.-]*)\.([\w]*)\.([A-z]))\w+" | grep ".$1" | sort -u
curl -s "https://crt.sh/?q=%25.$1&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | grep -v "@" | sort -u
curl -s "https://crt.sh/?q=$1&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | grep -v "@" | sort -u 
