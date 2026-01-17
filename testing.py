import os

path = os.getcwd()
print(path)


for directory in os.listdir(path):
    dir_path = os.path.join(path, directory)
    if dir_path and dir_path.endswith("_imgs"):
        print(f"dir: {directory}")
        for png in os.listdir(dir_path):
            print(png)
