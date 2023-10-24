// 画像の拡大表示
document.getElementById('resultImage').addEventListener('click', function() {
    const overlay = document.getElementById('overlay');
    const enlargedImg = document.getElementById('enlargedImage');
    enlargedImg.src = this.src;
    overlay.style.display = "flex";
});

// オーバーレイをクリックすると画像の拡大表示を閉じる
function closeOverlay() {
    const overlay = document.getElementById('overlay');
    overlay.style.display = "none";
}
