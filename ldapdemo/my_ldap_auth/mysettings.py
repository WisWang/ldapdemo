#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
if sys.platform.startswith("linux"):
    # prod system
    LDAP_HOST=''
    USER = ''  # admin DN
    PASSWORD = '' # admin passwd
    BASE_DN = ''
    OBJC = ['account', 'simpleSecurityObject', 'top']
    DNTEMPLATE = ""
else:
    # my own mac book
    LDAP_HOST = 'ldap://192.168.3.3'
    USER = 'cn=admin,dc=node1,dc=com' #admin DN
    PASSWORD = 'secret' #admin passwd
    BASE_DN = 'dc=node1,dc=com'
    OBJC = ['organizationalperson', 'inetorgperson', 'person']
    DNTEMPLATE = "uid=%s,ou=People,dc=node1,dc=com"

