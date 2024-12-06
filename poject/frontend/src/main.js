const pagesInput = document.getElementById('pagesInput');

uploadForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const file = pdfFile.files[0];
  const pagesValue = pagesInput.value.trim();
  let url = 'http://127.0.0.1:5000/pdf/upload';
  if (pagesValue) {
    url += `?pages=${encodeURIComponent(pagesValue)}`;
  }

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(url, {
      method: 'POST',
      body: formData
  });
});
