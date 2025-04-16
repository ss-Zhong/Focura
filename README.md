# Focura Dataset

**Focura** is a dataset designed for image classification tasks, focusing on the clear separation of foreground and background elements. The name "Focura" comes from the fusion of "Focus" and "Aura", symbolizing the clarity and distinction between the foreground and background that this dataset aims to highlight.

Special thanks to the contributors on [**Pexels**](https://www.pexels.com/) for providing the images used in this dataset.

## Use Focura

Just use the `Focura` class in `Focura.py` as the `ImageFolder` class. 

- Iterate over the background

  ```python
  bs = Focura.__build_subset__('/share/Focura')
  for scene_img in bs:
      ...
  ```

- Single background (`snow` as example)

  ```python
  bs = Focura.__build_subset__('/share/Focura', scene_choose='snow')
  for scene_img in bs:
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
