from torchvision.datasets.folder import ImageFolder
import random
import os
from PIL import Image
import torch

class Focura(torch.utils.data.Dataset):
    _scene_ = ''
    _scene_root_ = ''

    # path to the Focura subset with different scenes
    _subset_root_ = '/share/Focura/subFocura/'

    def __init__(self, root, n_way=5, n_shot=5, n_query=15, n_episodes=50, transform=None):
        super().__init__()
        root = f'{Focura._subset_root_}{Focura._scene_}'
        self.dataset = ImageFolder(root, transform=None)

        self.n_way = n_way
        self.n_shot = n_shot
        self.n_query = n_query
        self.n_episodes = n_episodes

        self.class_to_images = {i: [] for i in range(len(self.dataset.classes))}
        for path, label in self.dataset.samples:
            self.class_to_images[label].append(path)

        # 过滤掉图像数不足的类
        self.class_to_images = {
            cls: imgs for cls, imgs in self.class_to_images.items()
            if len(imgs) >= n_shot + n_query
        }
        self.valid_classes = list(self.class_to_images.keys())

        assert len(self.valid_classes) >= n_way, \
            f"Not enough classes with enough images (need {n_way}, got {len(self.valid_classes)})"

        self.transform = transform
    
    def __len__(self):
        return self.n_episodes

    def __getitem__(self, idx):
        episode_classes = random.sample(self.valid_classes, self.n_way)
        # print("episode_classes:", episode_classes)
        support_imgs, support_labels = [], []
        query_imgs, query_labels = [], []

        for i, cls in enumerate(episode_classes):
            imgs = random.sample(self.class_to_images[cls], self.n_shot + self.n_query)
            support = imgs[:self.n_shot]
            query = imgs[self.n_shot:]

            support_imgs += [self.transform(Image.open(p).convert("RGB")) for p in support]
            query_imgs += [self.transform(Image.open(p).convert("RGB")) for p in query]
            support_labels += [i] * self.n_shot  # 注意用 i 而不是原始 label
            query_labels += [i] * self.n_query

        return {
            'support_data': torch.stack(support_imgs),   # [N*K, C, H, W]
            'support_labels': torch.tensor(support_labels),
            'query_data': torch.stack(query_imgs),       # [N*Q, C, H, W]
            'query_labels': torch.tensor(query_labels)
        }

    @staticmethod
    def __list_scene__(focura_root):
        Focura._scene_root_ = focura_root + '/scene'
        scene_list = []
        for i, filename in enumerate(os.listdir(Focura._scene_root_)):
            scene = filename.split(".")[0]
            scene_list.append(f"{scene}")

        print("Scene list: ", scene_list)

        return scene_list
    
    @staticmethod
    def __build_subset__(focura_root, scene_choose = None, output_dir = 'output/subFocura', export = False):
        
        Focura._scene_root_ = focura_root + '/scene'
        object_dir = focura_root + '/object_224'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Iterate through all files in the scene_dir
        for filename in os.listdir(Focura._scene_root_):
            Focura._scene_ = filename.split(".")[0]

            if scene_choose is not None and Focura._scene_ != scene_choose:
                continue

            export_path = os.path.join(output_dir, Focura._scene_)
            if export:
                if not os.path.exists(export_path):
                    os.makedirs(export_path)
            
            scene = None
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # Get the full file path
                file_path = os.path.join(Focura._scene_root_, filename)
                scene = Image.open(file_path)

            print(f"Build sub focura base on {filename}")
            for subdir, dirs, files in os.walk(object_dir):
                for file in files:
                    if file.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
                        scene_width, scene_height = scene.size
                        scale_factor_scene = random.uniform(0.5, 1)
                        # scale_factor_scene = 1
                        crop_size = min(scene_width, scene_height) * scale_factor_scene
                        crop_x = random.randint(0, int(scene_width - crop_size))
                        crop_y = random.randint(0, int(scene_height - crop_size))
                        cropped_scene = scene.crop((crop_x, crop_y, crop_x + crop_size, crop_y + crop_size))
                        cropped_scene = cropped_scene.resize((224, 224))

                        obj_path = os.path.join(subdir, file)
                        obj = Image.open(obj_path)

                        angle = random.randint(-20, 20)
                        scale_factor = random.uniform(0.4, 0.7)
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

                        if export:
                            target_subdir = os.path.join(export_path, relative_path)
                        else:
                            target_subdir = os.path.join(output_dir, relative_path)

                        if not os.path.exists(target_subdir):
                            os.makedirs(target_subdir)
                        
                        target_path = os.path.join(target_subdir, file)
                        cropped_scene.save(target_path)

            yield Focura._scene_

if __name__ == '__main__':

    # path to the Focura dataset
    Focura_PATH = '/share/Focura'
    
    # build subset with export
    bs = Focura.__build_subset__(Focura_PATH, output_dir=Focura._subset_root_, export=True)
    for scene_img in bs:
        pass

    # # use the dataset
    # scene_list = Focura.__list_scene__('/share/Focura')
    # for scene in scene_list:
    #     Focura._scene_ = scene
    #     # ...