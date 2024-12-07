class PDFHandler {
    constructor() {
        this.form = document.getElementById('uploadForm');
        this.fileInput = document.getElementById('pdfFile');
        this.pagesInput = document.getElementById('pagesInput');
        
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleUpload();
        });
    }

    async handleUpload() {
        try {
            showToast('Uploading PDF...', 'info');
            
            const formData = new FormData();
            formData.append('file', this.fileInput.files[0]);
            
            const pagesValue = this.pagesInput.value.trim();
            let url = '/pdf/upload';
            if (pagesValue) {
                url += `?pages=${encodeURIComponent(pagesValue)}`;
            }

            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (response.ok) {
                showToast('PDF processed successfully!', 'success');
                this.displayContent(data.content);
            } else {
                throw new Error(data.error || 'Failed to process PDF');
            }
        } catch (error) {
            showToast(error.message, 'error');
            console.error('Upload error:', error);
        }
    }

    isplayContent(content) {
        const viewer = document.getElementById('document-viewer');
        if (!viewer) {
            console.error('Document viewer element not found');
            return;
        }
        
        // Convert markdown to HTML if needed
        viewer.innerHTML = content;
        
        // Show the viewer section
        viewer.classList.remove('hidden');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PDFHandler();
});