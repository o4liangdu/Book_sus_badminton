import requests
import time

def book(date, timeList=['09:01-10:00', '10:01-11:00'], jsessionid=""):
    # 调用获取场地库存接口
    result = queryPlace(date)
    # print(result)
    # 定场接口选定的两个场信息
    placeList = []
    isChose1 = False
    isChose2 = False
    for item in result:
        if item.get("time")==timeList[0] and not isChose1:
            print("开始定")
            print(item.get("sname"))
            print(item.get("time"))
            placeList.append(item)
            isChose1 = True
        if item.get("time")==timeList[1] and not isChose2:
            print("开始定")
            print(item.get("sname"))
            print(item.get("time"))
            placeList.append(item)
            isChose2 = True
    resultMsg = ""
    try:
        # 调用接口获取orderid
        orderId = getOrderId(placeList, jsessionid)
        # 调用接口下单
        resultMsg = order(orderId, jsessionid)
    except:
        pass
    return resultMsg

# 下单接口
def order(orderId, jsessionid):
    headers= {"Accept":"application/json, text/javascript, */*; q=0.01","Cookie": "from=undefined; from=undefined; JSESSIONID="+jsessionid, "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Host":"gym.sysu.edu.cn","Origin":"http://gym.sysu.edu.cn","Referer":"http://gym.sysu.edu.cn/order/show.html?id=61","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    params = r"param=%7B%22payid%22%3A2%2C%22orderid%22%3A%22"+str(orderId)+r"%22%2C%22ctypeindex%22%3A0%7D&json=true"
    res = requests.post("http://gym.sysu.edu.cn/pay/account/topay.html", headers=headers,data= params).json()
    print(res["message"])
    return res["message"]

# 选好场地后调用接口获得orderid
def getOrderId(placeList, jsessionid):
    headers= {"Accept":"application/json, text/javascript, */*; q=0.01","Cookie": "from=undefined; from=undefined; JSESSIONID="+jsessionid, "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Host":"gym.sysu.edu.cn","Origin":"http://gym.sysu.edu.cn","Referer":"http://gym.sysu.edu.cn/order/show.html?id=61","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    params = r"param=%7B%22activityPrice%22%3A0%2C%22activityStr%22%3Anull%2C%22address%22%3Anull%2C%22dates%22%3Anull%2C%22extend%22%3Anull%2C%22flag%22%3A%220%22%2C%22isBulkBooking%22%3Anull%2C%22isbookall%22%3A%220%22%2C%22isfreeman%22%3A%220%22%2C%22istimes%22%3A%221%22%2C%22mercacc%22%3Anull%2C%22merccode%22%3Anull%2C%22order%22%3Anull%2C%22orderfrom%22%3Anull%2C%22remark%22%3Anull%2C%22serviceid%22%3Anull%2C%22shoppingcart%22%3A%220%22%2C%22sno%22%3Anull%2C%22stock%22%3A%7B%22"+str(placeList[0].get("stockid"))+r"%22%3A%221%22%2C%22"+str(placeList[1].get("stockid"))+r"%22%3A%221%22%7D%2C%22stockdetail%22%3A%7B%22"+str(placeList[0].get("stockid"))+r"%22%3A%22"+str(placeList[0].get("id"))+r"%22%2C%22"+str(placeList[1].get("stockid"))+r"%22%3A%22"+str(placeList[1].get("id"))+r"%22%7D%2C%22stockdetailids%22%3A%22"+str(placeList[0].get("id"))+r"%2C"+str(placeList[1].get("id"))+r"%22%2C%22stockid%22%3Anull%2C%22subscriber%22%3A%220%22%2C%22time_detailnames%22%3Anull%2C%22userBean%22%3Anull%7D&json=true"
    res = requests.post("http://gym.sysu.edu.cn/order/book.html", headers=headers,data= params).json()
    if hasattr(res["object"], "orderid"):
        print(res["object"]["orderid"])
        return res["object"]["orderid"]
    else:
        return ""


# 调用场地接口
def queryPlace(date):
    res = requests.get("http://gym.sysu.edu.cn/product/findOkArea.html?s_date="+ date + "&serviceid=61&_=1616945522222").json().get("object")
    return list(filter(isAvailable, list(map(formatAllData, res))))

# 整理所有场地列表
def formatAllData(data):
    return {"sname": data.get("sname"), "time": data.get("stock").get("time_no"), "status": data.get("status"), "id": data.get("id"), "stockid": data.get("stockid")}

# 过滤可用场地的函数
def isAvailable(data):
    return data.get("status")==1

resultMsg = ""
while True:  # 进入一个无限循环，一直判断是否到达预定时间
    now = time.strftime('%H:%M:%S',time.localtime(time.time()))
    print(now)
    # if(now == "21:58:20"):
    if(now == "06:00:00"):
        while not resultMsg == "支付成功":
            # book函数的第一个参数为想要打球的日期，第二个参数是想要打球的时间点列表（注意格式），第三个参数为登录的cookie信息（登陆后打开开发者工具可查看cookie，复制jsession=后面的一串乱码）
            resultMsg = book("2021-04-03", ['19:01-20:00', '20:01-21:00'],"83D52D9CAEB77BB9835CB5E715FB2049")
        # 超时时间60秒
        time.sleep(60)
        break
