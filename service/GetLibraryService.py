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
            print("todo: library")

class GetZoushoService:
    """
    Input: isbn, systemids
    Output: 
    """
    zousho_url = "http://api.calil.jp/check"
