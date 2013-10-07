#from flask import g, render_template, request
from debug import *
import rpclib

@catch_err
def login(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('login', username=username, password=password)
        return ret

@catch_err
def check_token(username, token):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('check_token', username=username, token=token)
        return ret

@catch_err
def register(username, password):
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('register', username=username, password=password)
        return ret
