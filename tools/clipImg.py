import time
import os
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pyautogui
import argparse

parser = argparse.ArgumentParser(description="Clip img args.")
parser.add_argument('--label', type=str, help="label")
parser.add_argument('--save_folder_path', default="./Downloads", type=str, help="label")
args = parser.parse_args()

# 函数：点击“Accept”按钮
def click_accept_button():
    try:
        # 定位到Accept按钮并点击
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        accept_button.click()
        print("click Accept button")
    except Exception as e:
        print("unfind Accept button:", e)

# 函数：点击复选框
def click_checkbox():
    checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and contains(@class, 'checkbox')]")
    if not checkbox.is_selected():
        checkbox.click()  # 点击复选框，使其选中

# 函数：上传图片
def upload_image(file_path):
    # 找到“Upload an image”按钮并点击
    upload_button = driver.find_element(By.XPATH, "//button[contains(@class, 'text-blue-700') and contains(@class, 'underline')]")
    upload_button.click()
    
    # 等待文件选择框弹出
    time.sleep(1)
    
    # 使用send_keys来模拟选择文件
    file_input = driver.find_element(By.XPATH, "//input[@type='file']")  # 定位到文件选择框
    file_input.send_keys(file_path)  # 选择文件

def click_close_button():
    close_button = driver.find_element(By.XPATH, "//a[@class='font-bold text-blue-700' and text()='Close']")
    close_button.click()

def click_cutout_button():
    # 定位到包含 'Cut out object' 文本的按钮并点击
    cutout_button = driver.find_element(By.XPATH, "//button[contains(span, 'Cut out object')]")
    cutout_button.click()

# 函数：获取裁剪后的图像的base64数据
def get_cut_image_base64():
    time.sleep(2)
    # 假设裁剪后的图像存储在一个特定的img元素中，找到该元素
    img_element = driver.find_element(By.XPATH, "//img[contains(@src, 'data:image/png;base64,')]")
    img_base64 = img_element.get_attribute('src')
    return img_base64

# 函数：保存Base64图像数据为PNG文件
def save_base64_image(base64_data, output_path):
    # 去掉data:image/png;base64,部分
    image_data = base64_data.split(",")[1]
    with open(output_path, "wb") as img_file:
        img_file.write(base64.b64decode(image_data))

if __name__ == '__main__':

    folder_path = args.save_folder_path
    output_dir = "./object_HD/" + args.label
    url = "https://segment-anything.com/demo"
    load_time = 1

    # Check if directory exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Dir {output_dir} created")
    else:
        print(f"Dir {output_dir} exists")

    chrome_options = Options()
    # chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    time.sleep(load_time)
    click_accept_button()
    time.sleep(load_time)

    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    for i, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        
        # 点击接受协议复选框
        click_checkbox()
        
        # 上传图片
        upload_image(file_path)

        time.sleep(1)
        pyautogui.press('esc')

        input(f"Fig {i}: please clip the img, and press Enter after it\n")

        click_cutout_button()
        time.sleep(1)
        base64_data = get_cut_image_base64()
        output_path = output_dir + '//' + file + ".png"
        save_base64_image(base64_data, output_path)
        print(f"Fig {i} save to {file + '.png'}")
        print("######################################")
        
        driver.refresh()
        time.sleep(load_time)

    driver.quit()