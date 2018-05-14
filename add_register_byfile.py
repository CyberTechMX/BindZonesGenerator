#!/usr/bin/env python
#-*- encoding: utf-8 -*-
__autor__ = "Jesús Gómez"
__mail__ = "zosemu@gmail.com"

def read_config():
    try:
        f = open('dns_add.conf','r').read().split('\n')
        valores = {}
        for x in f:
            j = x.replace('\r','').split('=')
            if len(j) > 0:
                valores[j[0].rstrip()] = j[1].lstrip()
        if valores['mailaddr'].find('.') > 0:
            k = valores['mailaddr'].split('.')[0].replace('@','.')
        else:
            k = valores['mailaddr'].replace('@','.')
        valores['mailaddr'] = k
        return valores
    except:
        print "[-] Error on load configuration file."

def make_entradas(valores):
    try:
        f = open(valores['file'],'r').read().split('\n')
    except:
        print "[-] Error on load configuration file:", valores['file']
        exit()
    entradas = []
    for x in f:
        k = x.replace('\r','').lower()
        if k not in entradas:
            entradas.append(k)
    if len(entradas) > 0:
        file_db = valores['file'].replace('.txt','.db')
        file_conf = file_db + '.conf'
        rdb = open(file_db,'a')
        rcf = open(file_conf,'a')
        for x in entradas:
            rdb.write("""$ORIGIN %s.\n$TTL %s;\n@ IN SOA %s. %s. ( %s %s %s %s %s )\n@ IN  NS  %s.\n@ IN  A    %s\n* IN  A    %s\n\n""" % (x,valores['ttl'],valores['server'],valores['mailaddr'],valores['serial'],valores['refresh'],valores['retry'],valores['expire'],valores['minimum'],valores['server'],valores['ip'],valores['ip']))
            rcf.write("""    zone "%s" {\n        type master;\n        file "/var/named/data/%s";\n    };\n\n""" % (x,file_db))
        rdb.close()
        rcf.close()
    return len(entradas)

def main():
    conf = read_config()
    if len(conf) > 0:
        print "[+] Configuration values loaded."
        lineas = make_entradas(conf)
        print "[+]", lineas, " Entries saved."

main()