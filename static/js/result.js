// 以下はダミーデータとしての解析結果を示しています。
// 実際の解析結果に基づくデータに変更する必要があります。
// const analysisResult = {
//     totalStrawberries: 100,
//     flowering: 20,
//     growing_g: 30,
//     growing_w: 20,
//     nearly_m: 10,
//     mature: 20,
//     schedule: "3日後に20個のいちごが完熟する見込みです。"
// }

// function displayAnalysisResults() {
//     document.getElementById('totalStrawberries').textContent = analysisResult.totalStrawberries;
//     document.getElementById('floweringCount').textContent = analysisResult.flowering;
//     document.getElementById('growingGCount').textContent = analysisResult.growing_g;
//     document.getElementById('growingWCount').textContent = analysisResult.growing_w;
//     document.getElementById('nearlyMCount').textContent = analysisResult.nearly_m;
//     document.getElementById('matureCount').textContent = analysisResult.mature;
//     document.getElementById('schedule').textContent = analysisResult.schedule;
// }

// document.addEventListener('DOMContentLoaded', displayAnalysisResults);

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
