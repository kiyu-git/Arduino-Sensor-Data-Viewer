import os

file_path = "./template/Data/---/settings.json"
file_path = os.path.join(os.path.dirname(__file__), file_path)
with open(file_path) as f:
    s = f.read()
    print(s)
