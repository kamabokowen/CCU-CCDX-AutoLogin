import time
import requests
from pydub import AudioSegment
from pydub.playback import play

count_ex_num = 0
how_long_loop = 10





# 以下这段是为了模拟登录行为，发送登录数据包
def login():
    print (get_time_now(),"开始提交登录信息......")
    url="http://1.1.1.2/ac_portal/login.php"
    headers={
        'Host': '1.1.1.2',
        'Connection': 'keep-alive',
        'Content-Length':'63',
        'Accept': '*/*',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin':'http://1.1.1.2',
        'Referer': 'http://1.1.1.2/ac_portal/20180507163215/pc.html?template=20180507163215&tabs=pwd&vlanid=1026',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    userdata={
        'opr': 'pwdLogin',
        'userName' : '0431113364697691',
        'pwd': '110614',
        'rememberPwd': '0'
    }
    try:
        r=requests.post(url,headers=headers,data=userdata)
        print (get_time_now(),' 登录成功.现在开始测试连接')
        login_ok = AudioSegment.from_mp3("login_ok.mp3")
        play(login_ok)
    except:
        print("===发生错误，这是意料外情况,错误点在于 提交登录信息===")
        login_err = AudioSegment.from_mp3("loginerr.mp3")
        play(login_err)


# 以下这段是为了判断是否联网，等待返回204状态码
def Connect_able():
    q=requests.get("http://g.cn/generate_204")
    if(q.status_code==204):
        return True
    else:
        return False

# 以下这段是把获取当前时间封装起来
def get_time_now():
    return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

#以下这段函数是为了把重连信息推送给Server酱，进行微信通知
def push_to_server_chan():
    api = "https://sc.ftqq.com/SCU88241T88c1f10c0abc9b152f32d19bb2e2dc735e62598e1a8da.send"
    title = "612的路由器校园网发生了断网重连"
    content = "主人，刚刚检测到您在612寝室的路由器连接的校园网断开了，我已经在"+get_time_now()+"进行了重连，您收到了消息就代表重连成功了哦。"
    data = {
        "text" : title,
        "desp" : content
        }
    req = requests.post(api,data = data)

def main():
    print(get_time_now(),"CCDX校园网自动登录脚本开始运行了......")
    start_au = AudioSegment.from_mp3("F:\CCDX_Auto_Login\start.mp3")
    play(start_au)
    while True:
        count_ex_num = count_ex_num + 1
        while True:
            connectable = Connect_able()
            if not connectable:
                print(get_time_now(),"检测到网络断开，开始尝试重连......")
                net_off_au = AudioSegment.from_mp3("netoff.mp3")
                play(net_off_au)
                try:
                    login()
                except:
                    print(get_time_now(), "===发生错误，这是意料外情况,错误点在于 执行登录函数===")
                    login_fx_err = AudioSegment.from_mp3("loginfunctionerr.mp3")
                    play(login_fx_err)

                finally:
                    time.sleep(2)
                    if Connect_able():
                        print(get_time_now(),"网络重连成功了。")
                        all_ok = AudioSegment.from_mp3("all_ok_wechat.mp3")
                        play(all_ok)
                        push_to_server_chan()
                        print(get_time_now(),"已经把重连微信推送给Server酱")
                    else:
                        print(get_time_now(),"登录失败了，下个循环会再试的。")
            else:
                print(get_time_now(),"本次检测一切正常，这是第",count_ex_num," 次检测")
                time.sleep(5)
            time.sleep(1)
        time.sleep(how_long_loop)
if __name__ == '__main__':
    main()