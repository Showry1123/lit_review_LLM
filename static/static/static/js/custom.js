document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('userfileInput');
    const progressBar = document.querySelector('.progress-bar');
    const progressContainer = document.getElementById('uploadProgressContainer');
    const errorContainer = document.getElementById('JSerror');
    const errorDismissBtn = document.getElementById('JSerror_dismiss');
    const submitBtn = document.getElementById('btnSubmit');
    const uploadForm = document.getElementById('uploadForm');

    fileInput.addEventListener('change', function() {
        validateFileSize();
    });

    errorDismissBtn.addEventListener('click', function() {
        errorContainer.style.display = 'none';
    });

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        if (!validateFileSize()) {
            uploadFile();
        }
    });

    function validateFileSize() {
        const file = fileInput.files[0];
        if (file && file.size > 200 * 1024 * 1024) {
            showError('The chosen file is too large, please choose a smaller file.');
            fileInput.value = '';
            return true;
        }
        return false;
    }

    function uploadFile() {
        const formData = new FormData(uploadForm);
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', function(evt) {
            if (evt.lengthComputable) {
                const percentComplete = Math.round((evt.loaded / evt.total) * 100);
                updateProgressBar(percentComplete);
            }
        });

        xhr.open('POST', uploadForm.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 400) {
                const blob = new Blob([xhr.response], { type: 'text/csv' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'conclusions.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                hideProgressBar();
            } else {
                showError('Could not process the file.');
                hideProgressBar();
            }
        };

        xhr.onerror = function() {
            showError('Could not process the file.');
            hideProgressBar();
        };

        xhr.send(formData);
        showProgressBar();
    }

    function showError(message) {
        errorContainer.style.display = 'block';
        errorContainer.querySelector('strong').textContent = message;
    }

    function hideError() {
        errorContainer.style.display = 'none';
        errorContainer.querySelector('strong').textContent = '';
    }

    function showProgressBar() {
        progressContainer.style.display = 'block';
        submitBtn.disabled = true;
    }

    function updateProgressBar(percentage) {
        progressBar.style.width = percentage + '%';
        progressBar.textContent = percentage + '%';
    }

    function hideProgressBar() {
        progressContainer.style.display = 'none';
        submitBtn.disabled = false;
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';
    }
});
