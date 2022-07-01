import eel
import threading
import HandTracking
from HandTracking import hand_tracking
from ShortcutConfig import sc_conf

#   起動ボタンを押下した際に、"main.html"で呼び出される関数
@eel.expose
def boot_app():
    #   スレッドを新しく呼び出し、メインウィンドウと同時に、ハンドトラッキングを開始
    thread = threading.Thread(target=hand_tracking)
    thread.start()
    print("ハンドトラッキングを開始します")

#   停止ボタンを押下した際に、"main.html"で呼び出される関数
@eel.expose
def stop_app():
    #   ハンドトラッキングを終了
    #   hand_tracking関数内のグローバル変数FLGをfalseにし、処理を終了させる
    HandTracking.FLG = False
    print("ハンドトラッキングを停止します")

#   ショートカット設定ボタンを押下した際に、"main.html"で呼び出される関数
@eel.expose
def scconf_app():
    thread = threading.Thread(target=sc_conf)
    thread.start()
    print("ショートカット設定画面を開きます")

#   "main.html"を呼び出す関数
def main():
    eel.init("assets")
    eel.start("main.html", size=(700, 450))


if __name__ == "__main__":
    main()