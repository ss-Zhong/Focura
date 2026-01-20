# ✨Focura✨

> 🎉🎉 Congratulations! Our paper **"Glasses: Enabling Fast Environment-aware Few-Shot Learning via Device-Cloud Collaboration"** has been accepted to **the ACM Web Conference 2026 (WWW '26)**! 

<p align="center">
  <a href="https://github.com/ss-Zhong/Focura/stargazers"><img src="https://img.shields.io/github/stars/ss-Zhong/Focura?style=for-the-badge&color=5caaf3" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ss-Zhong/Focura?style=for-the-badge&color=6c757d" alt="License"></a>
  <a href="https://github.com/ss-Zhong/Focura/commits"><img src="https://img.shields.io/github/last-commit/ss-Zhong/Focura?style=for-the-badge&color=4c9f70" alt="Last Commit"></a>
  <a href="https://github.com/ss-Zhong/Focura"><img src="https://img.shields.io/github/repo-size/ss-Zhong/Focura?style=for-the-badge&color=17a2b8" alt="Repo Size"></a>
  <a href="https://github.com/ss-Zhong/Focura/issues"><img src="https://img.shields.io/github/issues/ss-Zhong/Focura?style=for-the-badge&color=f39c12" alt="Issues"></a>
</p>

<img src="img/README/Focura_sample.png" style="zoom:67%;" />

**Focura** is a dataset designed for image classification tasks, focusing on the clear separation of foreground and background elements. The name "Focura" is a fusion of "Focus" and "Aura", symbolizing the clarity and distinction between the foreground and background that this dataset aims to highlight.

The dataset includes **10 specific scenes**, containing **10 object classes**, with **20 objects per class**. This setup ensures a diverse set of images for robust classification tasks.

Special thanks to the contributors on [**Pexels**](https://www.pexels.com/) for providing the images used in this dataset.

## Using Focura

To use the dataset, simply utilize the `Focura` class in `Focura.py`, which functions similarly to the `ImageFolder` class. 

### Build Subset (Only Build Once)

  ```python
  bs = Focura.__build_subset__(Focura_PATH, output_dir=Focura._subset_root_, export=True, change_light=True)
  for scene_img in bs:
      pass
  ```

  Alternatively, you can run the script directly:

  ```bash
  python ./Focura.py
  ```

### Load Scenes

- To load all scenes:

  ```python
  Focura._subset_root_ = PATH_to_SubFocura # e.g. "./subFocura"
  scene_list = Focura.__list_scene__('./')
  for scene in scene_list:
      Focura._scene_ = scene
      ...
  ```

- To load selected scenes:

  ```python
  Focura._subset_root_ = PATH_to_SubFocura # e.g. "./subFocura"
  scene_list = ["snow", ...]
  for scene in scene_list:
      Focura._scene_ = scene
      ...
  ```

## Expanding the Dataset with Your Own Data

We provide Python scripts to help you expand the dataset using [**Segment Anything**](https://segment-anything.com/demo).

1. To crop your images, run:

    ```bash
    python .\tools\clipImg.py --label [YOUR_LABEL] --save_folder_path [YOUR_IMG_PATH]
    ```

2. To rename and reshape the dataset, run:

    ```bash
    python .\tools\rename_resolution.py
    ```
