# settings.py
# DMG パッケージ化用の設定ファイル

# DMG のボリューム名
volume_name = "My App"

# /Applications フォルダへのシンボリックリンクを作成（オプション）
applications_link = "/Applications"

# DMG ウィンドウの位置とサイズ (左上の座標とウィンドウサイズ)
window_rect = ((100, 100), (800, 600))

# アイコンのサイズ（ピクセル単位）
icon_size = 128

# （任意）背景画像を指定する場合は、画像ファイル（例: background.png）を用意し、以下のコメントアウトを解除
# background = "background.png"

# （任意）アイコンの配置例
# files: アプリのアイコンの位置を指定する（例：MyApp.app のアイコン）
files = {
    "dist/MyApp.app": {"x": 200, "y": 150},
}
# /Applicationsへのシンボリックリンクを作成（任意）
applications_link = "/Applications"
