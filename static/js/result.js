// 画像の拡大表示
document.querySelectorAll('.card-expandable').forEach(function (card) {
    card.addEventListener('click', function () {
        // カード内のimg要素のsrc属性を取得
        var imgSrc = card.querySelector('img').src;
        // カードのタイトルテキストを取得（バッジを除外）
        var cardTitle = card.querySelector('.title-text').textContent;
        // モーダル内のimg要素のsrcをカードの画像のsrcに設定
        document.getElementById('modalImage').src = imgSrc;
        // モーダルのタイトルを設定
        document.getElementById('imageModalLabel').textContent = cardTitle;
        // Bootstrapのモーダルインスタンスを取得し表示
        var imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
        imageModal.show();
    });
});
