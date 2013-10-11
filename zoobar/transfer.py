from flask import g, render_template, request

from login import requirelogin
from zoodb import *
from debug import *
import bankclient
import traceback

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            token = g.user.token
            zoobars = eval(request.form['zoobars'])
            bankclient.transfer(g.user.person.username,
                          request.form['recipient'], zoobars, token)
            warning = "Sent %d zoobars" % zoobars
    except (KeyError, ValueError, AttributeError) as e:
        traceback.print_exc()
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)
