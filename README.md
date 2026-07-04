# GRsync (Python 3 Edition) V1.1.1

このPythonスクリプトはImageSyncの仕組みを利用し、**GR II / GR III series / GR IV series**とPC（Windows / Mac OS）を直接Wi-Fi接続して写真の転送を行います。  
*（GR IV Monochromeで利用できました）*  


---

##  SUPPORT DEVICE ListにGR IVシリーズを追加
使い方は概ね同じですが、GR IVのWi-fi起動はアプリ「GR World」から行い、SSID起動後PCだけ接続。
（スマートフォンはアプリの画面で「（SSID）に接続しますか？」がポップアップしても「いいえ」、もしくはそのまま放置で対応）

---

##  使い方

### 1. 設定
`GRsync.py`内の設定項目 `PHOTO_DEST_DIR` を、ご自身の環境（保存場所）に合わせて変更してください。また、**パスの末尾は必ず `/` で終了させてください。**  

> Windows : `PHOTO_DEST_DIR = "D:/doc/Pictures/GR3/"`  
> Mac OS  : `PHOTO_DEST_DIR = "/Users/username/Pictures/GR3/"`

### 2. 必須条件
Python 3以上のバージョンをインストールしてご利用ください。  

### 3. 実行権限の付与
`GRsync.py`に実行権限を付与してください。  
```bash
chmod +x GRsync.py
```

### 4. Wi-Fi接続
PCとGRをWi-Fiで接続してください。
* GRメニュー → 無線LAN設定 → 動作モードをONに変更
* 通信情報で接続先情報を確認し、PCから接続します。

### 5. Run the Script / 実行
PC側で、GRsync.pyを実行します。（ターミナル or PowerShell）

#### すべての写真を取得する場合:
```bash
python3 GRsync.py -a
```

#### ファイルを指定して取得する場合:
```bash
python3 GRsync.py -d [DirectoryName] -f [FileName]
```

### -tf オプションの使い方

`-tf`（または `--timestamp-folder`）オプションは、カメラのフォルダ構造ではなく「ダウンロードした日時」ごとに写真を整理したい場合に便利です。

##### Example Command / 実行例

すべての写真を新しい日時フォルダにダウンロードする:
```bash
python3 GRsync.py -a -tf
```

2. 特定のファイル以降を日時フォルダにダウンロードする:  
```bash
python3 GRsync.py -d 100RICOH -f R0000001.JPG -tf
```

##### フォルダ構造の比較

| Mode | パスの例 | 説明 |
|:---|:---|:---|
| **Without `-tf` (Default)** | `.../GR3/100RICOH/R0000001.JPG` | カメラ側のフォルダ構造を維持します。 |
| **With `-tf`** | `.../GR3/20260101-1200/R0000001.JPG` | **フラット構造。** すべてのファイルが日時フォルダの直下に保存されます。 |

---

## License / Origins
* **Original Python 2 script:** Created by [clyang / GRsync](https://github.com/clyang/GRsync)
* **Python 3 port:** Updated by [zaka](https://zakazukuri.com/ricoh-digital-camera-gr-iii-wifi-photo-transfer/)
* **HDF Support & Fixes:** Updated by @[no-ra-inu](https://github.com/your-profile)


---

# GRsync (Python 3 Edition)

This Python script uses the ImageSync mechanism to transfer photos via a direct Wi-Fi connection between a GR II / GR III series / GR IV series camera and a PC (Windows / macOS).
(Confirmed working with the GR IV Monochrome)

---
## Added GR IV series to the SUPPORT DEVICE list
Usage is largely the same, but for the GR IV, Wi-Fi must be started from the "GR World" app. Once the SSID is active, connect only the PC to it.
(On the smartphone, if a "Connect to (SSID)?" popup appears in the app, tap "No" or simply leave it — don't connect the phone.)

---

## Usage
### 1. Configuration

Open `GRsync.py` and change the `PHOTO_DEST_DIR` to your preferred local folder path. **Ensure the path ends with a slash `/`.**  

> Windows : `PHOTO_DEST_DIR = "D:/doc/Pictures/GR3/"`  
> Mac OS  : `PHOTO_DEST_DIR = "/Users/username/Pictures/GR3/"`

### 2. Requirements
Please ensure Python 3 or higher is installed on your system.

### 3. Set Execution Permission 
Give execution permission to the script.
```bash
chmod +x GRsync.py
```

### 4. Wi-Fi Connection 
Connect your PC to the GR camera via Wi-Fi. 
* GR Menu -> Wireless LAN Settings -> Operating Mode: ON
* Check Communication Info for the SSID and password to connect.

### 5. Run the Script
Run the script from your terminal/command prompt. 

#### To download ALL photos
```bash
python3 GRsync.py -a
```

#### To download specific files
```bash
python3 GRsync.py -d [DirectoryName] -f [FileName]
```

### How to use the `-tf` option / -

The `-tf` (or `--timestamp-folder`) option is useful when you want to organize your photos by "download date" rather than camera directory structure.

##### Example Command

1. Download all photos into a new timestamped folder:
```bash
python3 GRsync.py -a -tf
```

2. Download from a specific file into a timestamped folder:
```bash
python3 GRsync.py -d 100RICOH -f R0000001.JPG -tf
```

##### Folder Structure Comparison

| Mode | Path Example | Description |
|:---|:---|:---|
| **Without `-tf` (Default)** | `.../GR3/100RICOH/R0000001.JPG` | Maintains camera directory structure. |
| **With `-tf`** | `.../GR3/20260101-1200/R0000001.JPG` | **Flat structure.** All files are saved directly under the timestamp folder. |

---

## License / Origins
* **Original Python 2 script:** Created by [clyang / GRsync](https://github.com/clyang/GRsync)
* **Python 3 port:** Updated by [zaka](https://zakazukuri.com/ricoh-digital-camera-gr-iii-wifi-photo-transfer/)
* **HDF Support & Fixes:** Updated by @[no-ra-inu](https://github.com/your-profile)
