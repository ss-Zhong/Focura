# Focura

![GitHub stars](https://img.shields.io/github/stars/ss-Zhong/Focura?style=flat&color=5caaf3)
![Visits](https://badges.pufler.dev/visits/ss-Zhong/Focura?color=47bdae)
![License](https://img.shields.io/github/license/ss-Zhong/Focura)
![Last commit](https://img.shields.io/github/last-commit/ss-Zhong/Focura)

**Focura** is a dataset designed for image classification tasks, focusing on the clear separation of foreground and background elements. The name "Focura" comes from the fusion of "Focus" and "Aura", symbolizing the clarity and distinction between the foreground and background that this dataset aims to highlight.

Special thanks to the contributors on [**Pexels**](https://www.pexels.com/) for providing the images used in this dataset.

## Use Focura

Just use the `Focura` class in `Focura.py` as the `ImageFolder` class. 

- Build subset (only build once)

  ```python
  bs = Focura.__build_subset__(Focura_PATH, output_dir=Focura._subset_root_, export=True)
  for scene_img in bs:
      pass
  ```

  or you can just

  ```bash
  python ./Focura.py
  ```

- Load scenes

  - All scenes

      ```python
      scene_list = Focura.__list_scene__('/share/Focura')
      for scene in scene_list:
          Focura._scene_ = scene
      	...
      ```
      
  - Selected scenes

      ```python
      scene_list = ["snow", ...]
      for scene in scene_list:
          Focura._scene_ = scene
      	...
      ```


## Use your data to expand the dataset.

We provide python script to help you expand your dataset with the help of [**Segment Anything**](https://segment-anything.com/demo).

1. You can clip the img you have by running:

    ```bash
    python .\tools\clipImg.py --label [YOUR_LABEL] --save_folder_path [YOUR_IMG_PATH]
    ```

2. And you can rename and reshape the dataset by running:

    ```bash
    python .\tools\rename_resolution.py
    ```
