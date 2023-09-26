import os

# アノテーションデータ群が入っているフォルダを指定する。
folder_path = "../datasets/rawdata"

for filename in os.listdir(folder_path):
    # フォルダ内の.txtファイルのみを処理する。
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            # 行をスペースで分割して数値に変換する。
            label, x, y, w, h = map(float, line.split())

            # ラベルが0の行をスキップする。
            if label == 0:
                continue

            # ラベルを1減らす。
            label -= 1

            # 新しい行を作成する。
            new_line = f"{int(label)} {x} {y} {w} {h}\n"
            new_lines.append(new_line)

        # ファイルに新しい行を書き込む。
        with open(file_path, "w") as file:
            file.writelines(new_lines)
