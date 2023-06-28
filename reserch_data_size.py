# 訓練データ数とモデル精度の相関を確認する
# ーーーーーーーーーーーーーーーーーーーー

# 必要なものをインポート
from ultralytics import YOLO
import torch
from pathlib import Path

# データセットのリストを作成
data_list = [f'datasets_path/data_{i}.yaml' for i in range(1, 7)]

# 追加学習
for i, data in enumerate(data_list, start=1):

    # 以前のモデルを読み込む
    if i == 1:
        model = YOLO('yolov8x.pt')
    else:
        model = YOLO(model_path)

    # 学習 → モデルを保存
    model.train(data=data, epochs=3)

    # 評価 → 結果を保存
    model.val(save_json=True)

    # 次の追加学習に向けて、今作ったモデルを呼び出すためのパスを更新する
    if i==1:
        model_path = 'runs/detect/train/weights/best.pt'
    else:
        model_path = f'runs/detect/train{i}/weights/best.pt'
