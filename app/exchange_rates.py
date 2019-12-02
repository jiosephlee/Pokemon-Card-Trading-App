import urllib.request
from app.models import ExchangeRate, db
import json
import time

# the purpose of these functions is to return an exchange rate from USD to some other currency

base_url = "https://api.exchangerate-api.com/v4/latest/%s"

# for all of these, we assume that currency is a currency that exists within the API. Since we're the ones who are controlling the currency, we don't need to make sure that it exists.


def add_exchange_rate(currency):
    full_query = base_url % (currency)
    req = urllib.request.Request(full_query)
    data = json.loads(urllib.request.urlopen(req).read())

    new_rate = ExchangeRate(currency, data['rates']['USD'], int(time.time()))
    db.session.add(new_rate)
    db.session.commit()



def update_exchange_rate(currency):
    # check if the database has the exchange rate
    check = ExchangeRate.query.filter_by(currency=currency).first()
    if check is None:
        add_exchange_rate(currency)
    elif check.timestamp < int(time.time()) - 24 * 60 * 60:
        db.session.delete(check)
        db.session.commit()
        add_exchange_rate(currency)


def get_exhange_rate(currency):
    update_exchange_rate(currency)

    req = ExchangeRate.query.filter_by(currency=currency).first()

    #print(req.currency, req.rate)

    return req.rate
