function resetToHome() {
    // ホームページ（ルートパス）にリダイレクトし、ページをリロードする
    window.location.href = '/';
    window.location.reload(true); // 強制的にサーバーからリロード
  }
