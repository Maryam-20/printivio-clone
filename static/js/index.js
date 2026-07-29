// --- UPLOAD DESIGN ELEMENTS ---
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
    if (fileNameEl) fileNameEl.textContent = file.name;
    if (dropzone) dropzone.style.display = 'none';
    if (fileList) fileList.style.display = 'block';
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Upload';
        submitBtn.dataset.state = 'ready';
    }
}

function resetToDropzone() {
    selectedFile = null;
    if (fileInput) fileInput.value = '';
    if (dropzone) dropzone.style.display = 'flex';
    if (fileList) fileList.style.display = 'none';
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Upload';
        submitBtn.dataset.state = '';
    }
}

// --- SAFE EVENT LISTENERS (Only runs if elements exist on the page) ---
if (dropzone && fileInput) {
    dropzone.addEventListener('click', () => fileInput.click());

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
}

if (fileInput) {
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) showFileSelected(this.files[0]);
    });
}

if (removeBtn) {
    removeBtn.addEventListener('click', resetToDropzone);
}

if (submitBtn && form) {
    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();

        // If already uploaded, proceed to cart
        if (submitBtn.dataset.state === 'uploaded') {
            window.location.href = submitBtn.dataset.cartUrl;
            return;
        }

        if (!selectedFile) return;

        const csrfTokenElement = form.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenElement) {
            alert('Security token missing. Please refresh.');
            return;
        }

        const formData = new FormData();
        formData.append('design_file', selectedFile);
        formData.append('csrfmiddlewaretoken', csrfTokenElement.value);

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
}

// --- GLOBAL PRICE CALCULATION FUNCTION 
// LISTEN TO THE SELECT QUANTITY OPTIONS ON CHANGE TO UPDATE PRICE 
window.updatePrice = function(selectElement) {
    const quantityValue = selectElement.value;
    const productId = selectElement.dataset.productId;

    fetch(`/products/calculate-price/${productId}/?quantity=${quantityValue}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const priceDisplay = document.getElementById(`price-display-${productId}`);
            if (priceDisplay) {
                priceDisplay.innerText = `₦${parseFloat(data.calculated_price).toLocaleString('en-NG', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
            }
        })
        .catch(error => console.error('Error handling price update:', error));
};
