# Arduino Sensor Data Viewer

csv ファイルをリアルタイムに読み込み、解析・表示するクロスプラットフォーム GUI アプリケーション

https://user-images.githubusercontent.com/47422498/188201253-5435330d-68b9-403f-bfe2-4fd7f1703085.mov

## Overview

csv ファイルをリアルタイムに読み込み、解析・表示する PyQt ベースの汎用的なアプリケーションです。[Arduino Serial Plot Recorder](https://github.com/kiyu-git/Arduino-Serial-Plot-Recorder)と組み合わせることで、リアルタイムにセンサー等のデータを解析できます。軽量なので、Raspberry Pi などでも動作します。長期間の観測に向いています。

[こちら](https://kiyu-shop.booth.pm/items/4140938)からプロジェクトへの寄付ができます。
継続的なプロジェクト維持のため、ぜひ寄付をお願いいたします。

## Requirement

### Mac

- PyQt のインストール

```
% brew install pyqt@5
```

- conda のインストール
- conda パッケージのインストール

```
% conda create -n PyQt python=3.9
% conda activate PyQt
% conda install pyqt
% conda install numpy
% conda install pyserial
% conda install pyqtgraph
% conda install pandas
```

- リポジトリのクローン

```
% git clone https://github.com/kiyu-git/Arduino-Sensor-Data-Viewer
```

### Raspberry pi

- Python のインストール

```
$ curl https://pyenv.run | bash
$ python -V
Python 3.9.2
```

- PyQt のインストール

```
$ sudo apt install libffi-dev
$ sudo apt install libatlas-base-dev
$ sudo apt install qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tool
```

- pip package のインストール

```
$ pip install pyqt5
$ pip install numpy pyserial pyqtgraph pandas
```

- リポジトリのクローン

```
$ mkdir PlantAnalysisApps
$ cd PlantAnalysisApps
$ git clone https://github.com/kiyu-git/Arduino-Sensor-Data-Viewer
```

## Usage

### Python

```
% python main.py
```

## Features

GUI のパラメータ説明

- file: 読み込むファイルを選択します。プルダウンから[set another data folder]を選択し、目的のフォルダを開きます。この際に、必ず[Arduino Serial Plot Recorder](https://github.com/kiyu-git/Arduino-Serial-Plot-Recorder)で生成された Data フォルダを選択してください。
- channel: [Arduino Serial Plot Recorder](https://github.com/kiyu-git/Arduino-Serial-Plot-Recorder) の Measurement Settings パネルで 2 以上を入力した場合のみ、対象とするチャンネルの番号を選べます。
- start: 表示するデータの開始時刻を変更できます。なお、load limit の方が優先されます
- invert: チェックすると 2.5V を基準に測定データの上下を反転できます
- load limit: 表示するデータの長さを変更できます
- LPF strength: ローパスフィルターの強度を変更できます
- update: チェックすると一定間隔でファイルの増分を読み込み、グラフを更新します
- update interval: グラフを更新する時間間隔を変更できます

## Related repository

このリポジトリは、『[植物生体電位測定をオープンにするプロジェクト](https://docs.google.com/presentation/d/1Tm0e-mBNrTchN6YlGpvvomUZfy79yOtrTSNHG-l_jFg/edit?usp=sharing)』の一部です。

『[植物生体電位測定をオープンにするプロジェクト](https://docs.google.com/presentation/d/1Tm0e-mBNrTchN6YlGpvvomUZfy79yOtrTSNHG-l_jFg/edit?usp=sharing)に関連する以下のリポジトリと組み合わせることによって、植物生体電位を測定することが可能です。

- 植物生体電位解析器 : https://github.com/kiyu-git/Plant-Bioelectric-Potential-Sensor
- 測定アプリケーション : https://github.com/kiyu-git/Arduino-Serial-Plot-Recorder
- 解析アプリケーション : https://github.com/kiyu-git/Arduino-Sensor-Data-Viewer
- 照明スイッチの自動化 : https://github.com/kiyu-git/Arduino-Python-Serial-Control-Example

植物生体電位の測定の詳細については[こちら](https://docs.google.com/presentation/d/1Tm0e-mBNrTchN6YlGpvvomUZfy79yOtrTSNHG-l_jFg/edit#slide=id.g15184a93673_0_264)を参考にしてください。

植物生体電位測定の例
![Plant-Bioelectric-Potential-Mearurement](https://github.com/kiyu-git/Plant-Bioelectric-Potential-Sensor/raw/main/images/Plant-Bioelectric-Potential-Mearurement.jpeg)

## Reference

## Donation

[こちら](https://kiyu-shop.booth.pm/items/4140938)からプロジェクトへの寄付ができます。
継続的なプロジェクト維持のため、ぜひ寄付をお願いいたします。

## Author

質問等は twitter または[Issues](https://github.com/kiyu-git/Arduino-Sensor-Data-Viewer/issues)より

twitter: https://twitter.com/kyu_yukirinrin

website: https://untamable.work

## Licence

[GNU General Public License v3.0](./LICENSE)
