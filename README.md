# GRsync (Python 3 Edition) V1.2.0

このPythonスクリプトはImageSyncの仕組みを利用し、**GR II / GR III series / GR IV series**とPC（Windows / Mac OS）を直接Wi-Fi接続して写真の転送を行います。  
*（GR IV Monochromeで利用できました）*  


---

## V1.2.0 変更点：差分ダウンロード（レジューム対応）

### `-tf` フォルダ名を `YYYYMMDD-HHMM` → `YYYYMMDD` に変更

以前は実行時刻を含む `20260101-1200` のようなフォルダ名だったため、転送途中で失敗し再実行すると別フォルダが作成されていました。  
**同日中は同じフォルダ（例：`20260101`）を使い回すよう変更しました。**

### 差分ダウンロード（全モード対応）

`-tf` の有無に関わらず、ダウンロード開始前にカメラのファイルリストと転送先フォルダのファイルリストを比較し、**未転送ファイルのみをダウンロード**します。

- 途中で失敗しても、再実行するとスキップ件数を表示して続きから取り込みます。
- 全ファイルが取得済みの場合は「Nothing to download.」と表示して終了します。

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

`-tf`（または `--timestamp-folder`）オプションは、カメラのフォルダ構造ではなく「ダウンロードした日付」ごとに写真を整理したい場合に便利です。  
JPG は日付フォルダ直下に保存され、DNG は `DNG/` サブフォルダに保存されます。  
同日に再実行した場合は同じ日付フォルダを使い回し、未転送ファイルのみダウンロードします。

##### Example Command / 実行例

すべての写真を日付フォルダにダウンロードする:
```bash
python3 GRsync.py -a -tf
```

特定のファイル以降を日付フォルダにダウンロードする:  
```bash
python3 GRsync.py -d 100RICOH -f R0000001.JPG -tf
```

##### フォルダ構造の比較

| Mode | パスの例 | 説明 |
|:---|:---|:---|
| **Without `-tf` (Default)** | `.../GR3/100RICOH/R0000001.JPG` / `.../GR3/100RICOH/DNG/R0000001.DNG` | カメラ側のフォルダ構造を維持し、DNG は各フォルダ内の `DNG/` に保存します。 |
| **With `-tf`** | `.../GR3/20260101/R0000001.JPG` / `.../GR3/20260101/DNG/R0000001.DNG` | JPG は日付フォルダ直下、DNG は `DNG/` に保存されます。 |

---

## License / Origins
* **Original Python 2 script:** Created by [clyang / GRsync](https://github.com/clyang/GRsync)
* **Python 3 port:** Updated by [zaka](https://zakazukuri.com/ricoh-digital-camera-gr-iii-wifi-photo-transfer/)
* **HDF Support & Fixes:** Updated by @[no-ra-inu](https://github.com/your-profile)


---

# GRsync (Python 3 Edition) V1.2.0

This Python script uses the ImageSync mechanism to transfer photos via a direct Wi-Fi connection between a GR II / GR III series / GR IV series camera and a PC (Windows / macOS).
(Confirmed working with the GR IV Monochrome)

---

## V1.2.0 Changes: Differential Download (Resume Support)

### `-tf` folder name changed from `YYYYMMDD-HHMM` to `YYYYMMDD`

Previously, the folder name included the time (e.g., `20260101-1200`), so a failed transfer followed by a retry would create a new, separate folder.  
**The folder now uses the date only (e.g., `20260101`), so the same folder is reused for all runs on the same day.**

### Differential download (applies to all modes)

Regardless of whether `-tf` is used, the script now compares the camera's file list against the destination folder before starting, and **downloads only the files not yet transferred**.

- If a transfer fails mid-way, re-running the script will display the number of skipped files and resume from where it left off.
- If all files are already present, the script prints "Nothing to download." and exits cleanly.

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

### How to use the `-tf` option

The `-tf` (or `--timestamp-folder`) option is useful when you want to organize your photos by download date rather than camera directory structure.  
JPG files are saved directly under the date folder, while DNG files are saved under a `DNG/` subfolder.  
Re-running on the same day reuses the same date folder and downloads only the missing files.

##### Example Command

1. Download all photos into a date folder:
```bash
python3 GRsync.py -a -tf
```

2. Download from a specific file into a date folder:
```bash
python3 GRsync.py -d 100RICOH -f R0000001.JPG -tf
```

##### Folder Structure Comparison

| Mode | Path Example | Description |
|:---|:---|:---|
| **Without `-tf` (Default)** | `.../GR3/100RICOH/R0000001.JPG` / `.../GR3/100RICOH/DNG/R0000001.DNG` | Maintains camera directory structure; DNG files are stored under `DNG/` inside each folder. |
| **With `-tf`** | `.../GR3/20260101/R0000001.JPG` / `.../GR3/20260101/DNG/R0000001.DNG` | JPG files go directly under the date folder; DNG files go under `DNG/`. |

---

## License / Origins
* **Original Python 2 script:** Created by [clyang / GRsync](https://github.com/clyang/GRsync)
* **Python 3 port:** Updated by [zaka](https://zakazukuri.com/ricoh-digital-camera-gr-iii-wifi-photo-transfer/)
* **HDF Support & Fixes:** Updated by @[no-ra-inu](https://github.com/your-profile)
