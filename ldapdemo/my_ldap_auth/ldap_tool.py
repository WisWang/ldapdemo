#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ldap
from my_ldap_auth.mysettings import *


class LdapTool(object):

    def __init__(self):
        conn = ldap.initialize(LDAP_HOST)
        conn.simple_bind_s(USER, PASSWORD)
        self.conn = conn

    def check_user(self, username):
        self.conn.simple_bind_s(USER, PASSWORD)
        filter = '(uid=%s)' % username
        attrs = ['sn', 'uid']
        ret = self.conn.search_s(BASE_DN, ldap.SCOPE_SUBTREE, filter, attrs)
        if ret:
            return ret[0][0]
        else:
            return False

    def check_pass(self, username, userpass):
        dn = self.check_user(username)
        if dn:
            try:  # secret and username OK
                self.conn.simple_bind_s(dn,userpass)
                return 0
            except ldap.LDAPError, e: #secret not correct
                return e
        else: #username not found
            return 1

    def reset_pass(self,username,password):
        dn = self.check_user(username)
        mod_attrs = [(ldap.MOD_REPLACE, "userPassword",password), ]
        self.conn.modify_s(dn, mod_attrs)

    def chpass(self,username,oldpass,newpass):
        dn = self.check_user(username)
        self.conn.passwd_s(dn, oldpass, newpass)

    def signup(self,username,newpass,objclass=OBJC):
        dn = DNTEMPLATE % username
        if sys.platform.startswith("linux"):
            # prod parameter
            add_record = [
                ('objectclass', objclass),
                ('uid', [username]),
                ('cn', [username]),
                ('sn', [username]),
                ('userpassword', [newpass]),
                ('ou', ['People']),
                ('mail', ['%s@prod.com'%username])
            ]
        else:
            # my dev parameter
            add_record = [
                ('objectclass', objclass),
                ('uid', [username]),
                ('cn', [username]),
                ('sn', [username]),
                ('userpassword', [newpass]),
                ('ou', ['People']),
                ('mail', ['%s@dev.com'%username])
            ]
        self.conn.simple_bind_s(USER, PASSWORD)
        self. conn.add_s(dn,add_record)

    def del_user(self,username):
        dn = self.check_user(username)
        self.conn.delete_s(dn)

def test():
    conn = ldap.initialize(LDAP_HOST)
    # conn.protocol_version = ldap.VERSION3
    # print conn.simple_bind_s("uid=test,ou=People,%s"%BASE_DN, "555")# test the username and passwd
    print "test"
    conn.simple_bind_s(USER,PASSWORD)
    print "test finish"


if __name__ == "__main__":
    print LDAP_HOST
    test()


