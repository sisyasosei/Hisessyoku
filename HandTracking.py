import cv2
import time
import math
import eel
import pyautogui
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# 2頂点の距離の計算
def calcDistance(p0, p1):
  a1 = p1.x-p0.x
  a2 = p1.y-p0.y
  return math.sqrt(a1*a1 + a2*a2)


# 3頂点の角度の計算
def calcAngle(p0, p1, p2):
  a1 = p1.x-p0.x
  a2 = p1.y-p0.y
  b1 = p2.x-p1.x
  b2 = p2.y-p1.y
  angle = math.acos( (a1*b1 + a2*b2) / math.sqrt((a1*a1 + a2*a2)*(b1*b1 + b2*b2)) ) * 180/math.pi
  return angle


# 指の角度の合計の計算
def cancFingerAngle(p0, p1, p2, p3, p4):
  result = 0
  result += calcAngle(p0, p1, p2)
  result += calcAngle(p1, p2, p3)
  result += calcAngle(p2, p3, p4)
  return result


# 指ポーズの検出
def detectFingerPose(landmarks):
  # 指のオープン・クローズ
  thumbIsOpen = cancFingerAngle(landmarks[0], landmarks[1], landmarks[2], landmarks[3], landmarks[4]) < 70
  firstFingerIsOpen = cancFingerAngle(landmarks[0], landmarks[5], landmarks[6], landmarks[7], landmarks[8]) < 100
  secondFingerIsOpen = cancFingerAngle(landmarks[0], landmarks[9], landmarks[10], landmarks[11], landmarks[12]) < 100
  thirdFingerIsOpen = cancFingerAngle(landmarks[0], landmarks[13], landmarks[14], landmarks[15], landmarks[16]) < 100
  fourthFingerIsOpen = cancFingerAngle(landmarks[0], landmarks[17], landmarks[18], landmarks[19], landmarks[20]) < 100

  # ジェスチャー
  if (calcDistance(landmarks[4], landmarks[8]) < 0.06 and not secondFingerIsOpen and not thirdFingerIsOpen and not fourthFingerIsOpen):
      return "OK"
  elif (calcDistance(landmarks[4], landmarks[12]) < 0.1 and calcDistance(landmarks[4], landmarks[16]) < 0.1 and firstFingerIsOpen and fourthFingerIsOpen):
      return "キツネ"
  elif (thumbIsOpen and not firstFingerIsOpen and not secondFingerIsOpen and not thirdFingerIsOpen and not fourthFingerIsOpen):
      return "いいね"
  elif (thumbIsOpen and firstFingerIsOpen and secondFingerIsOpen and thirdFingerIsOpen and fourthFingerIsOpen):
      return "５"
  elif (not thumbIsOpen and firstFingerIsOpen and secondFingerIsOpen and thirdFingerIsOpen and fourthFingerIsOpen):
      return "４"
  elif (not thumbIsOpen and firstFingerIsOpen and secondFingerIsOpen and thirdFingerIsOpen and not fourthFingerIsOpen):
      return "３"
  elif (not thumbIsOpen and firstFingerIsOpen and secondFingerIsOpen and not thirdFingerIsOpen and not fourthFingerIsOpen):
      return "２"
  elif (not calcDistance(landmarks[4], landmarks[8]) < 0.1 and not thumbIsOpen and firstFingerIsOpen and not secondFingerIsOpen and not thirdFingerIsOpen and not fourthFingerIsOpen):
      return "１"

  return "０"


def hand_tracking():
  #グローバル変数FLGで起動・停止の条件分岐を行う
  global FLG
  FLG = None
  # ウェブカメラ入力用
  cap = cv2.VideoCapture(0)
  with mp_hands.Hands(
          min_detection_confidence=0.5,
          min_tracking_confidence=0.5) as hands:
    while cap.isOpened():

      if FLG == False:
        break

      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # ビデオをロードする場合は、「続行」ではなく「中断」を使用
        continue

      # 後で自分撮りビューを表示するために画像を水平方向に反転し、変換
      # BGR画像をRGBに変換
      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
      image = cv2.resize(image, dsize=(480, 270), dst=image, fx=0, fy=0, interpolation=cv2.INTER_NEAREST)
      # パフォーマンスを向上させるには、オプションで画像を書き込み不可としてマーク
      # 参照渡し
      image.flags.writeable = False
      results = hands.process(image)

      # 画像に手の注釈を描画
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

          #image = cv2.flip(image, 1)  # ミラー表示
          #image_width, image_height = image.shape[1], image.shape[0]
          image_width, image_height = 1919, 1079

          # 人差し指(指先)の座標値(x,y)をカメラでキャプチャした画像に合わせる
          index_finger_tip_x = int(hand_landmarks.landmark[8].x * image_width)
          index_finger_tip_y = int(hand_landmarks.landmark[8].y * image_height)

          # 人差し指(第二関節)の座標値(x,y)をカメラでキャプチャした画像に合わせる
          index_finger_pip_x = int(hand_landmarks.landmark[6].x * image_width)
          index_finger_pip_y = int(hand_landmarks.landmark[6].y * image_height)

          # landmark_subsetに関節の座標情報を持たせる
          landmark_subset = hand_landmarks.landmark
          # 関節の座標を引数にポーズを判定する関数を実行、返り値をposeに格納
          pose = detectFingerPose(landmark_subset)

          """
          # 人差し指を曲げたとき、クリックをする
          if index_finger_tip_y > index_finger_pip_y:
            pyautogui.click(index_finger_pip_x, index_finger_pip_y)
            time.sleep(1)
          """
          if pose == "OK":
            pyautogui.click(index_finger_pip_x, index_finger_pip_y)
            time.sleep(1)
          # クリックでない時、ポーズを判定する関数の返り値をもとに、ポーズごとのイベントを呼び出す
          elif pose == "キツネ":
            # jsの関数からポーズに割り当てられたショートカットの番号を取得
            print("てすとおきつね")
          elif pose == "４":
            print("テスト４")
          elif pose == "３":
            print("テスト３")
          elif pose == "２":
            print("テスト２")
          elif pose == "１":
            pyautogui.moveTo(index_finger_pip_x, index_finger_pip_y)
            #print("カーソル移動")

          # 上記外は、カーソルを移動させる
          """
          else:
            pyautogui.moveTo(index_finger_pip_x, index_finger_pip_y)
          """

      cv2.imshow('MediaPipe Hands', image)
      if cv2.waitKey(5) and 0xFF == 27:
        break

  cap.release()