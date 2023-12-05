'''

    Redis? what is dat
    
    okay i dunno actually maybe i really should use redis

'''

# cache object realized as a SINGLETON
class Cache:
    
    # вот тут мы обмазываемся паттернами ради прикола
    _instance = None
    
    def __call__(_class, *args, **kwargs):
        return _instance if _class._instance else object.__call__(_class, *args, **kwargs)
    
    
    # а вот тут нормальный код
    @classmethod
    def __main(self):
        self.cached_mac: list = list()
    
    #mac addresses
    @classmethod
    def is_mac_stored(self, mac):
        return mac in self.cached_mac
    
    @classmethod
    def mac_store_or_get(self, mac):
        return mac if mac in self.cached_mac else (mac, self.cached_mac.append(mac))[0]
    
    # entry point
    @classmethod
    def __init__(self):
        __main()
