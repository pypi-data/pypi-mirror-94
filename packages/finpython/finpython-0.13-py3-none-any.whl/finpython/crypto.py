import requests as r
import json
import datetime as dt

class Messari:
    url = 'https://data.messari.io/api/v1/assets/{crypto}/metrics/price/time-series?start={start}&end={end}&interval=1d&columns=open'
    def __init__(self):
        print('loaded')
    def last_30_days(self,crypto):
        start = (dt.datetime.now() - dt.timedelta(30)).strftime("%Y-%m-%d")
        end = dt.datetime.now().strftime("%Y-%m-%d")
        url = Messari.url.format(crypto=crypto,start=start,end=end)
        content = r.get(Messari.url.format(crypto=crypto,start=start,end=end))
        values = json.loads(content.text)['data']['values']
        x= list(map (lambda v: v[0], values))
        y= list(map (lambda v: v[1], values))
        return x,y