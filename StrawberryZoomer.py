import os, re
import cv2
from PIL import Image

# YOLO形式のアノテーションデータを1つ取ってきて、Pythonの辞書型に変換する関数
def parse_yolo_format(img_path, label_path):
    # 画像サイズを読み取る
    img = cv2.imread(img_path)
    img_height, img_width = img.shape[:2]

    # アノテーションデータを開く
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # アノテーションデータの情報をPythonの辞書型に格納する
    # 辞書型に入るデータは割合ではなく実際の長さ
    bboxes = []
    for line in lines:
        class_id, x_center_ratio, y_center_ratio, width_ratio, height_ratio = map(float, line.split())

        # 幅や高さが0のバウンディングボックスは無視する
        if width_ratio == 0 or height_ratio == 0:
            continue

        x_center = x_center_ratio * img_width
        y_center = y_center_ratio * img_height
        width = width_ratio * img_width
        height = height_ratio * img_height
        bbox = {
            'class_id': int(class_id),
            'x_center': x_center,
            'y_center': y_center,
            'width': width,
            'height': height
        }
        bboxes.append(bbox)

    return bboxes

# バウンディングボックスのデータを元に、そのバウンディボックスの角の座標を特定する関数
def calculate_bbox_corners(bbox):
    # 引数になっているデータの中身を変数に格納
    x_center = bbox['x_center']
    y_center = bbox['y_center']
    width = bbox['width']
    height = bbox['height']

    # 左上から時計回りにbbox_corners_0 ~ 3 とする(openCVに合わせて左上が(0,0))
    bbox_corners = {
        0: {'x': x_center - width / 2, 'y': y_center - height / 2},  # 左上
        1: {'x': x_center + width / 2, 'y': y_center - height / 2},  # 右上
        2: {'x': x_center + width / 2, 'y': y_center + height / 2},  # 右下
        3: {'x': x_center - width / 2, 'y': y_center + height / 2}   # 左下
    }

    return bbox_corners

# バウンディングボックスのデータを元に、画像の切り取り範囲を計算する関数
def calculate_crop_img_size(bbox, img_path):
    # 画像サイズを読み取る
    img = cv2.imread(img_path)
    img_height, img_width = img.shape[:2]

    # 引数になっているデータの中身を変数に格納
    x_center = bbox['x_center']
    y_center = bbox['y_center']
    width = bbox['width']
    height = bbox['height']

    # 切り取る領域の座標を指定(min: 左上、max: 右下)
    x_min = max(int(x_center - (width / 2) * 1.5), 0)
    y_min = max(int(y_center - (height / 2) * 1.5), 0)
    x_max = min(int(x_center + (width / 2) * 1.5), img_width)
    y_max = min(int(y_center + (height / 2) * 1.5), img_height)

    # 座標のいずれかがマイナスの場合、警告を表示
    if x_min < 0 or y_min < 0 or x_max < 0 or y_max < 0:
        print(f"警告: 計算された切り取り範囲のいずれかがマイナスです。x_min: {x_min}, y_min: {y_min}, x_max: {x_max}, y_max: {y_max}")

    # 結果を出力
    crop_img_size = {'x_min': x_min, 'y_min': y_min, 'x_max': x_max, 'y_max': y_max}
    return crop_img_size

# 画像切り取り、バウンディボックス付加、アノテーションデータ生成を行う関数
def generate_new_data(img_path, crop_img_size, bbox_corners, bbox, base_name, index):
    '''
    0, 出力フォルダの確認
    '''
    # 出力するフォルダパスをグローバル変数から読み込む
    global output_images_path
    global output_labels_path
    global output_checks_path

    '''
    1, 画像の切り取り
    '''
    # 切り取る対象の画像を読み込む
    img = cv2.imread(img_path)

    # 切り取る範囲を取得
    y_min = crop_img_size['y_min']
    y_max = crop_img_size['y_max']
    x_min = crop_img_size['x_min']
    x_max = crop_img_size['x_max']

    # 切り取りを実行
    cropped_img = img[y_min:y_max, x_min:x_max]

    # 切り取った画像を保存
    new_filename = f'{base_name}_zoom_{index}.png'
    new_filename_path = os.path.join(output_images_path, new_filename)
    cv2.imwrite(new_filename_path, cropped_img)

    '''
    2, バウンディボックスの付加
    '''
    # 描画するバウンディボックスの左上と右下の座標を取得
    x1 = int(bbox_corners[0]['x'] - x_min)
    y1 = int(bbox_corners[0]['y'] - y_min)
    x2 = int(bbox_corners[2]['x'] - x_min)
    y2 = int(bbox_corners[2]['y'] - y_min)

    # 画像にバウンディボックスを描画
    cropped_img_with_bbox = cv2.rectangle(cropped_img, (x1,y1), (x2,y2), (0,255,255), 2)

    # バウンディボックスを付加した画像を保存する
    new_filename = f'{base_name}_zoom_{index}.png'
    new_filename_path = os.path.join(output_checks_path, new_filename)
    cv2.imwrite(new_filename_path, cropped_img_with_bbox)

    '''
    3, アノテーションデータの生成
    '''
    # 現在の画像サイズを取得
    cropped_img_height, cropped_img_width = cropped_img.shape[:2]

    # 新しいアノテーションデータに入れる内容を計算
    new_x_center = (x1 + x2) / 2.0 / cropped_img_width
    new_y_center = (y1 + y2) / 2.0 / cropped_img_height
    new_width = (x2 - x1) / cropped_img_width
    new_height = (y2 - y1) / cropped_img_height

    # 新しいアノテーションデータを生成
    new_bbox = {
        'class_id': bbox['class_id'],
        'x_center': new_x_center,
        'y_center': new_y_center,
        'width': new_width,
        'height': new_height
    }

    # 新しいアノテーションデータをテキストファイルに保存
    new_filename = f'{base_name}_zoom_{index}.txt'
    new_filename_path = os.path.join(output_labels_path, new_filename)
    with open(new_filename_path, 'w') as file:
        file.write(f"{new_bbox['class_id']} {new_bbox['x_center']} {new_bbox['y_center']} {new_bbox['width']} {new_bbox['height']}\n")


'''
ここからメインの処理
'''

# パスの設定
input_path = '../../datasets/rawdata'
input_images_path = os.path.join(input_path, 'images')
input_labels_path = os.path.join(input_path, 'labels')

output_path = '../../datasets/rawdata_zoom'
output_images_path = os.path.join(output_path, 'images')
output_labels_path = os.path.join(output_path, 'labels')
output_checks_path = os.path.join(output_path, 'checks')

# 新しく作るデータのベースネーム(リスト)を作成
input_images_names = os.listdir(input_images_path) # imagesフォルダ内のファイル名を取得
base_names = [os.path.splitext(input_images_name)[0] for input_images_name in input_images_names] # 拡張子をとってベースネームとする
base_names = sorted(base_names, key=lambda x: [int(text) if text.isdigit() else text for text in re.split('([0-9]+)', x)]) # 並び替え

# 全ての画像＆アノテーションデータに対して新データ生成を行う
for base_name in base_names:

    # 対象の画像ファイルとテキストファイルをセット
    img_path = os.path.join(input_images_path, f'{base_name}.png')
    label_path = os.path.join(input_labels_path, f'{base_name}.txt')

    # テキストファイル内のアノテーションデータをPythonの辞書型にフォーマット
    bboxes = parse_yolo_format(img_path, label_path)

    # バウンディボックスの数だけ新データ生成を行う
    for index, bbox in enumerate(bboxes):

        # バウンディボックスの角を計算
        bbox_corners = calculate_bbox_corners(bbox)

        # 画像の切り取り範囲を計算
        crop_img_size = calculate_crop_img_size(bbox, img_path)

        # 新しい'切り取り画像'、'バウンディボックス付加画像'、'アノテーションデータ'を生成
        generate_new_data(img_path, crop_img_size, bbox_corners, bbox, base_name, index)
