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

        
        const items = e.dataTransfer.items;
        let folderDetected = false;

        for (let i = 0; i < items.length; i++) {
            if (items[i].webkitGetAsEntry && items[i].webkitGetAsEntry().isDirectory) {
                folderDetected = true;
                break;
            }
        }

        if (folderDetected) {
            fileInput.value = '';
        } else {
            const file = e.dataTransfer.files[0];
            fileInput.files = e.dataTransfer.files;
            displayFileName(file);
        }
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
