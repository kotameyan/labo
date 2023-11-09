import os
import shutil

def clean_and_keep(directory):
    # ディレクトリ内の全てのファイルとフォルダを削除
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # .gitkeep ファイルを作成
    open(os.path.join(directory, '.gitkeep'), 'a').close()

# 'uploads' と 'predict' フォルダ内の履歴データをクリーンアップ
directories_to_clean = ['static/uploads', 'static/predict/classes/graph', 'static/predict/classes/json', 'static/predict/harvests/graph', 'static/predict/harvests/json', 'static/predict/images']

for directory in directories_to_clean:
    clean_and_keep(directory)

print("履歴データのクリーンアップが完了し、.gitkeepファイルが追加されました。")
