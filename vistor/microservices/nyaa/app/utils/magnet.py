from urllib.parse import urlencode
import urllib


def get_magnet(info_hash, title):
    known_trackers = [
        "http://nyaa.tracker.wf:7777/announce",
        "udp://open.stealth.si:80/announce",
        "udp://tracker.opentrackr.org:1337/announce",
        "udp://exodus.desync.com:6969/announce",
        "udp://tracker.torrent.eu.org:451/announce"
    ]
    magnet_link = f'magnet:?xt=urn:btih:{info_hash}&{urlencode({"dn": title}, quote_via=urllib.parse.quote)}'
    for tracker in known_trackers:
        magnet_link += f'&{urlencode({"tr": tracker})}'
    return magnet_link
