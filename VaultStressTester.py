#!/usr/bin/env python3
import requests
import json
import logging
import argparse
import sys
import random
import uuid
import string

logger = logging.getLogger('ldw')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

logger.setLevel(logging.DEBUG)



def create_namespace(url, token,  path):
    headers = {'X-Vault-Token' :  token}
    response=requests.post(url +"/v1/sys/namespaces/{}".format(path), headers = headers)
    response.raise_for_status()

def delete_namespace(url, token, path):
    headers = {'X-Vault-Token' :  token}
    response=requests.delete(url +"/v1/sys/namespaces/{}".format(path), headers = headers)
    response.raise_for_status()
    return
    try:
        pass
    except:
        logger.error("Could not find the indicated product:")
        sys.exit(2)



def main():

    rounds = 200
    max_count  = 200
    path_lenght = 20
    namespaces = []

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Please indicate the vault url')
    parser.add_argument('-t', '--token', help='Please indicate the vault token')
    parser.add_argument('-v', action='store_true', help='Increase verbosity')
    args = parser.parse_args()
    url = args.url
    token = args.token
     
    if args.v :
        logging.info("Setting verbosity on")
        logger.setLevel(logging.DEBUG)
        
    else:
        logger.setLevel(logging.INFO)

    for i in range(rounds):
        print("Round {} ".format(i))
        to_add = random.randrange(0, max_count - len(namespaces))
        print("Adding {}/{} ".format(to_add, len(namespaces)))
        for j in range(to_add):
            path = None
            while path in namespaces or path == None:
                path = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(path_lenght))
            create_namespace(url, token, path)
            namespaces.append(path)
        
        to_del = random.randrange(0, len(namespaces))
        print("Deleting {}/{} ".format(to_del, len(namespaces)))
        for j in range(to_del):
            namespace_to_del = namespaces[random.randrange(0, len(namespaces))]
            delete_namespace(url, token, namespace_to_del)
            namespaces.remove(namespace_to_del)

    for i in range(len(namespaces)):
        delete_namespace(url, token,namespaces[i])

    
    
if __name__ == '__main__':
    main()
