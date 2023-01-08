import csv
import datetime as dt
import itertools

# set logging
import logging
import os
import sys
import time
from collections import deque
from itertools import islice
from turtle import width

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6 import QtCore, QtWidgets

import tools
from UI.Ui_Analyzer import Ui_Analyzer

"""
Set Logger
"""


class DashLoggerHandler(logging.StreamHandler):
    def __init__(self, console):
        logging.StreamHandler.__init__(self)
        self.console = console

    def emit(self, record):
        msg = self.format(record)
        print(msg)
        self.console.append(msg)


# set logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# FORMAT = "%(asctime)s %(message)s"
FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


"""
Main Window
"""


class GraphWindow(QtWidgets.QWidget):
    pre_file_idx = 0

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)
        # uic.loadUi("./UI/analysis_simple.ui", self)
        self.ui = Ui_Analyzer()
        self.ui.setupUi(self)

        self.setWindowTitle("Analyzer")
        # logger
        dashLoggerHandler = DashLoggerHandler(self.InputConsole)
        logger.addHandler(dashLoggerHandler)
        # init graphs
        self.dir_path = "../../002_生体電位測定/Data"
        if not os.path.exists(self.dir_path):
            self.dir_path = "./template/Data"
        self.folder_paths = tools.get_latest_folder_paths(self.dir_path)
        path_latest_folder: str = self.folder_paths[0]

        self.init_variables(path_latest_folder)
        # inspector
        self.droppdown_items, self.update_timer = self.set_inspector_ui()
        # update flg
        if self.settings["update_flg"]:
            self.update_timer.start()

    def init_variables(self, _folder_path):
        # paths
        self.csv_path: str = tools.get_csv_path(_folder_path)
        self.settings_path: str = tools.get_settings_path(_folder_path, __file__)
        # settings
        self.settings = tools.get_analysis_settings(self.settings_path)
        self.measurement_settings = tools.get_measurement_settings(_folder_path)
        # graph
        self.graph = DrawGraph(
            self.csv_path,
            self.settings,
            self.measurement_settings,
            self.GraphicsLayoutWidget,
        )

    def set_inspector_ui(self):
        droppdown_items = tools.make_droppdown_item(self.folder_paths)
        droppdown_item_labels = [item["label"] for item in droppdown_items]
        self.InputFiles.addItems(droppdown_item_labels)
        self.InputFiles.setCurrentText(droppdown_item_labels[0])
        self.pre_file_idx = 0
        self.InputFiles.currentIndexChanged.connect(
            lambda index: self.load_new_file(index)
        )

        self.InputProgram.setText(os.path.basename(__file__))

        self.InputChannel.setRange(0, self.measurement_settings["num_channels"] - 1)
        self.InputChannel.setSingleStep(1)
        self.InputChannel.setValue(self.settings["channel"])
        self.InputChannel.valueChanged.connect(
            lambda value: self.update_graph_with_variables("channel", value)
        )

        self.InputStartDate.setDateTime(
            dt.datetime.strptime(self.settings["start_date"], "%Y-%m-%d_%H-%M-%S")
        )
        self.InputStartDate.setDisplayFormat("yyyy/MM/dd hh:mm:ss")
        self.InputStartDate.setSelectedSection(0x0008)
        self.InputStartDate.dateTimeChanged.connect(
            lambda value: self.update_graph_with_variables("start_date", value)
        )

        self.InputInvertFlg.setChecked(self.settings["invert_flg"])
        self.InputInvertFlg.stateChanged.connect(
            lambda value: self.update_graph_with_variables("invert_flg", value)
        )

        self.InputLoadLimit.setMinimum(1)
        self.InputLoadLimit.setSingleStep(1)
        self.InputLoadLimit.setValue(self.settings["num_load_hours"])
        self.InputLoadLimit.valueChanged.connect(
            lambda value: self.update_graph_with_variables("num_load_hours", value)
        )

        self.InputLPFStrength.setRange(0.0, 1.0)
        self.InputLPFStrength.setSingleStep(0.1)
        self.InputLPFStrength.setValue(self.settings["LPF_strength"])
        self.InputLPFStrength.valueChanged.connect(
            lambda value: self.update_graph_with_variables("LPF_strength", value)
        )

        self.InputUpdateFlg.setChecked(self.settings["update_flg"])
        self.InputUpdateFlg.stateChanged.connect(
            lambda value: self.update_graph_with_variables("update_flg", value)
        )

        self.InputUpdateInterval.setMinimum(5)
        self.InputUpdateInterval.setSingleStep(5)
        self.InputUpdateInterval.setValue(self.settings["update_seconds"])
        self.InputUpdateInterval.valueChanged.connect(
            lambda value: self.update_graph_with_variables("update_seconds", value)
        )

        update_timer = QtCore.QTimer()
        update_timer.setInterval(self.settings["update_seconds"] * 1000)
        update_timer.timeout.connect(lambda: self.update_graph_with_interval())

        return droppdown_items, update_timer

    def load_new_file(self, idx):
        folder_path = self.droppdown_items[idx]["value"]
        if folder_path == "[set another Data folder]":
            dir = QtWidgets.QFileDialog.getExistingDirectory(
                None,
                "Select a folder:",
                self.dir_path,
                QtWidgets.QFileDialog.ShowDirsOnly,
            )
            if dir == "":
                droppdown_item_labels = [item["label"] for item in self.droppdown_items]
                self.InputFiles.blockSignals(True)
                self.InputFiles.setCurrentText(droppdown_item_labels[self.pre_file_idx])
                self.InputFiles.blockSignals(False)
            else:
                self.dir_path = dir
                self.folder_paths = tools.get_latest_folder_paths(self.dir_path)
                path_latest_folder: str = self.folder_paths[0]
                self.folder_path = path_latest_folder
                self.droppdown_items = tools.make_droppdown_item(self.folder_paths)
                droppdown_item_labels = [item["label"] for item in self.droppdown_items]

                self.init_variables(self.folder_path)

                # file listの更新
                self.InputFiles.blockSignals(True)
                self.InputFiles.clear()
                self.InputFiles.addItems(droppdown_item_labels)
                self.InputFiles.setCurrentText(droppdown_item_labels[0])
                self.pre_file_idx = 0
                self.InputFiles.blockSignals(False)

                # uiの更新
                self.update_inspector_ui(self.settings, self.measurement_settings)

        else:
            self.pre_file_idx = idx
            self.init_variables(folder_path)
            self.update_inspector_ui(self.settings, self.measurement_settings)

    def update_inspector_ui(self, settings, measurement_settings):
        self.InputChannel.blockSignals(True)
        self.InputStartDate.blockSignals(True)
        self.InputInvertFlg.blockSignals(True)
        self.InputLoadLimit.blockSignals(True)
        self.InputLPFStrength.blockSignals(True)
        self.InputChannel.setRange(0, measurement_settings["num_channels"] - 1)
        self.InputChannel.setValue(settings["channel"])
        self.InputStartDate.setDateTime(
            dt.datetime.strptime(settings["start_date"], "%Y-%m-%d_%H-%M-%S")
        )
        self.InputInvertFlg.setChecked(settings["invert_flg"])
        self.InputLoadLimit.setValue(settings["num_load_hours"])
        self.InputLPFStrength.setValue(settings["LPF_strength"])
        self.InputUpdateFlg.setChecked(settings["update_flg"])
        self.InputUpdateInterval.setValue(settings["update_seconds"])
        self.update_timer.setInterval(settings["update_seconds"] * 1000)
        self.InputChannel.blockSignals(False)
        self.InputStartDate.blockSignals(False)
        self.InputInvertFlg.blockSignals(False)
        self.InputLoadLimit.blockSignals(False)
        self.InputLPFStrength.blockSignals(False)

    def update_graph_with_variables(self, key, value):
        # settingsの更新
        if key == "invert_flg" or key == "update_flg":
            if value == 2:
                self.settings[key] = True
            elif value == 0:
                self.settings[key] = False
            else:
                print("Error")
        elif key == "start_date":
            self.settings[key] = value.toString("yyyy-MM-dd_hh-mm-ss")
        else:
            self.settings[key] = value

        # 保存
        tools.save_settings(self.settings, self.settings_path)
        if key == "update_flg" or key == "update_seconds":
            if key == "update_flg":
                if value:
                    self.update_timer.start()
                else:
                    self.update_timer.stop()
            elif key == "update_seconds":
                self.update_timer.setInterval(value * 1000)
        else:
            self.graph.update_with_variables(
                self.settings, self.measurement_settings, key
            )

    def update_graph_with_interval(self):
        # 再描画
        self.graph.update_with_interval()


"""
Draw Graph
"""


class DrawGraph:
    colorpalette = itertools.cycle(
        [
            "#636EFA",
            "#EF553B",
            "#00CC96",
            "#AB63FA",
            "#FFA15A",
            "#19D3F3",
            "#FF6692",
            "#B6E880",
            "#FF97FF",
            "#FECB52",
        ]
    )

    def __init__(
        self, _csv_path, _settings, _measurement_settings, _GraphicsLayoutWidget
    ) -> None:
        # init variables
        self.csv_path = _csv_path
        self.settings = _settings
        self.measurement_settings = _measurement_settings
        self.GraphicsLayoutWidget = _GraphicsLayoutWidget
        self.init_variables(self.settings, self.measurement_settings)

        ### figure
        self.graphs = self.set_graph_ui()
        # Draw Figure
        self.data = self.plot(True)
        # 十字ポインター
        self.graphs["signals"]["graphic"].scene().sigMouseMoved.connect(self.mouseMoved)
        # 範囲
        self.graphs["range"]["region"].sigRegionChanged.connect(self.updateViewRange)
        self.set_view_area()
        self.graphs["signals"]["graphic"].sigRangeChanged.connect(self.updateRegion)

    def init_variables(self, _settings, _measurement_settings):
        self.pre_max_time = self.pre_min_time = dt.datetime.strptime(
            _settings["start_date"], "%Y-%m-%d_%H-%M-%S"
        )
        sample_freq = 1 / float(_measurement_settings["log_interval"])
        self.num_load_samples = int(_settings["num_load_hours"] * 60 * 60 * sample_freq)
        self.data_arr: dict[str, deque] = {
            "date": deque([], maxlen=self.num_load_samples),
            "raw": deque([], maxlen=self.num_load_samples),
            "filtered": deque([], maxlen=self.num_load_samples),
            # "HPF": deque([], self.num_load_samples),
        }
        self.line_loaded = 0

    def set_view_area(self, _setX=True, _setY=True):
        self.graphs["signals"]["graphic"].setLimits(
            xMin=0,
            xMax=sys.float_info.max,
            yMin=sys.float_info.min,
            yMax=sys.float_info.max,
        )
        if _setX:
            self.graphs["range"]["region"].setRegion(
                [self.data.index[0], self.data.index[-1]]
            )
        self.graphs["signals"]["graphic"].enableAutoRange(axis="y")
        self.graphs["signals"]["graphic"].setAutoVisible(y=True)
        view = self.graphs["signals"]["graphic"].viewRange()
        self.graphs["signals"]["graphic"].setLimits(
            xMin=view[0][0], xMax=view[0][1], yMin=view[1][0], yMax=view[1][1]
        )

    def set_graph_ui(self) -> dict:
        """
        now
        plots: {
            signals,
            range
        }

        lines: {
            raw_signal,
            filtered_signal,
        }
        """
        """
        want to
        graph: {
            label: {
                graphic,
                plots
            }
            signals: {
                graphic,
                plots: {
                    raw_signal,
                    filtered_signal,
                    vLine,
                    hLine,
                    vb
                }
            },
            range: {
                graphic,
                plots: {
                    raw_signal,
                }
                region,
            }
        }


        """
        graphs: dict[str, dict] = {}

        pg.setConfigOptions(antialias=True)
        win = self.GraphicsLayoutWidget
        win.clear()
        graphs["label"]: dict = {}
        graphs["label"]["graphic"] = pg.LabelItem(justify="right")
        graphs["label"]["graphic"].setText(
            "<span style='font-size: 12pt'>x=<br>y=</span>"
        )
        win.addItem(graphs["label"]["graphic"])

        ######
        win.nextRow()
        graph: dict = {}
        graph["graphic"] = win.addPlot()
        # 凡例
        graph["graphic"].addLegend()
        graph["graphic"].setAutoVisible(y=True)
        axis = pg.DateAxisItem()
        graph["graphic"].setAxisItems({"bottom": axis})
        graph["graphic"].setLabel("left", "Electric Potential", units="V")
        graph["graphic"].setLabel("bottom", "Time")
        # plots
        self.main_line_color = next(self.colorpalette)
        plots: dict[str, None] = {}
        plots["raw"] = graph["graphic"].plot(
            pen=pg.mkPen(color=self.main_line_color, width=2),
            name="<span style='color: #ffffff; font-size: 12px'>Raw Signal</span>",
        )
        plots["filtered"] = graph["graphic"].plot(
            pen=pg.mkPen(color=next(self.colorpalette), width=2),
            name="<span style='color: #ffffff; font-size: 12px'>Filtered Signal</span>",
        )

        # plots["HPF"] = graph["graphic"].plot(
        #     pen=next(self.colorpalette),
        #     name="<span style='color: #ffffff; font-size: 12px'>LPF</span>",
        # )
        ##### add new ...
        # cross hair
        plots["vLine"] = pg.InfiniteLine(angle=90, movable=False)
        plots["hLine"] = pg.InfiniteLine(angle=0, movable=False)
        graph["graphic"].addItem(plots["vLine"], ignoreBounds=True)
        graph["graphic"].addItem(plots["hLine"], ignoreBounds=True)
        plots["vb"] = graph["graphic"].vb

        graph["plots"] = plots
        graphs["signals"] = graph

        #####
        win.nextRow()
        graph: dict[str, None] = {}
        graph["graphic"] = win.addPlot()
        graph["graphic"].setAutoVisible(y=True)
        graph["graphic"].setMouseEnabled(x=False, y=False)
        axis = pg.DateAxisItem()
        graph["graphic"].setAxisItems({"bottom": axis})

        plots: dict[str, None] = {}
        plots["signal"] = graph["graphic"].plot(
            pen="w",
            name="<span style='color: #ffffff; font-weight: bold; font-size: 12px'>Raw Signal</span>",
        )
        graph["plots"] = plots

        graph["region"] = pg.LinearRegionItem()
        graph["region"].setZValue(10)
        graph["graphic"].addItem(graph["region"], ignoreBounds=True)

        graphs["range"] = graph

        ###
        win.ci.layout.setRowStretchFactor(0, 1)
        win.ci.layout.setRowStretchFactor(1, 8)
        win.ci.layout.setRowStretchFactor(2, 2)

        return graphs

    def plot(self, _init_call_flg):
        # main
        t1 = time.time()
        logger.info("########\nfile loading...")
        with open(self.csv_path) as f:
            # 読み込み制限
            raw_data = f.readlines()  ## ファイルを全行読む
            new_data = (
                raw_data[-self.num_load_samples :]  ## 初回読み込みの場合は制限の分だけ読む
                if _init_call_flg
                else raw_data[self.line_loaded :]  ## 初回以外の読み込みの場合は未読み込みの部分だけ読む
            )
            self.line_loaded = len(raw_data)

            # 最終行のNULLを削除
            if 0 < len(new_data) and "\0" in new_data[-1]:
                new_data = new_data[0:-1]

            # 読み込み
            for row in csv.reader(new_data):
                ### date
                try:
                    date: int = int(
                        dt.datetime.strptime(
                            str(row[0]), "%Y-%m-%d %H:%M:%S.%f"
                        ).timestamp()
                    )
                except:
                    date: int = int(
                        dt.datetime.strptime(
                            str(row[0]), "%Y-%m-%d %H:%M:%S"
                        ).timestamp()
                    )
                self.data_arr["date"].append(date)

                ### value
                value: float = float(row[1 + self.settings["channel"]])
                if self.settings["invert_flg"]:
                    value: float = float(5 - value)
                self.data_arr["raw"].append(value)

                ### filtered LPF
                k: float = self.settings["LPF_strength"]
                value_filtered: float = (
                    k * self.data_arr["filtered"][-1] + (1 - k) * value
                    if 0 < len(self.data_arr["filtered"])
                    else value
                )
                self.data_arr["filtered"].append(value_filtered)

                ### filtered HPF
                # k: float = self.settings["LPF_strength"]
                # value_HPF: float = (
                #     0.999
                #     * (self.data_arr["HPF"][-1] + value - self.data_arr["raw"][-2])
                #     if 0 < len(self.data_arr["HPF"])
                #     else 0
                # )
                # self.data_arr["HPF"].append(value_HPF)

        # set start date
        start_date = dt.datetime.strptime(
            self.settings["start_date"], "%Y-%m-%d_%H-%M-%S"
        ).timestamp()
        start_idx = (
            tools.nearest_date(self.data_arr["date"], start_date)
            if self.data_arr["date"][0] < start_date
            else 1
        )
        for k in self.data_arr.keys():
            self.data_arr[k] = deque(
                islice(self.data_arr[k], max(0, start_idx - 1), None),
                maxlen=self.num_load_samples,
            )

        # make pandas
        logger.info("make pandas...")
        t2 = time.time()
        data_df = pd.DataFrame(
            {
                "raw": self.data_arr["raw"],
                "filtered": self.data_arr["filtered"],
                # "HPF": self.data_arr["HPF"],
            },
            index=self.data_arr["date"],
        )
        logger.info("make plot...")
        t3 = time.time()
        self.graphs["signals"]["plots"]["raw"].setData(
            data_df.index, list(data_df["raw"])
        )
        self.graphs["signals"]["plots"]["filtered"].setData(
            data_df.index, list(data_df["filtered"])
        )
        # self.graphs["signals"]["plots"]["HPF"].setData(
        #     data_df.index, list(data_df["HPF"])
        # )
        self.graphs["range"]["plots"]["signal"].setData(
            data_df.index, list(data_df["filtered"])
        )
        t4 = time.time()
        logger.info("- file load: {:.3f}".format(t2 - t1))
        logger.info("- pandas: {:.3f}".format(t3 - t2))
        logger.info("- plot: {:.3f}".format(t4 - t3))
        return data_df

    def update_with_variables(self, _settings, _measurement_settings, _key):
        # init variables
        self.init_variables(_settings, _measurement_settings)
        # Draw Figure
        self.data = self.plot(True)
        if _key == "num_load_hours":
            self.set_view_area()
        elif _key == "invert_flg":
            self.set_view_area(_setX=False)

    def update_with_interval(self):
        self.data = self.plot(False)
        self.set_view_area()

    def mouseMoved(self, pos):
        if self.graphs["signals"]["graphic"].sceneBoundingRect().contains(pos):
            mousePoint = self.graphs["signals"]["plots"]["vb"].mapSceneToView(pos)
            index = int(mousePoint.x())
            try:
                if self.data.index[0] < index and index < self.data.index[-1]:
                    self.graphs["label"]["graphic"].setText(
                        "<span style='font-size: 12pt'>x={}<br>y=<span style='color: {}'>{:.6f}</span></span>".format(
                            dt.datetime.fromtimestamp(index).strftime(
                                "%Y/%m/%d %H:%M:%S"
                            ),
                            self.main_line_color,
                            self.data.loc[index]["filtered"],
                        )
                    )
                self.graphs["signals"]["plots"]["vLine"].setPos(mousePoint.x())
                self.graphs["signals"]["plots"]["hLine"].setPos(
                    self.data.loc[index]["filtered"]
                )
            except KeyError:
                print("key error")

    def updateViewRange(self):
        minX, maxX = self.graphs["range"]["region"].getRegion()
        self.graphs["signals"]["graphic"].setXRange(minX, maxX, padding=0)

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.graphs["range"]["region"].setRegion(rgn)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWin = GraphWindow()
    myWin.show()
    sys.exit(app.exec_())
