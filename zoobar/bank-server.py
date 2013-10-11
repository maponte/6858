#!/usr/bin/python
#
# Insert bank server code here.
#
import rpclib
import sys
import bank
import authclient
from debug import *

class BankRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_transfer(self, sender, recipient, zoobars, token):
        if authclient.check_token(sender, token):
            return bank.transfer(sender, recipient, zoobars)
        return None
    def rpc_balance(self, username):
        return bank.balance(username)
    def rpc_get_log(self, username):
        return serialize_log(bank.get_log(username))
    def rpc_init_user(self, username):
        log('rpc_init_user('+username+')')
        return bank.init_user(username)

def serialize_log(tlog):
    ret = []
    for entry in tlog:
        ret.append({'time': entry.time,
                    'sender':entry.sender,
                    'recipient':entry.recipient,
                    'amount':entry.amount})
    return ret

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)
