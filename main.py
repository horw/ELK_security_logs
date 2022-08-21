from elasticsearch import Elasticsearch

from search_queries import destAddressQuery, eventType, requiredURL, timeWindow
from log.proxy.reader import ProxyFileReader
from log.proxy.parser import ProxyParser

es = Elasticsearch(['http://localhost:9200'])

data = ProxyFileReader('proxy.log').get_data()

pattern = r'dst=(.*?) dhost=(.*?) suser=(.*?) src=(.*?) sport=(.*?) tierep=(.*?) in=(.*?) out=(.*?) requestMethod=(.*?) request=(.*?) '


for items in ProxyParser(pattern, data).search():

    daddr, dhost, suser, saddr, sport, *_, req_method, req = items
    print(
        f"Source \"addr:port@user\" \"{saddr}:{sport}@{suser}\"\n",
        f"Dest \"addr - domain - url\" \"{daddr} - {dhost} - {req}\""
    )

    daddr_query = destAddressQuery(daddr)
    res = es.search(
        size=100,
        query=daddr_query.get_query()
    )

    if res['hits']['total']['value']:
        print(f"Total found {res['hits']['total']['value']} logs related to this host address")
        query, script = daddr_query.update_by(dhost)
        es.update_by_query(
            index='security-index',
            query=query,
            script=script
        )
    else:
        print("There aren't information about this host in current .evtx file")

    print('-'*100)


def log_between_logon_and_request(start_event_name, stop_url_event):

    res = es.search(
        size=1,
        query=eventType(start_event_name).get_query()
    )
    logon_time = res['hits']['hits'][0]['_source']['@timestamp']

    res = es.search(
        size=1,
        query=requiredURL(stop_url_event).get_query()
    )
    requests_time = res['hits']['hits'][0]['_source']['@timestamp']

    res = es.search(
        size=100,
        query=timeWindow(logon_time, requests_time).get_query()
    )

    print(f"From {logon_time} to {requests_time} total occurred {len(res['hits']['hits'])} events")


log_between_logon_and_request("Logon","pastebin.com")
