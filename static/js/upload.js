document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('resumeFile');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const removeFileBtn = document.getElementById('removeFile');
    const submitBtn = document.getElementById('submitBtn');
    const uploadForm = document.getElementById('uploadForm');
    const progressContainer = document.getElementById('progressContainer');
    const btnText = document.getElementById('btnText');
    const btnLoading = document.getElementById('btnLoading');

    // File input change handler
    fileInput.addEventListener('change', handleFileSelect);
    
    // Upload area click handler
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Drag and drop handlers
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Remove file handler
    removeFileBtn.addEventListener('click', removeFile);
    
    // Form submit handler
    uploadForm.addEventListener('submit', handleFormSubmit);

    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            displayFileInfo(file);
        }
    }

    function handleDragOver(event) {
        event.preventDefault();
        uploadArea.classList.add('dragover');
    }

    function handleDragLeave(event) {
        event.preventDefault();
        uploadArea.classList.remove('dragover');
    }

    function handleDrop(event) {
        event.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (isValidFile(file)) {
                fileInput.files = files;
                displayFileInfo(file);
            } else {
                alert('Please upload only PDF or DOCX files.');
            }
        }
    }

    function isValidFile(file) {
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
        return allowedTypes.includes(file.type);
    }

    function displayFileInfo(file) {
        fileName.textContent = file.name;
        fileInfo.style.display = 'block';
        uploadArea.style.display = 'none';
        submitBtn.disabled = false;
    }

    function removeFile() {
        fileInput.value = '';
        fileInfo.style.display = 'none';
        uploadArea.style.display = 'block';
        submitBtn.disabled = true;
    }

    function handleFormSubmit(event) {
        if (!fileInput.files.length) {
            event.preventDefault();
            alert('Please select a file to upload.');
            return;
        }

        // Show loading state
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        submitBtn.disabled = true;
        
        // Show progress bar
        progressContainer.style.display = 'block';
        animateProgress();
    }

    function animateProgress() {
        const progressBar = progressContainer.querySelector('.progress-bar');
        let width = 0;
        const interval = setInterval(() => {
            width += Math.random() * 15;
            if (width >= 100) {
                width = 100;
                clearInterval(interval);
            }
            progressBar.style.width = width + '%';
        }, 500);
    }

    // File size validation
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file && file.size > 16 * 1024 * 1024) { // 16MB
            alert('File size must be less than 16MB.');
            this.value = '';
            removeFile();
        }
    });
});
