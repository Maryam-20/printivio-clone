(function() {
    const dropzone = document.getElementById('uploadDropzone');
    const fileInput = document.getElementById('designFileInput');
    const fileList = document.getElementById('uploadFileList');
    const fileNameEl = document.getElementById('uploadFileName');
    const removeBtn = document.getElementById('removeFileBtn');
    const submitBtn = document.getElementById('uploadSubmitBtn');
    const form = document.getElementById('uploadDesignForm');

    let selectedFile = null;

    function showFileSelected(file) {
        selectedFile = file;
        fileNameEl.textContent = file.name;
        dropzone.style.display = 'none';
        fileList.style.display = 'block';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Upload';
        submitBtn.dataset.state = 'ready';
    }

    function resetToDropzone() {
        selectedFile = null;
        fileInput.value = '';
        dropzone.style.display = 'flex';
        fileList.style.display = 'none';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Upload';
        submitBtn.dataset.state = '';
    }

    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) showFileSelected(this.files[0]);
    });

    dropzone.addEventListener('dragover', function(e) {
        e.preventDefault();
        dropzone.style.backgroundColor = '#F0EDE0';
    });
    dropzone.addEventListener('dragleave', function() {
        dropzone.style.backgroundColor = '';
    });
    dropzone.addEventListener('drop', function(e) {
        e.preventDefault();
        dropzone.style.backgroundColor = '';
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            showFileSelected(e.dataTransfer.files[0]);
        }
    });

    removeBtn.addEventListener('click', resetToDropzone);

    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();

        // If already uploaded, this click means "Proceed to Cart"
        if (submitBtn.dataset.state === 'uploaded') {
            window.location.href = submitBtn.dataset.cartUrl;
            return;
        }

        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('design_file', selectedFile);
        formData.append('csrfmiddlewaretoken', form.querySelector('[name=csrfmiddlewaretoken]').value);

        submitBtn.disabled = true;
        submitBtn.textContent = 'Uploading...';

        fetch(form.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Proceed to Cart';
                submitBtn.dataset.state = 'uploaded';
                submitBtn.dataset.cartUrl = data.cart_url;
            } else {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Upload';
                alert(data.error || 'Upload failed. Please try again.');
            }
        })
        .catch(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Upload';
            alert('Something went wrong. Please try again.');
        });
    });
})();