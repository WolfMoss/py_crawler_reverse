from paddleocr import PaddleOCR, draw_ocr
import time
# 创建OCR对象，默认使用英文和中文
ocr = PaddleOCR()

# 这里是你的函数，例如 ocr.ocr("屏幕截图 2024-05-22 151713.png")
start_time = time.time()
print("开始执行函数", start_time)
result = ocr.ocr("微信图片_20240522143521.png")
end_time = time.time()
execution_time = end_time - start_time
print(f"函数执行时间: {execution_time}秒")

# 打印结果
for line in result:
    print(line)