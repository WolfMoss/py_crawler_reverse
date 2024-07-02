from PIL import Image
import numpy as np

def remove_white_background(image_path, output_path):
    # 打开图像并转换为RGBA模式
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # 更改白色背景（可以调整容差）
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))  # 将白色像素变为透明
        else:
            new_data.append(item)

    img.putdata(new_data)

    arr = np.array(img)

    # 获取非透明像素的边界
    non_white_pixels = np.where(arr[:, :, 3] != 0)
    if non_white_pixels[0].size == 0 or non_white_pixels[1].size == 0:
        return None  # 如果没有非白色像素，返回None或其他适当的值

    # 获取边界值
    top, bottom = np.min(non_white_pixels[0]), np.max(non_white_pixels[0])
    left, right = np.min(non_white_pixels[1]), np.max(non_white_pixels[1])

    # 裁剪图像
    cropped_image = img.crop((left, top, right + 1, bottom + 1))


    cropped_image.save(output_path, format="PNG")

    #img.save(output_path, "PNG")

# 示例用法
remove_white_background('下载 (1).jpg', 'output.png')