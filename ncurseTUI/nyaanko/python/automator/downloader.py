import os
from transmission_rpc import Client
from transmission_rpc.utils import format_size, format_speed
from transmission_rpc.torrent import Status, Torrent

class TorrentClient:
    def __init__(
        self,
        download_dir,
        host = None,
        port = None,
        username = None,
        password = None,
        log_file = os.path.join(".", "torrent_logs.txt")
    ):
        self.upload_limit = 10*1024
        self.download_dir = download_dir
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.log_file = log_file

        self.client = Client(host, port, username, password)


    def add_torrent(self, torrent_: str): ...

    def get_torrents(self): ...

    def start_torrent(self, torrent_id: str|int): ...

    def start_all(self): ...

    def get_general_torrent_data(self): ...

    def get_current_torrent_data(self, torrent_id: str|int): ...

    def set_download_limit(self): ...
