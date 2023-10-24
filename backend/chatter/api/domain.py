from db import db

def get_domains():
    rows = db.get_domains()
    return rows
    
def get_domain(domain_id):
    res = db.get_domain(domain_id)
    return res
