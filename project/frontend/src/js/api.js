const API = {
    baseURL: 'http://127.0.0.1:5000',

    async uploadPDF(file, pages = null) {
        const formData = new FormData();
        formData.append('file', file);

        let url = `${this.baseURL}/pdf/upload`;
        if (pages) {
            url += `?pages=${encodeURIComponent(pages)}`;
        }

        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Upload failed');
        }

        return response.json();
    },

    // Add more API methods as needed
};