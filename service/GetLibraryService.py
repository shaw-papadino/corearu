import requests
import json
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

            # print(f"lib:{lib_info}")
            return lib_info
            
    def adapt(self, lib_info,l = ["libid", "libkey", "distance", "geocode", "systemid", "address", "formal"]
):
        # 不要な要素を削除して返す
        lib_update = []
        for d in lib_info:
            info_update = {}
            for k, v in d.items():
                if(k in l):
                    info_update.setdefault(k,v)
            lib_update.append(info_update)
        return lib_update


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
    Output: 
        [
            {
                "systemid":"",
                "libkey": "",
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
        response = self.polling(self.zousho_url + query)
        # print(f"res:{response}")
        """
        {
          "session": "2d83ba454f7a8bb9aad5b35c122f1773",
          "continue": 0,
          "books": {
            "9784591159224": {
                  "Univ_Teikyo": {
                    "status": "OK",
                    "libkey": {},
                    "reserveurl": ""
                  },
                  "Tokyo_Setagaya": {
                    "status": "OK",
                    "libkey": {
                      "世田谷": "貸出可",
                      "深沢": "貸出中",
                      "経堂": "貸出可"
                    },
                    "reserveurl": "https://libweb.city.setagaya.tokyo.jp/cgi-bin/detail?NUM=005942406&CTG=1&RTN=01&TM=142142838"
                  },
                  "Kanagawa_Kawasaki": {
                    "status": "OK",
                    "libkey": {
                      "宮前": "貸出可",
                      "麻生": "貸出可",
                      "幸": "貸出可",
                      "中原": "貸出可",
                      "川崎": "貸出可",
                      "大師": "貸出可",
                      "多摩": "貸出可"
                    },
                    "reserveurl": "http://www.library.city.kawasaki.jp/clis/detail?NUM=003059147&CTG=1&RTN=01&TM=142142979"
                  },
                  "Univ_Tamabi": {
                    "status": "OK",
                    "libkey": {},
                    "reserveurl": ""
                  }
            }
          }
        }
        """
        output = []
        if (response.get("books") is not None):
            system_ids = list(set(system_ids))
            for id in system_ids:
                libkeys = response["books"][isbn][id]["libkey"]
                if (len(libkeys) != 0):
                    # print(f"libkeys:{libkeys}")
                    # libkey毎に必要な値をlib_infoから取得する
                    for info in lib_info:
                        # print(f"info:{info}")
                        if (info.get("libkey", "") in libkeys):
                            out_info = {
                                            "libkey":info.get("libkey"),
                                            "formal":info.get("formal"),
                                            "status":libkeys.get(info.get("libkey")),
                                            "address":info.get("address"),
                                            "distance":info.get("distance"),
                                            "uri":f'https://calil.jp/library/{info.get("libid")}/{info.get("formal")}',
                                            "mapuri":f'http://www.google.com/maps?q=%20{info.get("formal")}'
                                        }
                            output.append(out_info)
            # 距離の近い順にsort
            if (len(output) > 0):
                output.sort(key = lambda x: x.get("distance"))
        else:
            pass
        return output

    def polling(self, url):
        while True:
            response = requests.get(url)
            if (response.status_code == 200):
                res = response.text.strip("();")
                res = json.loads(res)
                # res = response.json()
                if (res["continue"] == 0):
                    return res
            time.sleep(1)

if __name__=="__main__":
    test_adapt()
