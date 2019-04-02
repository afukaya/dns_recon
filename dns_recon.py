#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
NAME  : dns_recon.py
AUTHOR: Alexandre Fukaya
DATE  : 25/01/2019

DESCRIPTION:
    Gather as much DNS information for a given internet domain name.
    
DEPENDENCIES:
	python-whois
	dnspython

TODO:

"""

import argparse
import sys
import socket
import whois
import dns.query
import dns.resolver
import dns.zone

def get_whois_info(domain):
    print('WHOIS info')
    try:
        whois_info = whois.whois(domain)
    except:
        print('Error getting Whois information')
        #sys.exit(2)
        
    print(whois_info.text)
    print('-' * 80)
    print('')
    
def get_servers(domain):
    print('Brute force server names')
    servers = ['ns1','ns2','www','fpt','webmail','mail']
    print('Hosts found @ ' + domain)
    for server in servers:
        fqdn = server + '.' + domain
        try:
            print(fqdn + ': ' + socket.gethostbyname(fqdn))
        except socket.gaierror:
            pass
    print('-'*80)
    print('')

def test_zone_transfer(domain):
    print('Testing DNS zone transfer')
    name_servers = dns.resolver.query(domain,'NS')
    servers = []
    for ns in name_servers:
        servers.append(str(ns))
    for server in servers:
        try:
            zone_transfer = dns.zone.from_xfr(dns.query.xfr(server,domain))
        except:
            print('Zone transfer not allowed')
        else:
            print('Zone Info')
            zone_info = zone_transfer.nodes.keys()
            zone_info.sort()
            for register in zone_info:
                print(zone_transfer[register].to_text(register))
    print('-'*80)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('domain',help='Domain name to acquire data.')
    args = parser.parse_args()

    get_whois_info(args.domain)
    test_zone_transfer(args.domain)
    get_servers(args.domain)

if __name__ == "__main__":
    main()