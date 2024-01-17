import copy

import cv2
import mediapipe as mp
import time
import math
import config as cfg

figure_index = cfg.figure_index
figure_size = cfg.figure_size
widgets = cfg.widgets
widget_pos = cfg.widget_pos
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.8, trackCon=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        model_complexity = 1
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, model_complexity,self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, frame, draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #print(self.results.multi_handedness)  # 获取检测结果中的左右手标签并打印

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    #print()
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    self.lmList.append([id, cx, cy])
                    #if draw:
                        #print()

                        #cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def fingersUp(self):
        fingers = []
        # 大拇指
        if self.lmList[self.tipIds[0]][2] < self.lmList[self.tipIds[0] - 1][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 其余手指
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)        # 检测手势并画上骨架信息

        lmList = detector.findPosition(img)  # 获取得到坐标点的列表
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, 'fps:' + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)

def interface(img, overlayList, state):
    '''

    :param img: 720 * 1280 *3
    :param overlayList: list size 34
    :param state: state of ai painter
    :return: img
    '''
    img_new = copy.deepcopy(img)
    def draw_area(a, b, c, d, value, img_new):
        '''

        :param a: upper bound
        :param b: lower bound
        :param c: left bound
        :param d: right bound
        :param value: name of wedget
        :return: img
        '''

        img_new[a:b, c:d, :] = overlayList[figure_index[value]]
        return img_new
    #print(state)
    for widget in widgets[state]:
        #print(widget)
        upper_bound, left_bound = widget_pos[widget]
        img_new = draw_area(upper_bound, upper_bound + figure_size[widget][0], left_bound, left_bound + figure_size[widget][1],
                             widget, img_new)
    return img_new

if __name__ == "__main__":
    main()
