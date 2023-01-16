import json
import os
from glob import glob


def get_latest_folder_paths(dirname):
    target = os.path.join(dirname, "*")
    folders = [f for f in glob(target) if os.path.isdir(f)]
    # フォルダの名前を参照して並べ替え / .csvファイルを内包するファイルのみ抽出
    folder_paths = [
        path
        for path in sorted(folders, reverse=True)
        if os.path.isfile(get_csv_path(path))
    ]
    return folder_paths


def get_csv_path(_path_folder: str) -> str:
    name_file = _path_folder.split("/")[-1]
    return f"{_path_folder}/{name_file}.csv"


def get_settings_path(_path_folder: str, _file: str) -> str:
    prefix: str = os.path.splitext(os.path.basename(_file))[0]
    return f"{_path_folder}/{prefix}_settings.json"


def get_analysis_settings(_path_settings: str) -> dict:
    if os.path.exists(_path_settings):
        # 読み込む
        analysis_settings = loadjson(_path_settings)
    else:
        # 作る -> templateにする
        analysis_settings = {
            "channel": 0,
            "start_date": "2021-10-14_17-40-00",
            "invert_flg": False,
            "num_load_hours": 1,
            "LPF_strength": 0.8,
            "on_threshold": 0.03,
            "off_threshold": 0.03,
            "update_flg": True,
            "update_seconds": 10,
        }
        with open(_path_settings, "w") as f:
            json.dump(analysis_settings, f, indent=4, ensure_ascii=False)
    return analysis_settings


def get_measurement_settings(_folder_path: str) -> dict:
    measurement_settings = loadjson(_folder_path + "/settings.json")
    try:
        measurement_settings["log_interval"]
    except:
        measurement_settings = loadjson("./template/settings.json")  # 過去のファイル対応
        print("use template setting file")
    return measurement_settings


def save_settings(_settings, _settings_path):
    _settings = _settings.copy()
    with open(_settings_path, "w") as f:
        json.dump(_settings, f, indent=4, ensure_ascii=False)


def make_droppdown_item(_folder_paths):
    dics = []
    for idx, folder_path in enumerate(_folder_paths):
        if idx == 0:
            dic = {
                "label": "[latest] " + get_folder_name(folder_path),
                "value": folder_path,
            }
        else:
            dic = {
                "label": get_folder_name(folder_path),
                "value": folder_path,
            }
        dics.append(dic)
    dics.append(
        {
            "label": "[set another Data folder]",
            "value": "[set another Data folder]",
        }
    )
    return dics


# parts
def loadjson(_path):
    try:
        return json.load(open(_path, "r"))
    except FileNotFoundError as e:
        print(e)


def get_folder_name(_folder_path):
    name = _folder_path.split("/")[-1]
    if "." in name:
        # 小数点第2位以下を切り捨て
        name = name[0:-4]
    return name


# #########
# def folder_path2csv_path(_folder_path):
#     return _folder_path + "/" + _folder_path.split("/")[-1] + ".csv"


# def loadmysettings(_folder_path, _file):
#     settings_path = (
#         _folder_path
#         + "/"
#         + os.path.splitext(os.path.basename(_file))[0]
#         + "_settings.json"
#     )
#     if os.path.exists(settings_path):
#         # 読み込む
#         settings = loadjson(settings_path)
#     else:
#         # 作る
#         settings = {
#             "channel": 0,
#             "start_date": "2021-10-14_17-40-00",
#             "invert_flg": False,
#             "num_load_hours": 1,
#             "LPF_strength": 0.8,
#             "on_threshold": 0.03,
#             "off_threshold": 0.03,
#             "update_flg": True,
#             "update_seconds": 10,
#         }
#         with open(settings_path, "w") as f:
#             json.dump(settings, f, indent=4, ensure_ascii=False)

#     return settings, settings_path


# def set_settings_variables(_folder_path, _file):
#     csv_path = folder_path2csv_path(_folder_path)
#     settings, settings_path = loadmysettings(_folder_path, _file)
#     measurement_settings = loadjson(_folder_path + "/settings.json")
#     try:
#         measurement_settings["log_interval"]
#     except:
#         measurement_settings = loadjson(
#             "./template/settings.json"
#         )  # 過去のファイル対応
#         print("use template setting file")

#     return csv_path, settings, settings_path, measurement_settings

# def nearest_date(dates, target):
#     # will return index
#     time_diff = np.abs([date - target for date in dates])
#     return time_diff.argmin(0)


# ########
# def folder_path2folder_names(_folder_path):
#     name = _folder_path.split("/")[-1]
#     if "." in name:
#         # 小数点第2位以下を切り捨て
#         name = name[0:-4]
#     return name


# def folder_paths2dict(_folder_paths):
#     dics = []
#     for idx, folder_path in enumerate(_folder_paths):
#         if idx == 0:
#             dic = {
#                 "label": "[latest] " + folder_path2folder_names(folder_path),
#                 "value": folder_path,
#             }
#         else:
#             dic = {
#                 "label": folder_path2folder_names(folder_path),
#                 "value": folder_path,
#             }
#         dics.append(dic)
#     dics.append(
#         {
#             "label": "[set another Data folder]",
#             "value": "[set another Data folder]",
#         }
#     )
#     return dics


# # def folder_paths2droppdown(_folder_paths):
# #     items = []
# #     for idx, folder_path in enumerate(_folder_paths):
# #         if idx == 0:
# #             item = "[latest] " + folder_path2folder_names(folder_path)
# #         else:
# #             item = folder_path2folder_names(folder_path)
# #         items.append(item)
# #     return items

# #############
# # def save_settings(_settings, _settings_path):
# #     _settings = _settings.copy()
# #     # _settings["start_date"] = dt.datetime.strftime(_settings["start_date"], "%Y-%m-%d_%H-%M-%S")

# #     with open(_settings_path, "w") as f:
# #         json.dump(_settings, f, indent=4, ensure_ascii=False)


# #############
