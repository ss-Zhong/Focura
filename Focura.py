from torchvision.datasets.folder import ImageFolder
import random
import os
from PIL import Image

class Focura(ImageFolder):
    def __init__(self, root, transform = None, target_transform = None, split_type = None, train_num:int = 5):
        self.scene_root = root + '/scene'
        root = 'output/subFocura'
        super(Focura, self).__init__(root, transform, target_transform)
        splited = [[] for _ in range(len(self.classes))]
        self.samples = []
        for img, label in self.imgs:
            splited[label].append((img, label))
        for x in splited:
            if split_type == 'train':
                self.samples += x[:train_num]
            else:
                self.samples += x[train_num:]
        self.imgs = self.samples
        random.shuffle(self.samples)
        self.targets = [s[1] for s in self.samples]

    @staticmethod
    def __build_subset__(focura_root):
        scene_dir = focura_root + '/scene'
        object_dir = focura_root + '/object_224'
        output_dir = 'output/subFocura'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Iterate through all files in the scene_dir
        for filename in os.listdir(scene_dir):
            scene = None
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # Get the full file path
                file_path = os.path.join(scene_dir, filename)
                scene = Image.open(file_path)

            print(f"Build sub focura base on {filename}")
            for subdir, dirs, files in os.walk(object_dir):
                for file in files:
                    if file.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
                        scene_width, scene_height = scene.size
                        scale_factor_scene = random.uniform(0.5, 1) 
                        crop_size = min(scene_width, scene_height) * scale_factor_scene
                        crop_x = random.randint(0, int(scene_width - crop_size))
                        crop_y = random.randint(0, int(scene_height - crop_size))
                        cropped_scene = scene.crop((crop_x, crop_y, crop_x + crop_size, crop_y + crop_size))
                        cropped_scene = cropped_scene.resize((224, 224))

                        obj_path = os.path.join(subdir, file)
                        obj = Image.open(obj_path)

                        angle = random.randint(-20, 20)
                        scale_factor = random.uniform(0.4, 0.7)  # Scale between 50% and 80%
                        new_width = int(obj.width * scale_factor)
                        new_height = int(obj.height * scale_factor)
                        obj = obj.resize((new_width, new_height))

                        # Rotate the image by a random angle
                        # obj = obj.rotate(angle)

                        max_x = cropped_scene.width - obj.width
                        max_y = cropped_scene.height - obj.height
                        random_x = random.randint(0, max_x)
                        random_y = random.randint(0, max_y)

                        # Paste the object onto the scene at a random location
                        cropped_scene.paste(obj, (random_x, random_y), obj.convert("RGBA"))

                        relative_path = os.path.relpath(subdir, object_dir)
                        target_subdir = os.path.join(output_dir, relative_path)

                        if not os.path.exists(target_subdir):
                            os.makedirs(target_subdir)
                        
                        target_path = os.path.join(target_subdir, file)
                        cropped_scene.save(target_path)

            yield filename

if __name__ == '__main__':
    bs = Focura.__build_subset__('/share/Focura')
    print(next(bs))