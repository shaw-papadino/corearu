import requests
from domain.Library import Library
from entity import APP_KEY
class GetLibraryService:
    """
    Input: isbn
    Output: systemids, libkeys, libid,formal,(address,geocode)
    """
    library_url = "http://api.calil.jp/library"
    def get_library(self, isbn, geocode, limit=5):
        query = "?appkey=" + APP_KEY + "&geocode=" + geocode[0] + "," + geocode[1] + "&limit=" + str(limit)
        response = requests.get(self.library_url + query)
        if (response.status_code == 200):
            lib_info = response.json()
            print(lib_info)

class GetZoushoService:
    """
    Input: isbn, systemids
    Output: 
    """
    zousho_url = "http://api.calil.jp/check"
    def get_zousho(self, isbn, systemids):
        systemids = list(set(systemids))
        for systemid in systemids:
            query = "?appkey=" + APP_KEY + "&isbn=" + isbn + "&systemids=" + systemid + "&format=json" 
