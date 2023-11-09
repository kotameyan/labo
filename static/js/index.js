// 画像をアップロードしたときにそれを表示する
function displayImage(input) {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            // テキストを非表示にし、画像を表示する
            document.getElementById('upload-text').style.display = 'none';
            const imgElement = document.getElementById('uploaded-image');
            imgElement.src = e.target.result;
            imgElement.style.display = 'block';

            // 枠線を点線から通常の線に変更する
            const uploadBox = document.querySelector('#upload-box');
            uploadBox.style.border = '3px solid #000';
        }
        reader.readAsDataURL(file);
    }
}

// キャンセルを押したときに画面をリロードする
function reloadPage() {
    window.location.reload(true);
}

// ローディングスピナーを起動する
document.getElementById('upload-form').addEventListener('submit', function () {
    document.getElementById('loading-overlay').style.display = 'flex'; // オーバーレイを表示
});
