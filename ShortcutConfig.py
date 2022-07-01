import eel
import threading
import configparser

@eel.expose
def priri(src):
    print(src)

#構成設定ファイルを読み込む
@eel.expose
def sc_conf_reader():
    # ConfigParserのインスタンス（特定の機能を持った変数）を取得
    config = configparser.ConfigParser()

    # 用意したsc_config.iniを読み出し
    config.read("sc_config.ini")
    # 変数configの中から、"sc_conf"セクションの"pose1"から"pose5"までの内容を取得
    cfg_read = [config["sc_conf"]["pose1"],
                config["sc_conf"]["pose2"],
                config["sc_conf"]["pose3"],
                config["sc_conf"]["pose4"],
                config["sc_conf"]["pose5"]]
    #変数の内容を出力
    for num in range(5):
        print(cfg_read[num])

    return cfg_read

@eel.expose
def sc_conf_write(cfg_write):
    # ConfigParserのインスタンス（特定の機能を持った変数）を取得
    config = configparser.ConfigParser()
    # 用意したsc_config.iniを読み出し
    config.read("sc_config.ini")

    # configの各項目に上書き
    config["sc_conf"]["pose1"] = cfg_write[0]
    config["sc_conf"]["pose2"] = cfg_write[1]
    config["sc_conf"]["pose3"] = cfg_write[2]
    config["sc_conf"]["pose4"] = cfg_write[3]
    config["sc_conf"]["pose5"] = cfg_write[4]

    # sc_config.iniファイルに上書き
    with open("sc_config.ini", "w") as file:
        config.write(file)
    for num in range(5):
        print(cfg_write[num])
#ショートカット設定画面"sccon.html"を開く関数
def sc_conf():
    eel.init("assets")
    eel.start("sccon.html", size=(700, 500))


if __name__ == "__main__":
    thread = threading.Thread(target=sc_conf)
    thread.start()
    print("ショートカット設定画面")