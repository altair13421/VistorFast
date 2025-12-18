from lxml import etree
from .magnet import get_magnet

# Nyaa Related
# Ok, so I took this From NyaaPy By Juanjo Salvador
def parse_rss(request_text):
    root =  etree.fromstring(request_text)
    torrents = list()
    for item in root.xpath("channel/item"):
        try:
            item_type = "remake" if (item.findtext('nyaa:remake', namespaces=item.nsmap) == "Yes") else "trusted" if (item.findtext('nyaa:trusted', namespaces=item.nsmap) == 'Yes') else "default"
            torrent = {
                "id": item.findtext('guid').split('/')[-1],
                "publish_date": item.findtext('pubDate'),
                "title": item.findtext('title'),
                'torrent_link': item.findtext('link'),
                'view_link': item.findtext('guid'),
                'magnet': get_magnet(item.findtext('nyaa:infoHash', namespaces=item.nsmap), item.findtext('title')),
                "seeders": item.findtext('nyaa:seeders', namespaces=item.nsmap),
                'category': item.findtext('nyaa:category', namespaces=item.nsmap),
                'categoryid': item.findtext('nyaa:categoryId', namespaces=item.nsmap).split('_'),
                'size': item.findtext('nyaa:size', namespaces=item.nsmap),
                'item_type': item_type
            }
            torrents.append(torrent)
        except IndexError:
            print("it passed")
    return torrents

def parse_nyaa(request_text):
    request_text = request_text
    torrents = list()
    return torrents
