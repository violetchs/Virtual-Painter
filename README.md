# Virtual-Painter
## 1. Description
This project builds a frame to run virtual painter (**VP**) on PC with a camera. 

Users can perform gestures or microgestures to interact with VP to draw a picture on the real world.
## 2. Instruction
You should run VP in a environment with `python==3.9`.

**COPY** the whole project into the root folder of you environment. That means the project and your environment are included in the same directory.
### 1. Requarments
Make sure packages below are installed in your environment.

```
numpy==1.26.2
opencv-python==4.8.1.78
mediapipe==0.10.9
```
### 2. How to paint
You can read instructions below to learn performing gestures to interact with VP.
* Function Selection
  
  VP has 3 main functions :**draw**, **select bbox**, **eraser**.
  >In draw, you can draw a picture.
  >
  >In select bbox, you can copy the content of the region into target region or delete it.
  >
  >In eraser, you can erase the existing content.
  
  Perform gestures as [function selection](https://www.bilibili.com/video/BV1eW4y1w71t/).
* Main Task

  To use 3 functions, perform gestures as [Pen up Pen down](https://www.bilibili.com/video/BV1K94y1K7DD/?vd_source=cd0764e6da97a83655f4eafba9e5abe6).
* Auxiliary Task

  To adjust the thickness of the painter/eraser or change the color, perform gestures as [microgestures]().
### 3. Start Painting
Run `python AiVirtualPainter.py` in the terminal to start.
Make sure your hand **50cm~60cm** away from camera!
## 3. Materials
A more detailed example video [here](https://www.bilibili.com/video/BV1zw4117781/).
