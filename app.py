from flask import Flask, render_template, request, redirect, url_for
from ultralytics import YOLO
from PIL import Image
import os, datetime, random, json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

app = Flask(__name__)



# グローバル変数
# -----------------------------------------------------
target_filename = ''
target_filename_with_extention = ''



# 関数
# -----------------------------------------------------
# ターゲットファイル名を生成
def generate_target_filename(filename):
    global target_filename
    global target_filename_with_extention

    # ベースとなるファイル名を生成
    dt_now = datetime.datetime.now()  # 日付情報を取得
    timestamp = dt_now.strftime("%m_%d_%H_%M")  # フォーマットを整えてタイムスタンプを作成
    random_num = f"{random.randint(0, 9999):04d}"  # 0から9999までのランダムな4桁の整数を生成
    target_filename = f"{timestamp}_{random_num}"  # グローバル変数を変更

    # 拡張子を取り出してセット
    file_extension = os.path.splitext(filename)[1] # ファイルの拡張子を取得
    target_filename_with_extention = f"{target_filename}{file_extension}" # グローバル変数を変更

# （推論結果から）画像を保存
def save_image(results):
    # 推論結果の画像を作成
    r = results[0]
    im_array = r.plot()  # plotメソッドで推論結果の画像をレンダリング
    im = Image.fromarray(im_array[..., ::-1])  # BGRからRGBに変換

    # 推論結果の画像を保存
    result_image_filename = f'result_images_{target_filename}.png'  # 保存する画像ファイル名を設定
    file_path = os.path.join(app.root_path, 'static/predict/images', result_image_filename)
    im.save(file_path)  # 画像を保存

# （推論結果から）各クラスをカウント
def count_classes(results):
    # 各クラスの個数をカウント
    r = results[0]  # 1枚の画像の推論結果を取得
    det = r.boxes  # boxes属性からバウンディングボックスを取得

    # すべてのクラスをキーとして持つ辞書を初期化
    all_classes = {
        "flowering": 0,
        "growing_g": 0,
        "growing_w": 0,
        "nearly_m": 0,
        "mature": 0
    }

    for c in det.cls.unique():  # ユニークなクラスIDをループ
        n = (det.cls == c).sum().item()  # 各クラスの検出をカウントし、Tensorをintに変換
        class_name = r.names[int(c)]  # クラス名を取得
        all_classes[class_name] = n  # クラスの個数を辞書に保存

    # すべてのクラスの数を合計
    all_classes["all"] = sum(all_classes.values())

    # 各クラスの個数をJSONファイルとして保存
    result_json_filename = f'result_classes_{target_filename}.json'  # 保存するJSONファイル名を設定
    file_path = os.path.join(app.root_path, 'static/predict/classes/json', result_json_filename)
    with open(file_path, 'w') as json_file:
        json.dump(all_classes, json_file, ensure_ascii=False, indent=4)  # JSONファイルとして保存

# （推論結果から）収穫時期の予測
def predict_harvest(result_classes_path):
    # JSONファイルを読み込み、Pythonの辞書として取得
    with open(result_classes_path, 'r') as file:
        data = json.load(file)

    # 現在の日付を取得
    today = datetime.date.today()

    # 各成長段階から成熟するまでの日数
    days_to_mature = {
        "flowering": 40,
        "growing_g": 20,
        "growing_w": 10,
        "nearly_m": 5,
        "mature": 0
    }

    # 成熟する日付を予測
    harvest_dates = {}
    for stage, days in days_to_mature.items():
        harvest_date = today + datetime.timedelta(days=days)
        if data[stage] > 0:
            if harvest_date in harvest_dates:
                harvest_dates[harvest_date] += data[stage]
            else:
                harvest_dates[harvest_date] = data[stage]

    # 日付の小さい方から順にソート
    sorted_harvest_dates = dict(sorted(harvest_dates.items()))

    # JSON形式で出力
    output = {date.strftime('%m/%d'): count for date, count in sorted_harvest_dates.items()}

    # JSONファイルとして保存
    result_json_filename = f'result_harvests_{target_filename}.json'
    file_path = os.path.join(app.root_path, 'static/predict/harvests/json', result_json_filename)
    with open(file_path, 'w') as json_file:
        json.dump(output, json_file, ensure_ascii=False, indent=4)

# classesから成長段階のグラフを作成
def create_classes_graph():
    # JSONファイルへのパスを指定
    json_file_path = os.path.join(app.root_path, 'static/predict/classes/json', f'result_classes_{target_filename}.json')

    # JSONファイルを読み込む
    with open(json_file_path, 'r') as json_file:
        data_json = json.load(json_file)

    # JSONデータをデータフレームに変換
    df = pd.DataFrame(list(data_json.items()), columns=['成長段階', '検出個数'])

    # 各棒グラフの色を指定
    colors = ['white', 'yellowgreen', 'green', 'pink', 'red', 'gray']
    edge_colors = ['black'] * len(colors)  # 全ての棒グラフに黒いエッジカラーを追加

    # 棒グラフの描画
    sns.barplot(x='成長段階', y='検出個数', data=df, palette=colors, edgecolor=edge_colors)

    # グラフを画像として保存
    plt.savefig(f'static/predict/classes/graph/result_classes_{target_filename}.png')

    # グラフを閉じる
    plt.close()

# harvestsから収穫時期のグラフを作成
def create_harvests_graph():
    # JSONファイルへのパスを指定
    json_file_path = os.path.join(app.root_path, 'static/predict/harvests/json', f'result_harvests_{target_filename}.json')

    # JSONファイルを読み込む
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # 日付と予測収穫個数をリストに分割
    dates = list(data.keys())
    harvest_counts = list(data.values())

    # 折れ線グラフを作成
    plt.figure(figsize=(10, 6))
    plt.plot(dates, harvest_counts, marker='o', linestyle='-', color='b', markersize=8)

    # 軸ラベル
    plt.xlabel("日付", fontsize=14)
    plt.ylabel("予測収穫個数", fontsize=14)

    # 日付をX軸に表示
    plt.xticks(rotation=45)

    # グリッド線を追加（オプション）
    plt.grid(True, linestyle='--', alpha=0.6)

    # グラフを画像として保存
    plt.savefig(f'static/predict/harvests/graph/result_harvests_{target_filename}.png')

    # グラフを閉じる
    plt.close()



# ページ
# -----------------------------------------------------
# ファイルのアップロード画面
@app.route('/')
def index():
    return render_template('index.html')

# 解析結果の表示画面
@app.route('/result')
def result():
    # htmlに渡すデータ（images）を用意
    result_images = url_for('static', filename=f'predict/images/result_images_{target_filename}.png')

    # htmlに渡すデータ(classes)を用意
    result_classes = url_for('static', filename=f'predict/classes/graph/result_classes_{target_filename}.png')

    # htmlに渡すデータ(harvests)を用意
    # result_harvests_path = os.path.join(app.root_path, 'static/predict/harvests/json', f'result_harvests_{target_filename}.json') # harvestsのパスを指定
    # with open(result_harvests_path, 'r') as file:
    #     result_harvests = json.load(file) # JSONファイルの読み込み
    result_harvests = url_for('static', filename=f'predict/harvests/graph/result_harvests_{target_filename}.png')

    return render_template('result.html', result_images=result_images, result_classes=result_classes, result_harvests=result_harvests)



# 機能
# -----------------------------------------------------
# アップロードされたファイルの保存
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file'] # ファイルを取得
    generate_target_filename(file.filename) # 保存するときのファイル名を生成
    file.save(os.path.join('static/uploads', target_filename_with_extention)) # ファイルをアップロードフォルダに保存
    return redirect(url_for('predict'))

# 推論
@app.route('/predict')
def predict():
    model = YOLO('models/best.pt') # 推論するmodelの読み込み

    file_path = os.path.join(app.root_path, 'static/uploads', target_filename_with_extention)
    results = model(file_path) # 推論の実行

    save_image(results) # 推論結果画像を保存

    count_classes(results) # 各クラスのカウントのJSONを作成
    create_classes_graph() # 各クラスのカウントのグラフを作成

    result_classes_path = os.path.join(app.root_path, 'static/predict/classes/json', f'result_classes_{target_filename}.json') # classesのJSONファイルのパスを指定
    predict_harvest(result_classes_path) # 収穫時期の予測のJSONを作成
    create_harvests_graph() # 収穫時期の予測のグラフを作成

    return redirect(url_for('result'))



if __name__ == '__main__':
    app.run(debug=True, port=8888)
