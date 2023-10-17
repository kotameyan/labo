function previewImage() {
    const fileInput = document.getElementById('strawberryImage');
    const previewContainer = document.querySelector('.upload-label');
    const uploadPrompt = document.getElementById('uploadPrompt');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.addEventListener('load', function () {
            const img = new Image();
            img.src = reader.result;
            img.onload = function() {
                previewContainer.style.backgroundImage = 'url(' + reader.result + ')';
                uploadPrompt.style.display = 'none';
            }
        });
        reader.readAsDataURL(file);
    } else {
        previewContainer.style.height = '300px';
        uploadPrompt.style.display = 'inline';
    }
}

document.getElementById('cancelBtn').addEventListener('click', function() {
    location.reload();
});
