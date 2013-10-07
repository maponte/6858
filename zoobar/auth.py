from zoodb import *
from debug import *

import hashlib
#import random
import os
import pbkdf2
import binascii

def randword():
    return os.urandom(4)

def pbkdf2hash(pw, salt):
    #return hashlib.md5(x).hexdigest()
    return pbkdf2.PBKDF2(pw, salt).hexread(32)

def b64_enc(binstr):
    return binascii.b2a_base64(binstr)

def b64_dec(ascstr):
    pass

def newtoken(db, cred):
    #hashinput = "%s%.10f" % (cred.password, get_rand())
    cred.token = pbkdf2hash(cred.password, randword())
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None
    if check_pw(cred, password):
        return newtoken(db, cred)
    else:
        return None

def register(username, password):
    db = person_setup()
    person = db.query(Person).get(username)
    if person:
        return None
    newperson = Person()
    newperson.username = username
    
    db.add(newperson)
    db.commit()
    newperson = Cred()
    newperson.username = username
    salt = b64_enc(randword())
    newperson.salt = unicode(salt)
    newperson.password = pbkdf2hash(password, salt)
    cdb = cred_setup()
    cdb.add(newperson)
    cdb.commit()
    return newtoken(cdb, newperson)

def check_token(username, token):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if person and person.token == token:
        return True
    else:
        return False

def check_pw(cred, pw):
    salt = str(cred.salt)
    log(salt)
    log(pbkdf2hash(pw,salt))
    log(cred.password)
    return pbkdf2hash(pw, salt) == cred.password
