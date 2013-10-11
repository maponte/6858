#from flask import g, render_template, request
from debug import *
import rpclib

@catch_err
def transfer(sender, recipient, zoobars, token):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('transfer', sender=sender,
                     recipient=recipient,
                     zoobars=zoobars,
                     token=token)
        return ret

@catch_err
def balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('balance', username=username)
        return ret

@catch_err
def get_log(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('get_log', username=username)
        return ret

@catch_err
def init_user(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('init_user', username=username)
        return ret
