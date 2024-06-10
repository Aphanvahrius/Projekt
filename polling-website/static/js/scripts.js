document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('pollForm');
    
    form.addEventListener('submit', function (event) {
        const fileInput = document.getElementById('attachment');
        const file = fileInput.files[0];

        if (file) {
            const maxFileSize = 25 * 1024 * 1024; // 25MB in bytes
            const allowedExtensions = ['pdf', 'doc', 'docx', 'jpg', 'png'];
            const fileExtension = file.name.split('.').pop().toLowerCase();

            if (file.size > maxFileSize) {
                alert('File size should not exceed 25MB.');
                event.preventDefault();
                return;
            }

            if (!allowedExtensions.includes(fileExtension)) {
                alert('Invalid file type. Only PDF, DOC, DOCX, JPG, and PNG files are allowed.');
                event.preventDefault();
                return;
            }
        }
    });
});
