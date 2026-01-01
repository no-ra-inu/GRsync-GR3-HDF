# GRsync (Python 3 Edition)

このPythonスクリプトはImageSyncの仕組みを利用し、**GR II / GR III / GR IIIx / GR III HDF / GR IIIx HDF**とPC（Windows / Mac OS）を直接Wi-Fi接続して写真の転送を行います。  
*（GR IVは未検証です。`SUPPORT_DEVICE`リストに追加することで対応できる可能性があります。）*  
This Python script uses the ImageSync API to transfer photos directly via Wi-Fi from **RICOH GR II / GR III / GR IIIx / GR III HDF / GR IIIx HDF** to your PC (Windows / Mac OS).  
*(Note: GR IV is not yet verified. It might work by adding it to the `SUPPORT_DEVICE` list.)*  


---

## Usage / 使い方

### 1. Configuration / 設定
`GRsync.py`内の設定項目 `PHOTO_DEST_DIR` を、ご自身の環境（保存場所）に合わせて変更してください。また、**パスの末尾は必ず `/` で終了させてください。**  
Open `GRsync.py` and change the `PHOTO_DEST_DIR` to your preferred local folder path. **Ensure the path ends with a slash `/`.**  

> Windows : `PHOTO_DEST_DIR = "D:/doc/Pictures/GR3/"`  
> Mac OS  : `PHOTO_DEST_DIR = "/Users/username/Pictures/GR3/"`

### 2. Requirements / 必須条件
Python 3以上のバージョンをインストールしてご利用ください。  
Please ensure Python 3 or higher is installed on your system.

### 3. Set Execution Permission / 実行権限の付与
`GRsync.py`に実行権限を付与してください。  
Give execution permission to the script.
```bash
chmod +x GRsync.py
```

### 4. Wi-Fi Connection / Wi-Fi接続
PCとGRをWi-Fiで接続してください。  
Connect your PC to the GR camera via Wi-Fi. 
* GRメニュー → 無線LAN設定 → 動作モードをONに変更<br>GR Menu -> Wireless LAN Settings -> Operating Mode: ON
* 通信情報で接続先情報を確認し、PCから接続します。<br>Check Communication Info for the SSID and password to connect.

### 5. Run the Script / 実行
PC側で、GRsync.pyを実行します。  Run the script from your terminal/command prompt. 

#### To download ALL photos / すべての写真を取得する場合:
```bash
python3 GRsync.py -a
```

#### To download specific files / ファイルを指定して取得する場合:
```bash
python3 GRsync.py -d [DirectoryName] -f [FileName]
```

## License / Origins
* Original Python 2 script: Created by clyang / [GRsync](https://github.com/clyang/GRsync)
* 
