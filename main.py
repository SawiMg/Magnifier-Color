import cv2
import numpy as np
import pyautogui
from PIL import Image

magnified_width = 100  # 放大区域的宽度
magnified_height = 100  # 放大区域的高度
scale_factor = 4  # 放大倍数
font_scale = 0.7  # 文字比例因子
font_thickness = 1  # 文字线条粗细
dot_radius = 1  # 定位点半径

recorded_positions = []  # 存储记录的鼠标位置和颜色
hex_color = None


class Magnifier:
    def __init__(self):
        self.magnified_image = None
        self.window_name = 'Magnifier'
        self.is_window_closed = False

    def update_magnifier(self, x, y):
        global hex_color
        magnified_x = x - int(magnified_width / 2)
        magnified_y = y - int(magnified_height / 2)
        magnified_image = pyautogui.screenshot(region=(magnified_x, magnified_y,
                                                       magnified_width, magnified_height))
        magnified_image = magnified_image.resize((magnified_width * scale_factor,
                                                  magnified_height * scale_factor),
                                                 resample=Image.BICUBIC)

        # 获取鼠标位置的像素颜色
        pixel_color = pyautogui.pixel(x, y)
        hex_color = '#{0:02x}{1:02x}{2:02x}'.format(pixel_color[0], pixel_color[1], pixel_color[2])

        # 在放大镜窗口中显示鼠标位置和像素颜色
        cv2_image = cv2.cvtColor(np.array(magnified_image), cv2.COLOR_RGB2BGR)
        cv2.putText(cv2_image, f'Position: ({x}, {y})', (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, (255, 255, 255), font_thickness)
        cv2.putText(cv2_image, f'Color: {hex_color}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, (255, 255, 255), font_thickness)

        # 在放大镜窗口中添加定位点
        cv2.circle(cv2_image, (int(cv2_image.shape[1] / 2), int(cv2_image.shape[0] / 2)),
                   dot_radius, (0, 255, 0), -1)

        cv2.imshow(self.window_name, cv2_image)

    def start(self):
        global hex_color
        # 创建放大镜窗口
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)  # 置顶窗口

        while not self.is_window_closed:
            x, y = pyautogui.position()
            self.update_magnifier(x, y)

            key = cv2.waitKey(1)
            if key == ord('q'):
                recorded_positions.append((x, y, pyautogui.pixel(x, y)))
                print(f"Recorded position: ({x}, {y}), f'Color: {hex_color}'")
            elif key == 27:  # 按下 "ESC" 键
                self.is_window_closed = True

        cv2.destroyAllWindows()


# 创建放大镜对象
magnifier = Magnifier()

# 启动放大镜
magnifier.start()
