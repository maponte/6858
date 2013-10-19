#!/usr/bin/python

import rpclib
import sys
import os
import sandboxlib
import urllib
import socket
import bankclient
import zoodb
import base64
import hashlib
#import authclient

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor):
        self.user = user
        self.visitor = visitor

    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        return bankclient.get_log(username)

    def rpc_get_user_info(self, username):
        person_db = zoodb.person_setup()
        p = person_db.query(zoodb.Person).get(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': p.profile,
                 'zoobars': bankclient.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        def get_token(username):
            cred_db = zoodb.cred_setup()
            c = cred_db.query(zoodb.Cred).get(username)
            return c.token
        token = get_token(self.user)
        bankclient.transfer(self.user, target, zoobars, token)

def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, pcode, user, visitor):
        uid = 61200

        #userdir = '/tmp'
        user_dirid = base64.b32encode(hashlib.sha1(user).digest())
        userdir = '/tmp/'+user_dirid
        try:
            os.mkdir(userdir, 0700)
            os.chown(userdir, uid, uid)
        except OSError:
            pass #probably already created directory
        
        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)
