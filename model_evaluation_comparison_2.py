import pandas as pd
import os
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns

# JSONファイルが保存されているディレクトリ
dir_path = "/Users/matsumotokotarou/My_Data/Local_Programing/workspace/labo/6_21/runs/detect/val_json"

# データフレームを保存するための空のリスト
dataframes = []

# ディレクトリ内の全てのJSONファイル名を取得
json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

# JSONファイル名を数値順に並べ替える
json_files.sort(key=lambda f: int(re.findall(r'\d+', f)[0]))

# 並べ替えたリストの全てのファイルをループ処理
for filename in json_files:
    print(f"Loading {filename}...")  # 読み込んでいるファイル名を出力
    # ファイルパスを作成
    file_path = os.path.join(dir_path, filename)
    # JSONファイルを読み込む
    with open(file_path, 'r') as f:
        data = json.load(f)
    # JSONデータをデータフレームに変換
    df = pd.json_normalize(data)
    # 新しい列を作成してグループ名（ファイル名）を格納
    group = re.findall(r'\d+', filename) # 数字を抽出
    df['group'] = group[0] if group else 'unknown' # 数字がなければ'unknown'とする
    # データフレームをリストに追加
    dataframes.append(df)

# 全てのデータフレームを一つに結合
result = pd.concat(dataframes, ignore_index=True)

# scoreをfloat型に変換
result['score'] = result['score'].astype(float)

# image_idとgroupでグループ化し、scoreの平均を計算
grouped = result.groupby(['image_id', 'group'])['score'].mean().reset_index()

# 結果を確認
print(grouped)

# データの可視化
plt.figure(figsize=(20,10)) # グラフのサイズを設定
sns.barplot(x='image_id', y='score', hue='group', data=grouped) # 棒グラフの作成

plt.title('Average Score per Image ID for Each Group') # タイトル
plt.xlabel('Image ID') # x軸のラベル
plt.ylabel('Average Score') # y軸のラベル

plt.xticks(rotation=90) # x軸のラベルを90度回転
plt.tight_layout() # レイアウトの調整
plt.show() # グラフの表示
