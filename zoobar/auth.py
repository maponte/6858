from zoodb import *
from debug import *

import hashlib
import random

def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token

def login(username, password):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if not person:
        return None
    if person.password == password:
        return newtoken(db, person)
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
    newperson.password = password
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
