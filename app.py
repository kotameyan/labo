from flask import Flask, render_template, request, redirect, url_for
from ultralytics import YOLO
from PIL import Image
import os, datetime, random, json

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
    result_image_filename = f'result_{target_filename}.png'  # 保存する画像ファイル名を設定
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
    result_json_filename = f'result_{target_filename}.json'  # 保存するJSONファイル名を設定
    file_path = os.path.join(app.root_path, 'static/predict/classes', result_json_filename)
    with open(file_path, 'w') as json_file:
        json.dump(all_classes, json_file, ensure_ascii=False, indent=4)  # JSONファイルとして保存



# ページ
# -----------------------------------------------------
# ファイルのアップロード画面
@app.route('/')
def index():
    return render_template('index.html')

# 解析結果の表示画面
@app.route('/result')
def result():
    # htmlに渡すデータ(img)を用意
    result_img = url_for('static', filename=f'predict/images/result_{target_filename}.png')

    # htmlに渡すデータ(json)を用意
    result_json_path = os.path.join(app.root_path, 'static/predict/classes', f'result_{target_filename}.json') # 解析結果（json）のパスを指定
    with open(result_json_path, 'r') as file:
        result_json = json.load(file) # JSONファイルの読み込み

    return render_template('result.html', result_img=result_img, result_json=result_json)



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
    count_classes(results) # 各クラスのカウントを保存
    return redirect(url_for('result'))



if __name__ == '__main__':
    app.run(debug=True, port=8888)
