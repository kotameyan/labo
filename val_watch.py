# 最初のインポート
from PIL import Image
from IPython.display import display
import os

# 特定のフォルダ内の画像を一括表示する関数を定義
def batch_display(folder_path):

    # 画像ファイルの拡張子（ここでは".jpg"と".png"を対象としています）
    extensions = (".jpg", ".png")

    # 画像ファイルのパスを格納するリスト
    image_paths = []

    # フォルダ内のファイルを走査して画像ファイルのパスをリストに追加する
    for file_name in os.listdir(folder_path):
        if file_name.endswith(extensions):
            image_path = os.path.join(folder_path, file_name)
            image_paths.append(image_path)

    # 画像を順番に読み込んでリストに格納する
    images = []
    for image_path in image_paths:
        image = Image.open(image_path)
        images.append(image)

    # 画像のサイズを取得
    widths, heights = zip(*(i.size for i in images))

    # 結合後の画像のサイズを計算
    max_width = max(widths)
    total_height = sum(heights)

    # 空のキャンバスを作成
    combined_image = Image.new("RGB", (max_width, total_height))

    # 画像をキャンバスに貼り付ける
    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height

    # 画像を表示
    combined_image.save("/Users/matsumotokotarou/Desktop/combined_image.jpg")

# 画像を表示
batch_display("/Users/matsumotokotarou/My_Data/Local_Programing/workspace/labo/6_21/runs/detect/val6")
