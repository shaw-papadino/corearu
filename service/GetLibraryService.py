import requests
import time
from domain.Library import Library
from entity import APP_KEY
class GetLibraryService:
    """
    Input: isbn
    Output: systemids, libkeys, libid,formal,(address,geocode)
    """
    library_url = "http://api.calil.jp/library"
    def get(self, geocode, limit=5):
        query = "?appkey=" + APP_KEY + "&geocode=" + geocode[0] + "," + geocode[1] + "&limit=" + str(limit) + "&format=json&callback="
        response = requests.get(self.library_url + query)
        if (response.status_code == 200):
            lib_info = response.json()
            return lib_info
            
    def adapt(self, lib_info):
        # 不要な要素を削除して返す
        l = ["libkey", "distance", "geocode", "systemid", "address", "formal"]
        lib_update = []
        info_update = {}
        for d in lib_info:
            for k, v in d.items():
                if(k in l):
                    info_update.setdefault(k,v)
            lib_update.append(info_update)
        return lib_update

        # return list(map(lambda x: x.pop(["category"], x.pop(["city"], x.pop(["short"], x.pop(["pref"], x.pop(["primary"], x.pop(["faid"], x.pop(["libid"], x.pop(["tel"], x.pop(["systemname"], x.pop(["isil"], x.pop(["post"], x.pop(["url_pc"], lib_c))

class GetZoushoService:
    """
    Input: 
        [ 
            {
                [x]"libkey": "松枝図書室",
                [x]"distance": 4.80656815509917,
                [x]"geocode": "136.750497,35.354231",
                [x]"systemid": "Gifu_Kasamatsu",
                [x]"address": "岐阜県羽島郡笠松町長池292番地",
                [x]"formal": "笠松町松枝公民館図書室"
            }
        ]
    response:
        {
          "session": "f9f33b9178f5556fff533845c8eaa4d6",
          "continue": 0,
          "books": {
            [isbn]"4834000826": {
              [systemid]"Tokyo_NDL": {
                "status": "Cache",
                "libkey": {
                  [libkey]"国際子ども図書館": [status]"蔵書あり"
                },
                "reserveurl": "https://ndlonline.ndl.go.jp/#!/detail/R300000001-I000002726097-00"
              },
              "Aomori_Pref": {
                "status": "Cache",
                "libkey": {
                  "青県図": "貸出可"
                },
                "reserveurl": "https://api.calil.jp/reserve?id=ae595257bb5e59c66f0ef813a2f6a381"
              }
            }
          }
        }
    Output: 
        [
            {
                "formal":"",
                "status":true,
                "address":""
                "distance": 1.2032
            }
        ]
    """
    zousho_url = "http://api.calil.jp/check"
    def get(self, isbn, lib_info):
        system_ids = list(map(lambda x: x["systemid"], lib_info))
        squery = ",".join(system_ids)
        query = "?appkey=" + APP_KEY + "&isbn=" + isbn + "&systemid=" + squery + "&format=json&callback=" 
        response = polling(requests.get(self.zousho_url + query))
        output = []
        for id in system_ids:
            libkeys = response["book"][isbn][id]["libkey"]
            if (len(libkeys) != 0):
                # libkey毎に必要な値をlib_infoから取得する
                output.append(list(map(lambda x: {
                    "formal":x["formal"],
                    "status":libkeys.get(x["libkey"]),
                    "address":x["address"],
                    "distance":x["distance"]
                    } if x["libkey"] in libkeys else {} )))
        # 距離の近い順にsort
        output.sort(key = lambda x: x["distance"])
        return output

    def polling(self, f):
        while True:
            response = f()
            if (response.status_code == 200):
                res = response.json()
                if (res["continue"] == 0):
                    return res
            time.sleep(1)
