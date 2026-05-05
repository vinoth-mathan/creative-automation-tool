document.addEventListener('DOMContentLoaded', () => {
    const brandSelect = document.getElementById('brand-select');
    const dealerContainer = document.getElementById('dealer-list-container');
    const dealerList = document.getElementById('dealer-list');
    const selectAllBtn = document.getElementById('select-all');
    const dropZone = document.getElementById('drop-zone');
    const bgInput = document.getElementById('bg-input');
    const preview = document.getElementById('preview');
    const generateBtn = document.getElementById('generate-btn');
    const status = document.getElementById('status');
    const downloadLink = document.getElementById('download-link');

    let selectedFile = null;

    // Load Brands
    fetch('/api/accounts')
        .then(res => res.json())
        .then(brands => {
            brands.forEach(brand => {
                const opt = document.createElement('option');
                opt.value = brand.id;
                opt.textContent = brand.name;
                brandSelect.appendChild(opt);
            });
        });

    // Brand Change
    brandSelect.addEventListener('change', (e) => {
        const brandId = e.target.value;
        if (!brandId) {
            dealerContainer.classList.add('hidden');
            return;
        }

        fetch(`/api/dealerships?account_id=${brandId}`)
            .then(res => res.json())
            .then(dealers => {
                dealerList.innerHTML = '';
                dealers.forEach(dealer => {
                    const label = document.createElement('label');
                    label.className = 'checkbox-container';
                    label.innerHTML = `
                        <input type="checkbox" value="${dealer.id}" class="dealer-checkbox">
                        <span class="checkmark"></span>
                        ${dealer.name}
                    `;
                    dealerList.appendChild(label);
                });
                dealerContainer.classList.remove('hidden');
                validateForm();
            });
    });

    // Select All
    selectAllBtn.addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('.dealer-checkbox');
        const allChecked = Array.from(checkboxes).every(cb => cb.checked);
        checkboxes.forEach(cb => cb.checked = !allChecked);
        validateForm();
    });

    // Upload Logic
    dropZone.addEventListener('click', () => bgInput.click());
    
    bgInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--border)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        handleFile(e.dataTransfer.files[0]);
    });

    function handleFile(file) {
        if (file && file.type.startsWith('image/')) {
            selectedFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result;
                preview.classList.remove('hidden');
                dropZone.querySelector('p').classList.add('hidden');
            };
            reader.readAsDataURL(file);
            validateForm();
        }
    }

    function validateForm() {
        const hasDealers = document.querySelectorAll('.dealer-checkbox:checked').length > 0;
        const hasFile = selectedFile !== null;
        generateBtn.disabled = !(hasDealers && hasFile);
    }

    // Listen for dealer checkbox changes
    dealerList.addEventListener('change', validateForm);

    // Generate
    generateBtn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('background', selectedFile);
        
        const dealerIds = Array.from(document.querySelectorAll('.dealer-checkbox:checked')).map(cb => cb.value);
        dealerIds.forEach(id => formData.append('dealer_ids', id));

        const sizes = Array.from(document.querySelectorAll('.size-options input:checked')).map(cb => cb.value);
        sizes.forEach(size => formData.append('sizes', size));

        formData.append('use_logo', document.getElementById('use-logo').checked);
        formData.append('logo_variant', document.querySelector('input[name="logo-variant"]:checked').value);

        generateBtn.disabled = true;
        status.textContent = 'Generating creatives... please wait.';
        downloadLink.classList.add('hidden');

        fetch('/api/generate', {
            method: 'POST',
            body: formData
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => { throw new Error(err.error || 'Server error'); });
            }
            return res.blob();
        })
        .then(blob => {
            status.textContent = 'Generation complete!';
            const url = window.URL.createObjectURL(blob);
            downloadLink.href = url;
            downloadLink.download = 'creatives.zip';
            downloadLink.classList.remove('hidden');
        })
        .catch(err => {
            status.textContent = 'Error: ' + err.message;
            console.error(err);
        })
        .finally(() => {
            generateBtn.disabled = false;
        });
    });
});
