import requests,json,time,re,datetime,os
import pandas as pd
import http.client,warnings
import pywinauto.clipboard,pywinauto
import win32gui,win32api,win32con
from io import StringIO
import http.client
import talib as ta
import talib.stream

pd.set_option('mode.chained_assignment', None)#屏蔽链式赋值警告
pd.set_option('display.unicode.east_asian_width', True)#设置列名对齐
global app,hwnd,main_window,left_window,button_window_list,edit_windows_list,cang_df
class Hx():
    #初始化
    def __init__(self):
        global app,hwnd,main_window,left_window,button_window_list,edit_windows_list,cang_df
    #关联账号
    def connect(self):
        global app,hwnd,main_window,left_window,button_window_list,edit_windows_list,cang_df
        button_window_list=[];edit_windows_list=[]
        app = pywinauto.application.Application()
        app.connect(title='网上股票交易系统5.0')
        hwnd = win32gui.FindWindow(None,'网上股票交易系统5.0') 
        main_window = app.window(handle=hwnd)
        lefthwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='SysTreeView32', parent=hwnd)[0] 
        left_window = pywinauto.controls.common_controls.TreeViewWrapper(lefthwnd)
        #left_window.get_item([4]).click()
        left_window.select('\\双向委托')
        edit_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Edit', parent=hwnd)#[459868, 594614, 528692]  右侧整个窗口
        button_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Button', parent=hwnd)
        for i in [0,1,4,5]:
            button_window_list.append(pywinauto.controls.win32_controls.ButtonWrapper(button_hwnd[i]))
        for i in range(0,6):
            edit_windows_list.append(pywinauto.controls.win32_controls.EditWrapper(edit_hwnd[i]))
    #获取持仓
    def get_chicang(self):
        global hwnd
        button_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Button', parent=hwnd)
        suanxin_window = pywinauto.controls.common_controls.TreeViewWrapper(button_hwnd[4])
        suanxin_window.click();time.sleep(1)
        cang_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='CVirtualGridCtrl', parent=hwnd)[0] 
        cang_window = pywinauto.controls.common_controls.TreeViewWrapper(cang_hwnd)
        pywinauto.clipboard.EmptyClipboard()
        cang_window.click()
        cang_window.type_keys('^C')
        s=pywinauto.clipboard.GetData().replace('\t',',')
        cang_df = pd.read_csv(StringIO(s),dtype={'证券代码': object,'可用余额':int},usecols=[0,1,2,3,4,5,6,7,8,9,10])
        cang_df.drop(cang_df[cang_df['可用余额'] == 0].index, inplace=True)
        cang_df=cang_df.round(2)
        return cang_df
    #用最新价格更新持仓
    def updata_cang(self,cang_df):
        cang_df = cang_df[~cang_df['证券名称'].str.contains('发债')]
        if cang_df.empty:return cang_df
        temp_list = []
        for code in cang_df['证券代码'].values:
            if code[:2]=='11':code='sh'+code
            else:code='sz'+code
            temp_list.append(self.get_real_data(code)['price'])
        cang_df['市价']=temp_list
        cang_df['盈亏']=(cang_df['市价']-cang_df['成本价'])*cang_df['可用余额']
        cang_df['盈亏比(%)']=round((cang_df['市价']-cang_df['成本价'])/cang_df['成本价']*100,2)
        cang_df['市值']=cang_df['市价']*cang_df['可用余额']
        return cang_df
    #获取资金
    def get_money(self):
        global hwnd,left_window,main_window
        d={}
        left_window.select('\\查询[F4]\\资金股份')
        money_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='CVirtualGridCtrl', parent=hwnd)[1]
        money_window = pywinauto.controls.common_controls.TreeViewWrapper(money_hwnd)
        money_window.click()
        money_window.type_keys('^C')
        s=pywinauto.clipboard.GetData().replace('\t',',').split(',')
        d['资金余额']=float(s[8]);d['可用余额']=float(s[9]);d['总市值']=float(s[10]);d['总资产']=float(s[11])
        left_window.select('\\双向委托')
        main_window.type_keys('{F8}')
        return d
    #获取资金
    def get_kymoney(self):
        global hwnd
        kymoney_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='msctls_statusbar32', parent=hwnd)[0]
        kymoney_window = pywinauto.controls.common_controls.StatusBarWrapper(kymoney_hwnd)
        kymoney = kymoney_window.texts()[5]
        return kymoney
    #异常处理 弹窗
    def close_pop(self):
        global app,hwnd
        time.sleep(0.2)
        temp_list = [];hWndList = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hWndList)
        for item in hWndList:
            clsname = win32gui.GetClassName(item)
            title = win32gui.GetWindowText(item)
            if clsname=='#32770' and title=='':
                temp_list.append(item)
        win32gui.PostMessage(temp_list[1], win32con.WM_CLOSE, 0, 0)
        try:
            pophwnd = win32gui.GetForegroundWindow()
            if pophwnd!=hwnd:
                bpop_hwnd = pywinauto.findwindows.find_windows(top_level_only=False, class_name='Button', parent=pophwnd)
                bp_window = app.window(handle=bpop_hwnd[0]) 
                bp_window.click()
        except:pass
    #买入股票
    def buy(self,code,price,number):
        global edit_windows_list,button_window_list
        edit_windows_list[0].type_keys(code)
        edit_windows_list[1].type_keys(price)
        edit_windows_list[2].type_keys(number)
        button_window_list[0].click()
        self.close_pop()
    #卖出股票
    def sell(self,code,price,number):
        global edit_windows_list,button_window_list
        edit_windows_list[3].type_keys(code)
        edit_windows_list[4].type_keys(price)
        edit_windows_list[5].type_keys(number)
        button_window_list[1].click()
        self.close_pop()
    #刷新
    def shuanxin(self):
        global hwnd,button_window_list
        time.sleep(0.1)
        win32gui.SetForegroundWindow(hwnd) 
        button_window_list[2].click()
        time.sleep(0.1)
        self.close_pop()
    #全部撤单
    def chedan(self):
        global hwnd,button_window_list
        time.sleep(0.1)
        win32gui.SetForegroundWindow(hwnd) 
        button_window_list[3].click()
        time.sleep(0.1)
        self.close_pop()
    #计算当日持仓盈亏比
    def yk_mean(self,cang_df):
        cang_df = cang_df[~cang_df['证券名称'].str.contains('发债')]
        drzf_list=[]
        #cang_df = self.get_chicang()
        for code in cang_df['证券代码'].values:
            if code[:2]=='11':temp_code='sh'+code
            else:temp_code='sz'+code
            data=self.get_real_data(temp_code)
            zf = round((data['price']-data['close'])/data['close']*100,2)
            drzf_list.append(zf)
        cang_df['当日涨幅']=drzf_list
        zf_mean = round(cang_df['当日涨幅'].mean(),2)
        return zf_mean
    #清仓
    def clear_ance(self):
        cang_df = self.get_chicang()
        cang_df = cang_df[~cang_df['证券名称'].str.contains('发债')]
        if cang_df.empty:return
        else:
            for code in cang_df['证券代码'].values:
                self.close_pop()
                if code[:2]=='11':temp_code='sh'+code
                else:temp_code='sz'+code
                data=self.get_real_data(temp_code)
                price=round(data['price']*0.99,2)
                num =int(cang_df.loc[(cang_df[cang_df['证券代码']==code].index)[0]]['可用余额'])
                self.sell(code,price,num)
                time.sleep(0.3)
    #梭哈
    def soha(self,zz_list,n,num_type=10):
        if len(zz_list)>n:zz_list=zz_list[:n]
        money = float(self.get_kymoney())/len(zz_list)
        for code in zz_list:
            if code[2:4]=='13':continue
            self.close_pop()
            price=self.get_real_data(code)['price']
            code=code[2:]
            price = round(price*1.01,2)
            num=int(money//price)//num_type*num_type
            #print(code,price,num)
            if num > 0:
                self.buy(code,price,num)
        time.sleep(0.3)
        self.close_pop()
    #从百度网获取网格时间
    def get_web_time(self):
        host='www.baidu.com'
        conn=http.client.HTTPConnection(host)
        conn.request("GET", "/")
        r=conn.getresponse()
        #r.getheaders() #获取所有的http头
        ts=  r.getheader('date') #获取http头date部分
        #将GMT时间转换成北京时间
        ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
        ttime=time.localtime(time.mktime(ltime)+8*60*60)
        dat="%u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
        tm="%02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
        dt = dat+' '+tm
        return dt
    #从集思录获取可转债信息
    def get_kzz_list(self):
        n=0
        url = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=1606733540803'
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
        while True:
            try:
                response = requests.get(url,headers=headers)
                break
            except:time.sleep(0.5);n+=1
            if n==2:return 0
        res_dict = json.loads(response.text)
        a_list=[];b_list=[];c_list=[];d_list=[];e_list=[];f_list=[];g_list=[];h_list=[];i_list=[];j_list=[];k_list=[];l_list=[];m_list=[]
        stock_list={'转债代码' : a_list,'转债名称' : b_list,'现价' : c_list,'涨跌幅' : d_list,'正股代码' : e_list,'正股名称' : f_list,
        '正股价' : g_list,'正股涨跌' : h_list,'溢价率' : i_list,'剩余年限' : j_list,'成交额' : k_list,'换手率' : l_list,'强赎' : m_list}
        for data in res_dict['rows']:
            a_list.append(data['cell']['pre_bond_id']);b_list.append(data['cell']['bond_nm'])
            c_list.append(data['cell']['price']);d_list.append(data['cell']['increase_rt'][:-1])
            e_list.append(data['cell']['stock_id']);f_list.append(data['cell']['stock_nm'])
            g_list.append(data['cell']['sprice']);h_list.append(data['cell']['sincrease_rt'][:-1])
            i_list.append(data['cell']['premium_rt'][:-1]);j_list.append(data['cell']['year_left'])
            k_list.append(data['cell']['volume']);l_list.append(data['cell']['turnover_rt'])
            m_list.append(data['cell']['force_redeem'])
        data=pd.DataFrame(stock_list)#将字典转换成为数据框
        data = data[data['成交额']!='0.00']
        data[['现价','涨跌幅','正股价','正股涨跌','溢价率','剩余年限','成交额','换手率']]=data[['现价',
                '涨跌幅','正股价','正股涨跌','溢价率','剩余年限','成交额','换手率']].astype('float')
        data['强赎']=data['强赎'].fillna(True)
        data=data[~data['强赎'].str.contains('最后交易日',na=False)]#.contains('最后交易日')]
        data.drop('强赎',axis=1,inplace=True)
        data = data.sort_values(by="涨跌幅",ascending=False)
        data = data[(data['现价']>104) & (data['现价']<400)]
        data = data[(data['涨跌幅']<15) & (data['涨跌幅']>0)]
        data = data.reset_index(drop=True)
        return data

    #获取腾讯实时行情
    def get_real_data(self,code):
        d = {};n=0
        url='http://qt.gtimg.cn/q='+code
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
        while True:
            try:
                response = requests.get(url,headers=headers)
                break
            except:time.sleep(0.5);n+=1
            if n==2:return 0
        html = response.text.split('~')
        d['code'] = code;d['name'] = html[1]
        d['open'] = float(html[5]);d['close'] = float(html[4])
        d['price'] = float(html[3]);d['high'] = float(html[33])
        d['low'] = float(html[34]);d['b_1'] = float(html[9])
        d['s_1'] = float(html[19]);d['vs_1'] = int(html[20])     #20是卖一的量
        d['vb_1'] = int(html[10]);d['dt_price'] = float(html[48])  #跌停价  
        d['zt_price'] = float(html[47]);d['liangbi'] = float(html[49]) #量比
        d['dt']=html[30];d['vol']=html[36]
        return d
    #从新浪获取分时数据
    def get_k_fenshi(self,code,scale=240,len=300):
        url = 'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol='+code+'&scale='+str(scale)+'&ma=no&datalen='+str(len)
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
        response = requests.get(url,headers=headers)
        res_dict = json.loads(response.text)
        a_list=[];b_list=[];c_list=[];d_list=[];e_list=[];f_list=[]
        stock_list={'day' : a_list,'open' : b_list,'high' : c_list,'low' : d_list,'close' : e_list,'volume' : f_list}
        for item in res_dict:
            a_list.append(item['day']);b_list.append(item['open']);c_list.append(item['high'])
            d_list.append(item['low']);e_list.append(item['close']);f_list.append(item['volume']) 
        data=pd.DataFrame(stock_list)
        if scale==240 and self.is_jiaoyi():
            df = self.get_real_data(code)
            temp_d ={}
            temp_d['day']=df['dt'][:4]+'-'+df['dt'][4:6]+'-'+df['dt'][6:8]
            temp_d['open']=df['open'];temp_d['high']=df['high'];temp_d['low']=df['low']
            temp_d['close']=df['price'];temp_d['volume']=df['vol']
            data = data.append(temp_d, ignore_index=True)
        data[['open','high','low','close','volume']]=data[['open','high','low','close','volume']].astype('float')
        macd, macdsignal, macdhist = ta.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        data['dif']=macd;data['dea']=macdsignal;data['macd']=macdhist*2
        # 计算KDJ指标
        low_list=data['low'].rolling(window=9).min()
        high_list = data['high'].rolling(window=9).max()
        rsv = (data['close'] - low_list) / (high_list - low_list) * 100
        data['K'] = rsv.ewm(com=2).mean()
        data['D'] = data['K'].ewm(com=2).mean()
        data['J'] = 3 * data['K'] - 2 * data['D']

        data.dropna(axis = 0,inplace=True)
        data = data.reset_index(drop=True)
        return data
    #用MACD判断买点
    def is_macd(self,code):
        #df = ts.get_k_data(code,autype='qfq')
        df = self.get_k_fenshi(code)
        macd, macdsignal, macdhist = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['DIF']=macd;df['DEA']=macdsignal;df['MACD']=macdhist
        tiao1 = (df['MACD']>df['MACD'].shift()) & (df['MACD'].shift()<df['MACD'].shift(2))
        #tiao2 = df['MACD'].shift(8).rolling(6).min() > 0
        #tiao3 = df['MACD'] < 0
        #tiao4 = df['MACD'].shift().rolling(4).max() < 0
        tiao = tiao1# & tiao2 & tiao3 &tiao4
        df.loc[df[tiao == True].index, 'buy'] = 'y'
        if df.iloc[-1]['buy'] == 'y':
            return True
        else:
            return False
    #KDJ指标J金叉上穿0
    def is_kdj(self,code):
        df = self.get_k_fenshi(code)
        tiao = (df['J']>0) & (df['J'].shift()<0)
        df.loc[df[tiao == True].index, 'buy'] = 'y'
        if df.iloc[-1]['buy'] == 'y':
            return True
        else:
            return False
    #股票交易是否可交易
    def is_jiaoyi(self):
        jjr_list=['2021-01-01','2021-02-11','2021-02-12','2021-02-13','2021-02-14','2021-02-15','2021-02-16','2021-02-17',
                    '2021-04-05','2021-05-01','2021-05-02','2021-05-03','2021-05-04','2021-05-05','2021-06-14','2021-09-20',
                    '2021-09-21','2021-10-01','2021-10-02','2021-10-03','2021-10-04','2021-10-05','2021-10-06','2021-10-07']
        week = [0,1,2,3,4]
        now = str(datetime.datetime.now())#[:10]
        kd_day = now[:10];kd_shi = int(now.replace(':','')[11:17])
        shi_bool = (kd_shi >93000 and kd_shi <113000) or (kd_shi >130000 and kd_shi <150000)
        week_bool = datetime.date.today().weekday() in week
        if (kd_day not in jjr_list) and shi_bool and week_bool:
            return True
        else:
            return False
    #从新浪获取A股列表
    def get_a_list(self):
        url='http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=1&num=10000&sort=changepercent&node=hs_a'
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
        response = requests.get(url,headers=headers)
        res_dict = json.loads(response.text)
        a_list=[];b_list=[];c_list=[];d_list=[];e_list=[];f_list=[];g_list=[];h_list=[];i_list=[];j_list=[];k_list=[];l_list=[];m_list=[];n_list=[]
        stock_list={'symbol' : a_list,'代码' : b_list,'名称' : c_list,'现价' : d_list,'涨跌额' : e_list,'涨跌幅' : f_list,'买入' : g_list,
                '卖出' : h_list,'昨收' : i_list,'今开' : j_list,'最高' : k_list,'最低' : l_list,'成交量' : m_list,'成交额' : n_list}
        for item in res_dict:
            a_list.append(item['symbol']);b_list.append(item['code']);c_list.append(item['name'])
            d_list.append(item['trade']);e_list.append(item['pricechange']);f_list.append(item['changepercent'])
            g_list.append(item['buy']);h_list.append(item['sell']);i_list.append(item['settlement'])
            j_list.append(item['open']);k_list.append(item['high']);l_list.append(item['low'])
            m_list.append(item['volume']);n_list.append(item['amount'])
        data=pd.DataFrame(stock_list)
        data[['现价','涨跌额','涨跌幅','买入','卖出','昨收','今开','最高','最低']]=data[['现价',
            '涨跌幅','涨跌幅','买入','卖出','昨收','今开','最高','最低']].astype('float')
        return data
    #构建股票池
    def build_chi(self):
        df = self.get_a_list()
        temp_list =[];chuang_list=[]
        df = df[(df['涨跌幅']>1) & (df['涨跌幅']<5)]
        for code in df['symbol'].values:
            if code[2:5]=='300':chuang_list.append(code)
        for code in chuang_list:
            try:
                if self.is_kdj(code) and self.is_macd(code):
                    temp_list.append(code)
            except:pass
        return temp_list

