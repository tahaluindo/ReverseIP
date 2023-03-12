import os
import requests
import send_text

VulContents = {
    "Agile CRM": "Sorry, this page is no longer available.",
    "Airee.ru": "Ошибка 402. Сервис Айри.рф не оплачен",
    "Anima": "If this is your website and you've just created it, try refreshing in a minute",
    "AWS/S3": "The specified bucket does not exist",
    "Bitbucket": "Repository not found",
    "Campaign Monitor": "Trying to access your account?",
    "Digital Ocean": "Domain uses DO name servers with no records in DO.",
    "Fastly": "Fastly error: unknown domain:",
    "Gemfury": "404: This page could not be found.",
    "Ghost": "The thing you were looking for is no longer here, or never was",
    "Github": "There isn't a GitHub Pages site here.",
    "HatenaBlog": "404 Blog is not found",
    "Help Juice": "We could not find what you're looking for.",
    "Help Scout": "No settings were found for this company:",
    "Intercom": "Uh oh. That page doesn't exist.",
    "JetBrains": "is not a registered InCloud YouTrack",
    "Kinsta": "No Site For Domain",
    "LaunchRock": "It looks like you may have taken a wrong turn somewhere. Don't worry...it happens to all of us.",
    "Ngrok": "Tunnel *.ngrok.io not found",
    "Pantheon": "404 error unknown site!",
    "Pingdom": "Sorry, couldn't find the status page",
    "Readme.io": "Project doesnt exist... yet!",
    "Short.io": "Link does not exist",
    "SmartJobBoard": "This job board website is either expired or its domain name is invalid.",
    "Strikingly": "page not found",
    "Surge.sh": "project not found",
    "Uberflip": "Non-hub domain, The URL you've accessed does not provide a hub.",
    "Shopify": "Sorry, this shop is currently unavailable.",
    "Uptimerobot": "page not found",
    "UserVoice": "This UserVoice subdomain is currently available!",
    "Wix": "Looks Like This Domain Isn't Connected To A Website Yet!",
    "Wordpress": "Do you want to register *.wordpress.com?",
    "Worksites": "Hello! Sorry, but the website you&rsquo;re looking for doesn&rsquo;t exist."
}

def doVulac(target, chat_id):
    #Subdomain Takeover
    r = requests.get('https://api.hackertarget.com/hostsearch/?q=' + target)
    sub = r.text
    string = ''.join((element for element in sub if not element.isdigit()))
    final_subdomain = string.replace(',...', '')
    with open('temp_sub', 'w') as f:
        f.write(final_subdomain)
    of = open('temp_sub', 'r+')
    result = ""
    for lines in of:
        try:    
            r = requests.get('https://' + lines)
            cont = r.text
            for key,vul in VulContents.items():
                if cont._contains_(vul):
                    result += (lines + "is vulnerable to " + key + " takeover.\n")
                else:
                    pass
        except:
            result += ("No Vulnerabilites Found in : " + lines + "\n")
            continue
    of.close()
    os.remove('temp_sub')
    send_text.send_msg("Subdomain Takeover Done....", chat_id)

    done = "Subdomain Takeover Done \n" + result
    return done
