# charge_poi
# 利用高德接口web api中的poi搜索获取全国新能源充电站数据
关联：充电桩，充电站，汽车，新能源，地图，坐标，poi

###获取的结果：名称、地点、省、市、区、poi  2021年8月可以获得50000+充电站数据，与实际情况有误差但是不大，5%以内

接口返回的还有其他数据，可根据contest查看

最终结果没放上来，不知道这玩意能不能公开，大家自己爬吧



###接口参数

        'key': '  ',        # 高德web api密钥，需要自己申请 https://lbs.amap.com/
        
        'types':'011100',   # 充电站标签
        
        'city':adcode,      # 区域码
        
        'citylimit':'true', # 只显示本区域数据
        
        'offsest':20,       # 每次返回的数据个数，根据高德文档，每页最多25个
        
        'page':1            # 返回第几页的数据，从1开始，每次只返回该页码的数据
        
    base = 'https://restapi.amap.com/v3/place/text?'    # 接口链接
    
    
### 运行逻辑
1.读取区域编码

2.请求接口，获取该区域数据总量，返回页码参数

3.根据页码参数，再次请求接口，逐页获取数据

4.判断key是否存在，数据添加至list，缺失的属性填充------

5.最后写入文件

接口请求不能太频繁，否则会被封，已经加了sleep



### 区域码说明
直接使用给出的区域码（adcode）会获得重复的数据，因为省份、地级市市会包括下属的区县

且高德接口对于800以上的数据返回有限制，如北京市有几千的充电站，但是请求返回显示只有800多，显然不对，因此使用 区 编码请求数据

对adcode.csv处理，删除省、地级市（00结尾），市辖区（01）结尾的编码，保留了自治区下的01数据，最后得到acode_2.csv
### 高德可能会定期更改adcode编码，如发现获取的数据错误，请及时到高德获取最新编码https://lbs.amap.com/api/webservice/download
