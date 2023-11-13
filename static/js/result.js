// 画像の拡大表示
document.querySelectorAll('.expandable-image').forEach(function (img) {
    img.addEventListener('click', function () {
        // img要素のsrc属性を取得
        var imgSrc = img.src;
        // img要素が属するカードまたはアコーディオンアイテムのタイトルテキストを取得
        var cardTitle = img.closest('.card, .accordion-item').querySelector('.title-text').textContent;
        // モーダル内のimg要素のsrcをカードの画像のsrcに設定
        document.getElementById('modalImage').src = imgSrc;
        // モーダルのタイトルを設定
        document.getElementById('imageModalLabel').textContent = cardTitle;
        // Bootstrapのモーダルインスタンスを取得し表示
        var imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
        imageModal.show();
    });
});
