const fileUploadContainer = document.getElementById('fileUploadContainer');
const fileInput = document.getElementById('fileInput');
const fileNameDisplay = document.getElementById('fileName');

if (fileUploadContainer !== null){
    fileUploadContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadContainer.classList.add('dragging');
    });
    
    fileUploadContainer.addEventListener('dragleave', () => {
        fileUploadContainer.classList.remove('dragging');
    });
    
    fileUploadContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadContainer.classList.remove('dragging');
        const file = e.dataTransfer.files[0];
        fileInput.files = e.dataTransfer.files;
        displayFileName(file);
    });
    
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        displayFileName(file);
    });
    
    function displayFileName(file) {
        if (file) {
        fileNameDisplay.textContent = file.name;
        }
    }
}
