import os
from PIL import Image
import argparse
from tqdm import tqdm

print("This code is for rename the pic and transfer the pic to target.")

parser = argparse.ArgumentParser(description="Renaming PNG files starting from a specified number.")
parser.add_argument('--sn', default=0, type=int, help="The number to start renaming from")
parser.add_argument('--zfill', default=4, type=int, help="The number to zfill index")
parser.add_argument('--resolution', default=224, type=int, help="Transfer HD img to this resolution")
parser.add_argument('--source_dir', default='./object_HD/', type=str, help="source dir of HD img")
args = parser.parse_args()

folders = [args.source_dir+f for f in os.listdir(args.source_dir) if os.path.isdir(args.source_dir+f)]
print(os.listdir(args.source_dir))

for folder in tqdm(folders, desc="Renaming..."):
    png_files = [f for f in os.listdir(folder) if f.endswith('.png')]

    png_files.sort()

    for i, file in enumerate(png_files, start=args.sn):
        file_extension = os.path.splitext(file)[1]
        new_name = f"{str(i).zfill(args.zfill)}{file_extension}"
        old_file_path = os.path.join(folder, file)
        new_file_path = os.path.join(folder, new_name)
        os.rename(old_file_path, new_file_path)
        # print(f"Renamed: {old_file_path} -> {new_file_path}")

    args.sn += 100

print("All files have been renamed successfully.")

source_dir = args.source_dir
output_dir = f'./object_{args.resolution}'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历 object_HD 下的所有子文件夹
for subdir, dirs, files in tqdm(os.walk(source_dir), desc=f"Change resolution to {args.resolution}..."):
    for file in files:
        if file.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
            
            img_path = os.path.join(subdir, file)
            img = Image.open(img_path)

            width, height = img.size
            max_size = args.resolution
            if width > height:
                new_width = max_size
                new_height = int((max_size / width) * height)
            else:
                new_height = max_size
                new_width = int((max_size / height) * width)

            # 调整图片大小
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 保存调整后的图片到目标文件夹，保留子文件夹结构
            # 计算相对路径
            relative_path = os.path.relpath(subdir, source_dir)
            target_subdir = os.path.join(output_dir, relative_path)

            # 确保目标子文件夹存在
            if not os.path.exists(target_subdir):
                os.makedirs(target_subdir)

            # 保存图片
            target_path = os.path.join(target_subdir, file)
            img_resized.save(target_path)

print(f"Transfer HD img to {args.resolution} successfully.")
