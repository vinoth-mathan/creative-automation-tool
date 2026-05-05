document.addEventListener('DOMContentLoaded', () => {
  const brandSelect = document.getElementById('brand-select');
  const dealerWrap = document.getElementById('dealer-wrap');
  const dealerList = document.getElementById('dealer-list');
  const selectAllBtn = document.getElementById('select-all');

  const dropZone = document.getElementById('drop-zone');
  const bgInput = document.getElementById('bg-input');
  const preview = document.getElementById('preview');
  const uploadText = document.getElementById('upload-text');

  const useLogo = document.getElementById('use-logo');
  const logoVariants = document.getElementById('logo-variants');

  const useExtraAsset = document.getElementById('use-extra-asset');
  const extraAssetControls = document.getElementById('extra-asset-controls');
  const extraAssetSelect = document.getElementById('extra-asset-select');
  const extraAssetUpload = document.getElementById('extra-asset-upload');

  const generateBtn = document.getElementById('generate-btn');
  const statusEl = document.getElementById('status');
  const downloadLink = document.getElementById('download-link');

  let selectedBackground = null;

  function isValidImage(file) {
    if (!file) return false;
    const validTypes = ['image/jpeg', 'image/png'];
    const lowerName = file.name.toLowerCase();
    const validExt = lowerName.endsWith('.jpg') || lowerName.endsWith('.jpeg') || lowerName.endsWith('.png');
    return validTypes.includes(file.type) && validExt;
  }

  function setStatus(message) {
    statusEl.textContent = message;
  }

  function getSelectedDealerIds() {
    return Array.from(document.querySelectorAll('.dealer-checkbox:checked')).map((cb) => cb.value);
  }

  function getSelectedSizes() {
    return Array.from(document.querySelectorAll('#sizes-wrap input[type="checkbox"]:checked')).map((cb) => cb.value);
  }

  function validateForm() {
    const hasDealers = getSelectedDealerIds().length > 0;
    const hasSizes = getSelectedSizes().length > 0;
    const hasBackground = !!selectedBackground;
    generateBtn.disabled = !(hasDealers && hasSizes && hasBackground);
  }

  function handleBackground(file) {
    if (!isValidImage(file)) {
      setStatus('Please upload a JPG or PNG background image.');
      return;
    }

    selectedBackground = file;
    const reader = new FileReader();
    reader.onload = (event) => {
      preview.src = event.target.result;
      preview.classList.remove('hidden');
      uploadText.classList.add('hidden');
      setStatus('Background ready.');
    };
    reader.readAsDataURL(file);
    validateForm();
  }

  function buildCommonFormData() {
    const fd = new FormData();
    fd.append('background', selectedBackground);
    fd.append('use_logo', useLogo.checked ? 'true' : 'false');
    fd.append('logo_variant', document.querySelector('input[name="logo-variant"]:checked').value);
    fd.append('use_additional_asset', useExtraAsset.checked ? 'true' : 'false');

    if (useExtraAsset.checked) {
      if (extraAssetSelect.value) {
        fd.append('additional_asset_path', extraAssetSelect.value);
      }
      if (extraAssetUpload.files[0]) {
        const uploadFile = extraAssetUpload.files[0];
        if (!isValidImage(uploadFile)) {
          throw new Error('Additional asset upload must be JPG or PNG.');
        }
        fd.append('additional_asset_file', uploadFile);
      }
    }

    return fd;
  }

  async function loadAccounts() {
    const res = await fetch('/api/accounts');
    const accounts = await res.json();
    for (const account of accounts) {
      const opt = document.createElement('option');
      opt.value = account.id;
      opt.textContent = account.name;
      brandSelect.appendChild(opt);
    }
  }

  async function loadAdditionalAssets() {
    const res = await fetch('/api/additional-assets');
    const assets = await res.json();

    assets.forEach((asset) => {
      const opt = document.createElement('option');
      opt.value = asset.value;
      opt.textContent = asset.label;
      extraAssetSelect.appendChild(opt);
    });
  }

  brandSelect.addEventListener('change', async (event) => {
    const accountId = event.target.value;
    dealerList.innerHTML = '';

    if (!accountId) {
      dealerWrap.classList.add('hidden');
      validateForm();
      return;
    }

    const res = await fetch(`/api/dealerships?account_id=${accountId}`);
    const dealers = await res.json();

    dealers.forEach((dealer) => {
      const label = document.createElement('label');
      label.innerHTML = `<input class="dealer-checkbox" type="checkbox" value="${dealer.id}"> ${dealer.name}`;
      dealerList.appendChild(label);
    });

    dealerWrap.classList.remove('hidden');
    validateForm();
  });

  dealerList.addEventListener('change', validateForm);

  selectAllBtn.addEventListener('click', () => {
    const checkboxes = Array.from(document.querySelectorAll('.dealer-checkbox'));
    const allChecked = checkboxes.length > 0 && checkboxes.every((cb) => cb.checked);
    checkboxes.forEach((cb) => {
      cb.checked = !allChecked;
    });
    validateForm();
  });

  dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
  });

  dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    handleBackground(event.dataTransfer.files[0]);
  });

  bgInput.addEventListener('change', (event) => {
    handleBackground(event.target.files[0]);
  });

  useLogo.addEventListener('change', () => {
    logoVariants.classList.toggle('hidden', !useLogo.checked);
  });

  useExtraAsset.addEventListener('change', () => {
    extraAssetControls.classList.toggle('hidden', !useExtraAsset.checked);
  });

  document.querySelectorAll('#sizes-wrap input[type="checkbox"]').forEach((checkbox) => {
    checkbox.addEventListener('change', validateForm);
  });

  generateBtn.addEventListener('click', async () => {
    const dealerIds = getSelectedDealerIds();
    const sizes = getSelectedSizes();
    const mode = document.querySelector('input[name="download-mode"]:checked').value;

    if (!selectedBackground || dealerIds.length === 0 || sizes.length === 0) {
      setStatus('Please select dealers, sizes, and a background image.');
      return;
    }

    generateBtn.disabled = true;
    downloadLink.classList.add('hidden');

    try {
      if (mode === 'zip') {
        const fd = buildCommonFormData();
        dealerIds.forEach((id) => fd.append('dealer_ids', id));
        sizes.forEach((size) => fd.append('sizes', size));

        setStatus('Generating ZIP package...');
        const res = await fetch('/api/generate', { method: 'POST', body: fd });
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.error || 'Generation failed.');
        }

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = 'creatives.zip';
        downloadLink.textContent = 'Download ZIP';
        downloadLink.classList.remove('hidden');
        setStatus('ZIP ready to download.');
      } else {
        const total = dealerIds.length * sizes.length;
        let done = 0;

        for (const dealerId of dealerIds) {
          for (const size of sizes) {
            done += 1;
            setStatus(`Generating file ${done}/${total}...`);
            const fd = buildCommonFormData();
            fd.append('dealer_id', dealerId);
            fd.append('size', size);

            const res = await fetch('/api/generate-single', { method: 'POST', body: fd });
            if (!res.ok) {
              const err = await res.json();
              throw new Error(err.error || 'Individual generation failed.');
            }

            const blob = await res.blob();
            const disposition = res.headers.get('Content-Disposition') || '';
            const filenameMatch = disposition.match(/filename="?([^";]+)"?/i);
            const filename = filenameMatch ? filenameMatch[1] : `creative_${done}.jpg`;

            const fileUrl = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = fileUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(fileUrl);
          }
        }

        setStatus('All individual files generated and downloaded.');
      }
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    } finally {
      generateBtn.disabled = false;
    }
  });

  loadAccounts().catch(() => setStatus('Unable to load accounts.'));
  loadAdditionalAssets().catch(() => setStatus('Unable to load additional assets.'));
  logoVariants.classList.toggle('hidden', !useLogo.checked);
  extraAssetControls.classList.add('hidden');
  validateForm();
});
