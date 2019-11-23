# IP address manipulation

import urllib.request
import json
from app.models import db, IPAddress

base_url = 'http://ip-api.com/json/%s'

def api_query(ip_addr):
    full_query = base_url % (ip_addr)
    req = urllib.request.Request(full_query)
    return json.loads(urllib.request.urlopen(req).read())

def get_location(ip_addr):
    # first, check the databse to see if there is a matching record
    match = IPAddress.query.filter_by(ip_str=str(ip_addr)).first()

    if match is not None:
        return match.location

    # since the ip is not in the database, query the API
    qres = api_query(ip_addr)

    final_result = ''

    if qres['status'] == 'success':
        final_result = qres['country']
    else:
        final_result = qres['message']

    # add the result to the database
    new_address = IPAddress(ip_addr, final_result)
    db.session.add(new_address)
    db.session.commit()

    return final_result
