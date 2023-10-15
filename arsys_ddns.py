import configparser
import sys
import zeep
from zeep.transports import Transport
import requests
from requests.auth import HTTPBasicAuth

config = configparser.ConfigParser()
config.read('config.ini')



API_login = config["arsys.api"]["User"]
API_secret = config["arsys.api"]["Secret"]


domain = config["arsys.dns"]["Domain"]
subdomain = config["arsys.dns"]["Subdomain"]

url = 'https://api.servidoresdns.net:54321/hosting/api/soap/index.php?wsdl'

def check_ip_change():
    old_ip_res = info_dns_zone(domain,subdomain)
    if(old_ip_res["errorCode"] != 0):
        exit(1)
    old_ip = old_ip_res["res"]["data"][0]["value"]
    current_ip = requests.get("http://ifconfig.me").text
    if(old_ip == current_ip):
        exit(0)
    else:
        print("IP has changed from " + old_ip + " to " + current_ip)
        res = modify_dns_entry(old_ip,current_ip)
        if(res["errorCode"] == 0):
            exit(0)
    exit(1) 


def modify_dns_entry(currentvalue, newvalue):
    params = {"domain":domain,"dns":subdomain,"currenttype":'A',"currentvalue":currentvalue,"newtype": "A","newvalue":newvalue}
    session = requests.Session()
    session.auth = HTTPBasicAuth(API_login, API_secret)
    transport = Transport(session=session)
    client = zeep.Client(url, transport=transport)
    response = client.service.ModifyDNSEntry(input=params)
    return response

def info_dns_zone(domain,subdomain):
    params = {"domain":domain,"dns":subdomain,"type":'A',"value":''}
    session = requests.Session()
    session.auth = HTTPBasicAuth(API_login, API_secret)
    transport = Transport(session=session)
    client = zeep.Client(url, transport=transport)
    response = client.service.InfoDNSZone(input=params)
    return response



if __name__ == "__main__":
    check_ip_change()
