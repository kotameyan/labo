# エポック数とモデル精度の相関を確認する
# --------------------------------

# 必要な物をインポート
from ultralytics import YOLO
import labo

# エポック数を変えながらモデル作りを繰り返す(3,6,9,12,15)
for i in range(3,16,3):

    # ベースとなるモデルの読み込み
    model = YOLO('yolov8x.pt')

    # ベースとなるモデルに追加学習
    model.train(data='data.yaml', epochs=i)

    # モデルの精度を検証し、保存
    metrics = model.val(save_json=True)

# 検証結果のJSONファイルをval_jsonフォルダに集める
detect_folder_path = '/Users/matsumotokotarou/My_Data/Local_Programing/workspace/labo/6_27/runs/detect'
labo.save_val_json(detect_folder_path)

# val_jsonフォルダを使って解析する
val_json_path = '/Users/matsumotokotarou/My_Data/Local_Programing/workspace/labo/6_27/runs/detect/val_json'
labo.analyze_val_json(val_json_path)
