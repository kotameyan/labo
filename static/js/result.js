// 画像の拡大表示
document.querySelectorAll('.expandable-image').forEach(function (element) {
    element.addEventListener('click', function () {
        var imgSrc;
        var cardTitle = element.closest('.card, .accordion-item').querySelector('.title-text').textContent;

        // エレメントがcanvasかimgかによって処理を分岐
        if (element.tagName === 'CANVAS') {
            // Canvasの内容をDataURLとして取得
            imgSrc = element.toDataURL();
        } else if (element.tagName === 'IMG') {
            // img要素のsrc属性を取得
            imgSrc = element.src;
        }

        // モーダル内のimg要素のsrcを設定
        document.getElementById('modalImage').src = imgSrc;
        // モーダルのタイトルを設定
        document.getElementById('imageModalLabel').textContent = cardTitle;
        // Bootstrapのモーダルインスタンスを取得し表示
        var imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
        imageModal.show();
    });
});



// 棒グラフ生成
document.addEventListener('DOMContentLoaded', function () {
    var charts = document.querySelectorAll('.growthChart');

    charts.forEach(function (ctx) {
        var data = resultClassesList;

        new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['flowering', 'growing_g', 'growing_w', 'nearly_m', 'mature', 'all'],
                datasets: [{
                    label: '成長段階別検出数',
                    data: [data.flowering, data.growing_g, data.growing_w, data.nearly_m, data.mature, data.all],
                    backgroundColor: ['white', 'yellowgreen', 'green', 'pink', 'red', 'grey'],
                    borderColor: ['black', 'black', 'black', 'black', 'black', 'black'],
                    borderWidth: 0.6
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            font: { size: 14 }
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 14 } }
                    }
                },
                plugins: {
                    legend: {
                        labels: { font: { size: 14 } },
                        onClick: function (e, legendItem, legend) {
                            // ここで何もしない
                        }
                    },
                    tooltip: { bodyFont: { size: 14 } }
                }
            }
        });
    });
});



// 折れ線グラフ生成
document.addEventListener('DOMContentLoaded', function () {
    var charts = document.querySelectorAll('.harvestChart');

    charts.forEach(function (canvas) {
        var ctx = canvas.getContext('2d');

        var data = resultHarvestsList;

        var dates = Object.keys(data);
        var counts = Object.values(data);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: '予測収穫数',
                    data: counts,
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            font: { size: 14 }
                        }
                    },
                    x: {
                        ticks: { font: { size: 14 } }
                    }
                },
                plugins: {
                    legend: {
                        labels: { font: { size: 14 } },
                        onClick: function (e, legendItem, legend) {
                            // ここで何もしない
                        }
                    },
                    tooltip: { bodyFont: { size: 14 } }
                }
            }
        });
    });
});
