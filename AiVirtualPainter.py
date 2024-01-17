import copy

import cv2
import HandTrackingModule as htm
import os
import numpy as np

import config

folderPath = "PainterImg/"
mylist = os.listdir(folderPath)
overlayList = []

for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

color_list = [[255, 0, 0], [255, 165, 0],
              [255, 255, 0], [0, 128, 0], [0, 255, 255],
              [0, 0, 255], [128, 0, 128], [255, 255, 255],
              [255, 192, 203]]
color_index = 0
color_remain_time = 0
color = color_list[color_index]

brushThickness_max = 30
rate = 0.5
brushThickness = int(rate * brushThickness_max)

eraserThickness_max = 40
rate2 = 0.5
eraserThickness = int(rate2 * eraserThickness_max)

cap = cv2.VideoCapture(0)  # 若使用笔记本自带摄像头则编号为0  若使用外接摄像头 则更改为1或其他编号
cap.set(3, 1280)
cap.set(4, 720)
# cap.set(3, 800)
# cap.set(4, 500)
detector = htm.handDetector()
tipid = detector.tipIds
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # 新建一个画板
# imgCanvas = np.zeros((500, 800, 3), np.uint8)  # 新建一个画板
state = 'base'
gesture = None
mod = None
draw_state = None
area = config.area
cutting = 'before_cut'
start_point = None
end_point = None
clear_cut = None

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 13.0, (1280, 720))

while True:
    # 1.import image
    success, img = cap.read()
    if type(img) == 'None':
        continue
    frame = cv2.flip(img, 1)  # 翻转
    img = htm.interface(frame, overlayList, state)
    # 2.find hand landmarks
    img = detector.findHands(img, frame)

    lmList = detector.findPosition(img, draw=True)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  #index finger position
        x2, y2 = lmList[12][1:] #mid finger position
        x3, y3 = lmList[4][1:]  #thumb position
        x4 = int((x1 + x3)/2)
        y4 = int((y1 + y3)/2)
        # 3. Check which fingers are up

        in_out_area = lambda x1, y1, a : x1 > a[1][0] and x1 < a[1][1] and y1 > a[0][0] and y1 < a[0][1]
        fingers = detector.fingersUp()
        if lmList[tipid[0]][1] < lmList[tipid[0]-2][1] - 15: #
                # hold on
            if in_out_area(x1, y1, area['small_painter']):
                if state == 'select_painter':
                    mod = 'draw'
                state = 'hold_painter'

            elif in_out_area(x1, y1, area['small_indicator']):
                if state == 'select_indicator':
                    mod = 'cut_copy'
                state = 'hold_indicator'

            elif in_out_area(x1, y1, area['small_eraser']):
                if state == 'select_eraser':
                    mod = 'eraser'
                state = 'hold_eraser'

            print('hold on')
        else:
                # select
            gesture = 'select'

            if in_out_area(x1, y1, area['big_painter']):
                state = 'select_painter'

            elif in_out_area(x1, y1, area['big_indicator']):
                state = 'select_indicator'

            elif in_out_area(x1, y1, area['big_eraser']):
                state = 'select_eraser'

            print('select')
        if mod == 'draw':

            if not in_out_area(x1, y1, area['base_toolbox']):

                cv2.circle(img, (x4, y4), brushThickness, color, cv2.FILLED)
                if abs(x1 - x3) <30 and abs(y1 - y3) <30: # 判断距离影响绘画效果 食指头和拇指头捏在一起
                    draw_state = 'pen_down'
                    print('pen down')
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    if color == [0, 0, 0]:
                        cv2.line(img, (xp, yp), (x4, y4), color, eraserThickness)  # ??
                        cv2.line(imgCanvas, (xp, yp), (x4, y4), color, eraserThickness)
                    else:
                        cv2.line(img, (xp, yp), (x4, y4), color, brushThickness)  # ??
                        cv2.line(imgCanvas, (xp, yp), (x4, y4), color, brushThickness)

                else:
                    print('pen up')
                    if lmList[tipid[0]-2][1] - lmList[tipid[0]][1] < 15 and lmList[7][2] - lmList[8][2] > 20\
                            and lmList[6][2] - lmList[7][2] > 20: #食指向上伸直、拇指向食指靠拢、虎口捏紧
                        draw_state = 'pen_up_linethickness'
                        y_index_sec = lmList[6][2]
                        limit = max(abs(y_index_sec - y1), 1)
                        pos = min(max(y2 - y1, 1), limit)
                        rat = pos/limit
                        brushThickness = max(int(brushThickness_max * rat), 1)

                    elif lmList[12][2] - lmList[10][2] > 10 and lmList[16][2] - lmList[14][2] > 10:
                        if lmList[18][2] - lmList[20][2] > 10:
                            draw_state = 'pen_up_rest'
                        else:
                            pinky_x1 = lmList[20][1]
                            pinky_y1 = lmList[20][2]
                            pinky_x2 = lmList[18][1]
                            pinky_y2 = lmList[18][2]
                            if  pinky_y1-pinky_y2>0:

                                if draw_state == 'pen_up_rest':
                                    color_index = color_index + 1
                                    if color_index > 8 :
                                        color_index = 0
                                    color = color_list[color_index]
                                    draw_state = 'pen_up_color'
                            else:
                                draw_state = 'pen_up_rest'
                    else:
                        draw_state = 'pen_up_rest'
                xp, yp = x4, y4
        elif mod == 'cut_copy':
            if abs(x1 - x3) < 30 and abs(y1 - y3) < 30:
                cv2.circle(img, (x4, y4), brushThickness, color, cv2.FILLED)
                if cutting == 'before_cut' or cutting == 'after_cut':
                    start_point = [x4, y4]
                    cutting = 'cut'
            else:
                if cutting == 'cut':
                    end_point = [x4, y4]
                    x_l = start_point[0]
                    x_r = end_point[0]
                    y_u = start_point[1]
                    y_b = end_point[1]
                    if x_r < x_l :
                        x_r, x_l = x_l, x_r
                    if y_b < y_u :
                        y_u, y_b = y_b, y_u
                    start_point = [x_l, y_u]
                    end_point = [x_r, y_b]

                    cutting = 'after_cut'
                if cutting == 'after_cut':
                    rtop = [end_point[0], start_point[1]]
                    lbottom = [start_point[0], end_point[1]]
                    cv2.line(img, start_point, rtop, [255, 255, 255], 10)
                    cv2.line(img, start_point, lbottom, [255, 255, 255], 10)
                    cv2.line(img, lbottom, end_point, [255, 255, 255], 10)
                    cv2.line(img, rtop, end_point, [255, 255, 255], 10)


            if lmList[12][2] - lmList[10][2] > 10 and lmList[16][2] - lmList[14][2] > 10 and cutting=='after_cut':

                if lmList[18][2] - lmList[20][2] > 10 :
                    clear_cut = 'rest'
                elif lmList[20][2] - lmList[18][2] > 10 and clear_cut == 'rest':
                    clear_cut = 'clear'
                    cutting = 'before_cut'
                    zeros = np.zeros((end_point[1]-start_point[1], end_point[0]-start_point[0], 3))
                    imgCanvas[start_point[1]:end_point[1], start_point[0]:end_point[0], :] = zeros

            if  lmList[tipid[0]-2][1] - lmList[tipid[0]][1] < 15 and lmList[7][2] - lmList[8][2] > 20\
                            and lmList[6][2] - lmList[7][2] > 20 and cutting == 'after_cut':
                length = end_point[0] - start_point[0]
                height = end_point[1] - start_point[1]
                length_max = 1280 - x1
                height_max = 720 - y1
                length = min(length, length_max)
                height = min(height, height_max)
                imgCanvas_copy = copy.deepcopy(imgCanvas)
                imgCanvas_copy[y1:y1+height, x1:x1+length, :] = cv2.bitwise_or(imgCanvas[start_point[1]:start_point[1]+height, start_point[0]:start_point[0]+length, :],
                                                                               imgCanvas_copy[y1:y1+height, x1:x1+length, :])
                imgCanvas = imgCanvas_copy
                cutting = 'before_cut'

        elif mod == 'eraser':
            if not in_out_area(x1, y1, area['base_toolbox']):

                cv2.circle(img, (x4, y4), eraserThickness, [0, 0, 0], cv2.FILLED)
                if abs(x1 - x3) <30 and abs(y1 - y3) <30: # 判断距离影响绘画效果 食指头和拇指头捏在一起
                    print('eraser_down')
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    cv2.line(img, (xp, yp), (x4, y4), [0, 0, 0], eraserThickness)  # ??
                    cv2.line(imgCanvas, (xp, yp), (x4, y4), [0, 0, 0], eraserThickness)
                else:
                    print('eraser up')
                    if lmList[tipid[0] - 2][1] - lmList[tipid[0]][1] < 15 and lmList[7][2] - lmList[8][2] > 20 \
                            and lmList[6][2] - lmList[7][2] > 20:  # 食指向上伸直、拇指向食指靠拢、虎口捏紧
                        y_index_sec = lmList[6][2]
                        limit = max(abs(y_index_sec - y1), 1)
                        pos = min(max(y2 - y1, 1), limit)
                        rat = pos / limit
                        eraserThickness = max(int(eraserThickness_max * rat), 1)
                xp, yp = x4, y4
        # 4. If Selection Mode – Two finger are up

        '''if y1 < 153:
            if 0 < x1 < 320:
                header = overlayList[0]
                color = [50, 128, 250]
            elif 320 < x1 < 640:
                header = overlayList[1]
                color = [0, 0, 255]
            elif 640 < x1 < 960:
                header = overlayList[2]
                color = [0, 255, 0]
            elif 960 < x1 < 1280:
                header = overlayList[3]
                color = [0, 0, 0]'''

        # 5. If Drawing Mode – Index finger is up
        '''if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
            print("Drawing Mode")
            
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if color == [0, 0, 0]:
                cv2.line(img, (xp, yp), (x1, y1), color, eraserThickness)  # ??
                cv2.line(imgCanvas, (xp, yp), (x1, y1), color, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), color, brushThickness)   # ??
                cv2.line(imgCanvas, (xp, yp), (x1, y1), color, brushThickness)

        xp, yp = x1, y1'''
        # Clear Canvas when all fingers are up
        # if all (x >= 1 for x in fingers):
        #     imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    # 实时显示画笔轨迹的实现
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)
    out.write(img)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)
