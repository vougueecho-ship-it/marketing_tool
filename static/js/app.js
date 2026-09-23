document.addEventListener('DOMContentLoaded', () => {
  // State
  let templates = [];
  let currentTemplate = null;
  let activeFile = 'client sheet.xlsx';
  let leadFiles = [];
  let fileQueue = [];
  let currentPage = 1;
  const pageSize = 25;
  let isPolling = true;

  // DOM Elements - Queue Controls
  const btnSetQueue = document.getElementById('btn-set-queue');
  const btnClearQueue = document.getElementById('btn-clear-queue');
  const queueBanner = document.getElementById('queue-banner');
  const queueSequenceDisplay = document.getElementById('queue-sequence-display');
  const chkSelectAllFiles = document.getElementById('chk-select-all-files');

  // DOM Elements - Tabs
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  // DOM Elements - Header & Quick Select
  const quickFileSelect = document.getElementById('quick-file-select');
  const activeFileLabel = document.getElementById('active-file-label');
  const ctrlTargetFilename = document.getElementById('ctrl-target-filename');
  const tabFilesCount = document.getElementById('tab-files-count');
  const recipientsFileBadge = document.getElementById('recipients-file-badge');

  // DOM Elements - Stats
  const statTotal = document.getElementById('stat-total');
  const statSent = document.getElementById('stat-sent');
  const statPending = document.getElementById('stat-pending');
  const statFailed = document.getElementById('stat-failed');
  const statTotalClicks = document.getElementById('stat-total-clicks');
  const statUniqueClicks = document.getElementById('stat-unique-clicks');
  const statTodaySent = document.getElementById('stat-today-sent');
  const statDailyLimit = document.getElementById('stat-daily-limit');
  const tabClicksCount = document.getElementById('tab-clicks-count');
  const tabRecCount = document.getElementById('tab-rec-count');
  const progressPercentage = document.getElementById('progress-percentage');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const campaignBadge = document.getElementById('campaign-badge');
  const sendingIndicator = document.getElementById('sending-indicator');
  const currentSendingEmail = document.getElementById('current-sending-email');

  // DOM Elements - Control Tab
  const btnStart = document.getElementById('btn-start');
  const btnPause = document.getElementById('btn-pause');
  const btnStop = document.getElementById('btn-stop');
  const btnReset = document.getElementById('btn-reset');
  const ctrlSubject = document.getElementById('ctrl-subject');
  const ctrlSenderName = document.getElementById('ctrl-sender-name');
  const templateSelectorControl = document.getElementById('template-selector-control');
  const ctrlSenderAccountSelect = document.getElementById('ctrl-sender-account-select');
  const btnSwitchFileQuick = document.getElementById('btn-switch-file-quick');

  // DOM Elements - Test Sender
  const testEmailInput = document.getElementById('test-email-input');
  const btnSendTest = document.getElementById('btn-send-test');
  const testResultMsg = document.getElementById('test-result-msg');

  // DOM Elements - Files Tab
  const filesTableBody = document.getElementById('files-table-body');
  const uploadForm = document.getElementById('upload-form');
  const fileInput = document.getElementById('file-input');
  const btnBrowseFile = document.getElementById('btn-browse-file');
  const selectedFileName = document.getElementById('selected-file-name');
  const btnUploadSubmit = document.getElementById('btn-upload-submit');
  const uploadStatusMsg = document.getElementById('upload-status-msg');

  // DOM Elements - Template Designer & Drip Stages
  const stageCards = document.querySelectorAll('.stage-card');
  const templateDropdown = document.getElementById('template-dropdown');
  const editorSubject = document.getElementById('editor-subject');
  const editorSenderName = document.getElementById('editor-sender-name');
  const editorHtml = document.getElementById('editor-html');
  const editorPlain = document.getElementById('editor-plain');
  const previewIframe = document.getElementById('preview-iframe');

  // DOM Elements - Clicks Tab
  const clicksTableBody = document.getElementById('clicks-table-body');
  const clicksSearch = document.getElementById('clicks-search');
  const btnRefreshClicks = document.getElementById('btn-refresh-clicks');

  // DOM Elements - Recipients
  const recipientsTableBody = document.getElementById('recipients-table-body');
  const recSearch = document.getElementById('rec-search');
  const recFilterStatus = document.getElementById('rec-filter-status');
  const btnRetryFailed = document.getElementById('btn-retry-failed');
  const btnExportCsv = document.getElementById('btn-export-csv');
  const btnPrevPage = document.getElementById('btn-prev-page');
  const btnNextPage = document.getElementById('btn-next-page');
  const pageIndicator = document.getElementById('page-indicator');

  // DOM Elements - Settings Form
  const settingsForm = document.getElementById('settings-form');
  const saveCfgMsg = document.getElementById('save-cfg-msg');

  // DOM Elements - Logs
  const liveConsole = document.getElementById('live-console');
  const btnClearLogsView = document.getElementById('btn-clear-logs-view');

  // DOM Elements - Modern Layout & Mobile Sidebar
  const appSidebar = document.getElementById('app-sidebar');
  const sidebarBackdrop = document.getElementById('sidebar-backdrop');
  const btnMobileToggle = document.getElementById('btn-mobile-sidebar-toggle');
  const activeViewTitle = document.getElementById('active-view-title');
  const btnSidebarLimitModal = document.getElementById('btn-sidebar-limit-modal');

  const tabTitles = {
    'tab-control': '<i class="fa-solid fa-rocket text-primary"></i> <span>1-Click Campaign Dispatcher</span>',
    'tab-cleaner': '<i class="fa-solid fa-broom text-primary"></i> <span>Deep Email Verifier &amp; Cleaner</span>',
    'tab-files': '<i class="fa-solid fa-folder-tree text-primary"></i> <span>Lead Files &amp; Queue Manager</span>',
    'tab-templates': '<i class="fa-solid fa-layer-group text-primary"></i> <span>Drip Sequences &amp; AI Generator</span>',
    'tab-recipients': '<i class="fa-solid fa-list-check text-primary"></i> <span>Recipients Queue &amp; Status</span>',
    'tab-clicks': '<i class="fa-solid fa-fire text-warning"></i> <span>Engaged Leads &amp; Clicks Tracker</span>',
    'tab-senders': '<i class="fa-solid fa-at text-primary"></i> <span>Sender Emails &amp; Account Rotation</span>',
    'tab-warmup': '<i class="fa-solid fa-fire-flame-curved" style="color: #ea580c;"></i> <span>Gmail Warmup &amp; Deliverability Pool</span>',
    'tab-settings': '<i class="fa-solid fa-sliders text-primary"></i> <span>SMTP &amp; Anti-Spam Settings</span>',
    'tab-logs': '<i class="fa-solid fa-terminal text-primary"></i> <span>Live Dispatch Console Stream</span>'
  };

  if (btnMobileToggle && appSidebar && sidebarBackdrop) {
    btnMobileToggle.addEventListener('click', () => {
      appSidebar.classList.toggle('open');
      sidebarBackdrop.classList.toggle('active');
    });
    sidebarBackdrop.addEventListener('click', () => {
      appSidebar.classList.remove('open');
      sidebarBackdrop.classList.remove('active');
    });
  }

  if (btnSidebarLimitModal) {
    btnSidebarLimitModal.addEventListener('click', () => {
      const btnOpenLimit = document.getElementById('btn-open-limit-modal');
      if (btnOpenLimit) btnOpenLimit.click();
    });
  }

  // ==================== 1. TAB NAVIGATION ====================
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add('active');

      if (activeViewTitle && tabTitles[targetId]) {
        activeViewTitle.innerHTML = tabTitles[targetId];
      }

      if (appSidebar && sidebarBackdrop) {
        appSidebar.classList.remove('open');
        sidebarBackdrop.classList.remove('active');
      }

      if (targetId === 'tab-recipients') {
        loadRecipients();
      } else if (targetId === 'tab-clicks') {
        loadClicks();
      } else if (targetId === 'tab-files') {
        loadFiles();
      } else if (targetId === 'tab-senders') {
        loadSenderAccounts();
      } else if (targetId === 'tab-warmup') {
        loadWarmupData();
      }
    });
  });

  if (btnSwitchFileQuick) {
    btnSwitchFileQuick.addEventListener('click', () => {
      const filesTabBtn = document.querySelector('[data-tab="tab-files"]');
      if (filesTabBtn) filesTabBtn.click();
    });
  }

  // ==================== 2. LEAD FILES & QUEUE MANAGEMENT ====================
  async function loadFiles() {
    try {
      const res = await fetch('/api/files');
      const data = await res.json();
      activeFile = data.active_file;
      leadFiles = data.files || [];

      // Fetch active queue status
      fetchQueue();

      tabFilesCount.textContent = leadFiles.length;
      activeFileLabel.textContent = activeFile || 'None Selected';
      ctrlTargetFilename.textContent = activeFile || 'None Selected';
      recipientsFileBadge.textContent = activeFile || 'None';
      if (btnExportCsv) {
        btnExportCsv.href = `/api/export-report?file_name=${encodeURIComponent(activeFile)}`;
      }

      // Quick Selector
      quickFileSelect.innerHTML = '';
      leadFiles.forEach(f => {
        const opt = new Option(`${f.name} (${f.total} leads)`, f.name, false, f.name === activeFile);
        quickFileSelect.add(opt);
      });

      // Files Table
      if (filesTableBody) {
        if (leadFiles.length === 0) {
          filesTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No files uploaded yet.</td></tr>';
          return;
        }

        filesTableBody.innerHTML = leadFiles.map(f => {
          const isCurrent = f.name === activeFile;
          const inQueueIndex = fileQueue.indexOf(f.name);
          const queueBadge = inQueueIndex >= 0 ? `<span class="status-badge pending" style="margin-left: 6px;">Queue #${inQueueIndex + 1}</span>` : '';

          return `
            <tr style="${isCurrent ? 'background: rgba(245, 158, 11, 0.08);' : ''}">
              <td class="text-center">
                <input type="checkbox" class="chk-file-select" value="${escapeHtml(f.name)}" ${inQueueIndex >= 0 ? 'checked' : ''}>
              </td>
              <td>
                <i class="fa-solid fa-file-excel text-gold" style="margin-right: 6px;"></i>
                <strong>${escapeHtml(f.name)}</strong>
                ${isCurrent ? '<span class="status-badge sent" style="margin-left: 8px;">Active</span>' : ''}
                ${queueBadge}
              </td>
              <td><strong>${Number(f.total).toLocaleString()}</strong></td>
              <td><span class="text-gold">${Number(f.sent).toLocaleString()}</span></td>
              <td>${Number(f.pending).toLocaleString()}</td>
              <td>
                <div style="display: flex; gap: 6px; align-items: center;">
                  ${isCurrent ? 
                    '<button class="btn btn-sm btn-primary" disabled><i class="fa-solid fa-check"></i> Selected</button>' : 
                    `<button class="btn btn-sm btn-outline btn-select-file" data-file="${escapeHtml(f.name)}">Select List</button>`
                  }
                  <button class="btn btn-sm btn-danger btn-delete-file" data-file="${escapeHtml(f.name)}" title="Delete list & remove leads">
                    <i class="fa-solid fa-trash-can"></i>
                  </button>
                </div>
              </td>
            </tr>
          `;
        }).join('');

        // Attach listeners for select & delete buttons
        document.querySelectorAll('.btn-select-file').forEach(btn => {
          btn.addEventListener('click', () => {
            selectFile(btn.getAttribute('data-file'));
          });
        });

        document.querySelectorAll('.btn-delete-file').forEach(btn => {
          btn.addEventListener('click', () => {
            deleteFile(btn.getAttribute('data-file'));
          });
        });
      }
    } catch (err) {
      console.error('Failed to load files:', err);
    }
  }

  async function fetchQueue() {
    try {
      const res = await fetch('/api/queue');
      const data = await res.json();
      fileQueue = data.file_queue || [];
      renderQueueUI();
    } catch (err) {
      console.error('Failed to fetch queue:', err);
    }
  }

  function renderQueueUI() {
    if (fileQueue && fileQueue.length > 0) {
      if (queueBanner) queueBanner.style.display = 'flex';
      if (btnClearQueue) btnClearQueue.style.display = 'inline-flex';
      if (queueSequenceDisplay) {
        queueSequenceDisplay.innerHTML = fileQueue.map((f, i) => `<span class="badge ${f === activeFile ? 'badge-running' : 'badge-idle'}" style="margin-right: 4px;">#${i+1} ${escapeHtml(f)}</span>`).join(' ➔ ');
      }
    } else {
      if (queueBanner) queueBanner.style.display = 'none';
      if (btnClearQueue) btnClearQueue.style.display = 'none';
    }
  }

  async function selectFile(fileName) {
    try {
      const res = await fetch('/api/files/select', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_name: fileName })
      });
      const data = await res.json();
      if (data.success) {
        activeFile = fileName;
        activeFileLabel.textContent = activeFile;
        ctrlTargetFilename.textContent = activeFile;
        recipientsFileBadge.textContent = activeFile;
        loadFiles();
        fetchStats();
        loadRecipients();
      } else {
        alert(data.error || 'Failed to select file.');
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  }

  async function deleteFile(fileName) {
    if (!confirm(`Are you sure you want to DELETE lead list '${fileName}'?\n\nThis will permanently remove the file and all its associated recipient data.`)) {
      return;
    }

    try {
      const res = await fetch('/api/files/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_name: fileName })
      });
      const data = await res.json();
      if (data.success) {
        alert(data.message);
        loadFiles();
        fetchStats();
        loadRecipients();
      } else {
        alert(data.error || 'Failed to delete file.');
      }
    } catch (err) {
      alert('Error deleting file: ' + err.message);
    }
  }

  // Queue toolbar event listeners
  if (chkSelectAllFiles) {
    chkSelectAllFiles.addEventListener('change', (e) => {
      document.querySelectorAll('.chk-file-select').forEach(chk => {
        chk.checked = e.target.checked;
      });
    });
  }

  if (btnSetQueue) {
    btnSetQueue.addEventListener('click', async () => {
      const checkedInputs = Array.from(document.querySelectorAll('.chk-file-select:checked'));
      const selectedFiles = checkedInputs.map(input => input.value);

      if (selectedFiles.length === 0) {
        alert('Please check at least one file to build a campaign queue.');
        return;
      }

      try {
        const res = await fetch('/api/queue', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_queue: selectedFiles })
        });
        const data = await res.json();
        if (data.success) {
          fileQueue = data.file_queue || [];
          renderQueueUI();
          loadFiles();
          alert(`Multi-File Queue set! When your campaign runs, it will auto-process these ${fileQueue.length} files sequentially.`);
        } else {
          alert(data.error || 'Failed to update queue.');
        }
      } catch (err) {
        alert('Error setting queue: ' + err.message);
      }
    });
  }

  if (btnClearQueue) {
    btnClearQueue.addEventListener('click', async () => {
      try {
        const res = await fetch('/api/queue', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_queue: [] })
        });
        const data = await res.json();
        if (data.success) {
          fileQueue = [];
          renderQueueUI();
          loadFiles();
        }
      } catch (err) {
        console.error(err);
      }
    });
  }

  quickFileSelect.addEventListener('change', (e) => {
    selectFile(e.target.value);
  });

  // File Upload Logic
  btnBrowseFile.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      const f = fileInput.files[0];
      selectedFileName.textContent = `Selected: ${f.name} (${roundKb(f.size)})`;
      btnUploadSubmit.style.display = 'inline-flex';
    }
  });

  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!fileInput.files.length) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    btnUploadSubmit.disabled = true;
    btnUploadSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading & Parsing Leads...';
    uploadStatusMsg.style.display = 'none';

    try {
      const res = await fetch('/api/files/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();

      if (data.success) {
        uploadStatusMsg.style.display = 'block';
        uploadStatusMsg.className = 'alert-box alert-success';
        uploadStatusMsg.textContent = data.message;
        fileInput.value = '';
        selectedFileName.textContent = '';
        btnUploadSubmit.style.display = 'none';

        loadFiles();
        fetchStats();
        loadRecipients();
      } else {
        uploadStatusMsg.style.display = 'block';
        uploadStatusMsg.className = 'alert-box alert-danger';
        uploadStatusMsg.textContent = data.error || 'Upload failed.';
      }
    } catch (err) {
      uploadStatusMsg.style.display = 'block';
      uploadStatusMsg.className = 'alert-box alert-danger';
      uploadStatusMsg.textContent = 'Upload network error: ' + err.message;
    } finally {
      btnUploadSubmit.disabled = false;
      btnUploadSubmit.innerHTML = '<i class="fa-solid fa-arrow-up-from-bracket"></i> Upload & Load Leads';
    }
  });

  function roundKb(bytes) {
    return `${Math.round(bytes / 1024)} KB`;
  }

  // ==================== 3. 3-STAGE DRIP TEMPLATES ====================
  async function loadTemplates() {
    try {
      const res = await fetch('/api/templates');
      templates = await res.json();

      templateSelectorControl.innerHTML = '';
      templateDropdown.innerHTML = '';

      templates.forEach((tpl) => {
        const opt1 = new Option(tpl.name, tpl.id);
        const opt2 = new Option(tpl.name, tpl.id);
        templateSelectorControl.add(opt1);
        templateDropdown.add(opt2);
      });

      if (templates.length > 0) {
        selectTemplate(templates[0].id);
      }
    } catch (err) {
      console.error('Failed to load templates:', err);
    }
  }

  function selectTemplate(templateId) {
    const tpl = templates.find(t => t.id === templateId) || templates[0];
    if (!tpl) return;
    currentTemplate = tpl;

    templateSelectorControl.value = tpl.id;
    templateDropdown.value = tpl.id;

    // Highlight Drip Stage Card
    stageCards.forEach(sc => {
      if (sc.getAttribute('data-stage') === tpl.id) {
        sc.classList.add('active');
      } else {
        sc.classList.remove('active');
      }
    });

    ctrlSubject.value = tpl.subject;
    editorSubject.value = tpl.subject;
    editorHtml.value = tpl.html;
    editorPlain.value = tpl.plain_text;

    updatePreview(tpl.html);
  }

  stageCards.forEach(card => {
    card.addEventListener('click', () => {
      const stageId = card.getAttribute('data-stage');
      selectTemplate(stageId);
    });
  });

  const btnDeleteTemplate = document.getElementById('btn-delete-template');
  if (btnDeleteTemplate) {
    btnDeleteTemplate.addEventListener('click', async () => {
      if (!currentTemplate) return;
      if (templates.length <= 1) {
        alert('Cannot delete the last remaining template!');
        return;
      }
      const confirmDel = confirm(`Are you sure you want to delete template "${currentTemplate.name}"?`);
      if (!confirmDel) return;

      try {
        const res = await fetch('/api/templates/delete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ template_id: currentTemplate.id })
        });
        const data = await res.json();
        if (data.success) {
          alert(data.message || 'Template deleted successfully!');
          await loadTemplates();
        } else {
          alert(data.error || 'Failed to delete template.');
        }
      } catch (err) {
        alert('Network error while deleting template: ' + err.message);
      }
    });
  }

  templateSelectorControl.addEventListener('change', (e) => {
    selectTemplate(e.target.value);
  });

  templateDropdown.addEventListener('change', (e) => {
    selectTemplate(e.target.value);
  });

  ctrlSubject.addEventListener('input', (e) => {
    editorSubject.value = e.target.value;
  });
  editorSubject.addEventListener('input', (e) => {
    ctrlSubject.value = e.target.value;
  });

  ctrlSenderName.addEventListener('input', (e) => {
    editorSenderName.value = e.target.value;
  });
  editorSenderName.addEventListener('input', (e) => {
    ctrlSenderName.value = e.target.value;
  });

  editorHtml.addEventListener('input', (e) => {
    updatePreview(e.target.value);
  });

  function updatePreview(html) {
    const doc = previewIframe.contentDocument || previewIframe.contentWindow.document;
    doc.open();
    doc.write(html);
    doc.close();
  }

  // ==================== SMART AI EMAIL TEMPLATE GENERATOR ====================
  const aiPromptInput = document.getElementById('ai-prompt-input');
  const aiToneSelect = document.getElementById('ai-tone-select');
  const btnGenerateAiTemplate = document.getElementById('btn-generate-ai-template');
  const aiGeneratedActionBar = document.getElementById('ai-generated-action-bar');
  const aiGeneratedSubjectPreview = document.getElementById('ai-generated-subject-preview');
  const btnApplyAiToCampaign = document.getElementById('btn-apply-ai-to-campaign');
  const btnSaveAiTemplate = document.getElementById('btn-save-ai-template');
  const presetChips = document.querySelectorAll('.preset-chip');

  let currentGeneratedTemplate = null;

  presetChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const promptText = chip.getAttribute('data-prompt');
      if (aiPromptInput && promptText) {
        aiPromptInput.value = promptText;
      }
    });
  });

  if (btnGenerateAiTemplate) {
    btnGenerateAiTemplate.addEventListener('click', async () => {
      const promptVal = aiPromptInput ? aiPromptInput.value.trim() : '';
      if (!promptVal) {
        alert('Please type what you want your email to say before generating!');
        return;
      }

      btnGenerateAiTemplate.disabled = true;
      btnGenerateAiTemplate.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating Smart Template...';

      try {
        const toneVal = aiToneSelect ? aiToneSelect.value : 'vip';
        const res = await fetch('/api/templates/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: promptVal, tone: toneVal })
        });
        const data = await res.json();
        if (data.success && data.template) {
          currentGeneratedTemplate = data.template;
          
          // Populate editor fields
          editorSubject.value = data.template.subject;
          ctrlSubject.value = data.template.subject;
          editorHtml.value = data.template.html;
          editorPlain.value = data.template.plain_text;

          updatePreview(data.template.html);

          if (aiGeneratedSubjectPreview) aiGeneratedSubjectPreview.textContent = data.template.subject;
          if (aiGeneratedActionBar) aiGeneratedActionBar.style.display = 'block';

        } else {
          alert(data.error || 'Failed to generate template.');
        }
      } catch (err) {
        alert('Generation error: ' + err.message);
      } finally {
        btnGenerateAiTemplate.disabled = false;
        btnGenerateAiTemplate.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Template';
      }
    });
  }

  if (btnApplyAiToCampaign) {
    btnApplyAiToCampaign.addEventListener('click', () => {
      if (!currentGeneratedTemplate) return;
      ctrlSubject.value = currentGeneratedTemplate.subject;
      editorSubject.value = currentGeneratedTemplate.subject;
      editorHtml.value = currentGeneratedTemplate.html;
      editorPlain.value = currentGeneratedTemplate.plain_text;
      
      const controlTabBtn = document.querySelector('[data-tab="tab-control"]');
      if (controlTabBtn) controlTabBtn.click();

      alert(`✅ Generated template "${currentGeneratedTemplate.subject}" loaded into Campaign Control! Click "Start Campaign" when ready to send.`);
    });
  }

  if (btnSaveAiTemplate) {
    btnSaveAiTemplate.addEventListener('click', async () => {
      if (!currentGeneratedTemplate) return;
      btnSaveAiTemplate.disabled = true;
      try {
        const res = await fetch('/api/templates/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ template: currentGeneratedTemplate })
        });
        const data = await res.json();
        if (data.success) {
          alert(data.message || 'Template saved successfully!');
          await loadTemplates();
          selectTemplate(currentGeneratedTemplate.id);
        } else {
          alert(data.error || 'Failed to save template.');
        }
      } catch (err) {
        alert('Error saving template: ' + err.message);
      } finally {
        btnSaveAiTemplate.disabled = false;
      }
    });
  }


  // ==================== 4. STATS & PROGRESS POLLING ====================
  async function fetchStats() {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();

      if (data.active_file && data.active_file !== activeFile) {
        activeFile = data.active_file;
        activeFileLabel.textContent = activeFile;
        ctrlTargetFilename.textContent = activeFile;
        recipientsFileBadge.textContent = activeFile;
      }

      if (statTotal) statTotal.textContent = Number(data.total || 0).toLocaleString();
      if (statSent) statSent.textContent = Number(data.sent || 0).toLocaleString();
      if (statPending) statPending.textContent = Number(data.pending || 0).toLocaleString();
      if (statFailed) statFailed.textContent = Number(data.failed || 0).toLocaleString();
      if (statTotalClicks) statTotalClicks.textContent = Number(data.total_clicks || 0).toLocaleString();
      if (statUniqueClicks) statUniqueClicks.textContent = Number(data.unique_clicks || 0).toLocaleString();
      if (statTodaySent) statTodaySent.textContent = Number(data.today_sent || 0).toLocaleString();
      if (statDailyLimit) statDailyLimit.textContent = Number(data.daily_limit || 850).toLocaleString();
      if (tabClicksCount) tabClicksCount.textContent = Number(data.unique_clicks || 0).toLocaleString();
      if (tabRecCount) tabRecCount.textContent = Number(data.total || 0).toLocaleString();

      const todaySentNum = Number(data.today_sent || 0);
      const dailyLimitNum = Number(data.daily_limit || 850);
      const quotaPct = dailyLimitNum > 0 ? Math.min(100, Math.round((todaySentNum / dailyLimitNum) * 100)) : 0;
      const sidebarQuotaBar = document.getElementById('sidebar-quota-bar');
      const sidebarQuotaSent = document.getElementById('sidebar-quota-sent');
      const sidebarQuotaLimit = document.getElementById('sidebar-quota-limit');
      if (sidebarQuotaBar) sidebarQuotaBar.style.width = `${quotaPct}%`;
      if (sidebarQuotaSent) sidebarQuotaSent.textContent = todaySentNum.toLocaleString();
      if (sidebarQuotaLimit) sidebarQuotaLimit.textContent = dailyLimitNum.toLocaleString();

      const pct = data.total > 0 ? Math.round(((data.sent + (data.failed || 0)) / data.total) * 100) : 0;
      if (progressPercentage) progressPercentage.textContent = `${pct}% (${data.sent}/${data.total} Sent)`;
      if (progressBarFill) {
        progressBarFill.style.width = `${pct}%`;
      }

      if (data.is_running) {
        if (data.is_paused) {
          if (campaignBadge) {
            campaignBadge.className = 'badge badge-paused';
            campaignBadge.innerHTML = '<i class="fa-solid fa-pause"></i> CAMPAIGN PAUSED';
          }
          if (btnStart) {
            btnStart.innerHTML = `<i class="fa-solid fa-play"></i> Resume Campaign (${data.pending} Remaining)`;
            btnStart.disabled = false;
          }
          if (btnPause) btnPause.disabled = true;
          if (btnStop) btnStop.disabled = false;
          if (sendingIndicator) sendingIndicator.style.display = 'none';
        } else {
          if (campaignBadge) {
            campaignBadge.className = 'badge badge-running';
            campaignBadge.innerHTML = '<i class="fa-solid fa-bolt"></i> CAMPAIGN RUNNING';
          }
          if (btnStart) {
            btnStart.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Dispatching (${data.pending} Left)...`;
            btnStart.disabled = true;
          }
          if (btnPause) btnPause.disabled = false;
          if (btnStop) btnStop.disabled = false;

          if (data.current_email && sendingIndicator) {
            sendingIndicator.style.display = 'inline-flex';
            if (currentSendingEmail) currentSendingEmail.textContent = data.current_email;
          }
        }
      } else {
        if (campaignBadge) {
          campaignBadge.className = 'badge badge-idle';
          if (data.pending === 0 && data.total > 0) {
            campaignBadge.innerHTML = '<i class="fa-solid fa-circle-check text-success"></i> COMPLETED (100%)';
          } else {
            campaignBadge.innerHTML = '<i class="fa-solid fa-circle"></i> IDLE / READY';
          }
        }
        
        if (btnStart) {
          if (data.pending === 0 && data.total > 0) {
            btnStart.innerHTML = '<i class="fa-solid fa-circle-check"></i> All Leads Completed (100%)';
            btnStart.disabled = true;
            btnStart.classList.add('btn-disabled');
          } else if (data.sent > 0) {
            btnStart.innerHTML = `<i class="fa-solid fa-play"></i> Send Remaining (${Number(data.pending).toLocaleString()} Pending Leads)`;
            btnStart.disabled = false;
            btnStart.classList.remove('btn-disabled');
          } else {
            btnStart.innerHTML = `<i class="fa-solid fa-play"></i> Start Campaign (${Number(data.total).toLocaleString()} Leads)`;
            btnStart.disabled = false;
            btnStart.classList.remove('btn-disabled');
          }
        }

        if (btnPause) btnPause.disabled = true;
        if (btnStop) btnStop.disabled = true;
        if (sendingIndicator) sendingIndicator.style.display = 'none';
      }
    } catch (err) {
      console.error('Stats poll error:', err);
    }
  }

  // ==================== 5. LIVE LOGS POLLING ====================
  async function fetchLogs() {
    try {
      const res = await fetch('/api/logs?limit=50');
      const logs = await res.json();
      if (!logs || logs.length === 0) return;

      liveConsole.innerHTML = logs.map(l => `
        <div class="log-entry">
          <span class="log-time">[${l.timestamp}]</span>
          <span class="log-${l.level}">[${l.level}]</span>
          <span>${escapeHtml(l.message)}</span>
        </div>
      `).join('');
    } catch (err) {
      console.error('Logs fetch error:', err);
    }
  }

  btnClearLogsView.addEventListener('click', () => {
    liveConsole.innerHTML = '<div class="log-entry text-muted">Console cleared.</div>';
  });

  // ==================== 6. CLICKS TRACKER ====================
  async function loadClicks() {
    const search = clicksSearch.value.trim();
    clicksTableBody.innerHTML = '<tr><td colspan="5" class="text-center">Loading clicked leads...</td></tr>';
    
    try {
      const res = await fetch(`/api/clicks?search=${encodeURIComponent(search)}&limit=100`);
      const list = await res.json();

      if (list.length === 0) {
        clicksTableBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No clicks recorded yet. When users click the link in their email, they will show up here live!</td></tr>';
        return;
      }

      clicksTableBody.innerHTML = list.map(c => `
        <tr>
          <td>#${c.id}</td>
          <td><strong>${escapeHtml(c.email)}</strong></td>
          <td>
            <span class="click-badge ${c.click_count >= 2 ? 'hot' : ''}">
              <i class="fa-solid fa-arrow-pointer"></i> ${c.click_count} ${c.click_count > 1 ? 'Clicks 🔥' : 'Click'}
            </span>
          </td>
          <td>${c.first_clicked_at}</td>
          <td>${c.last_clicked_at}</td>
        </tr>
      `).join('');
    } catch (err) {
      clicksTableBody.innerHTML = `<tr><td colspan="5" class="text-danger">Failed to load clicks: ${err.message}</td></tr>`;
    }
  }

  clicksSearch.addEventListener('input', () => loadClicks());
  btnRefreshClicks.addEventListener('click', () => loadClicks());

  const btnTestClickLink = document.getElementById('btn-test-click-link');
  if (btnTestClickLink) {
    btnTestClickLink.addEventListener('click', () => {
      const testEmail = `test_player_${Math.floor(100 + Math.random() * 900)}@winningheaven.com`;
      const testUrl = `/r?e=${encodeURIComponent(testEmail)}&dest=${encodeURIComponent('https://winningheaven.com')}`;
      window.open(testUrl, '_blank');
      setTimeout(() => {
        loadClicks();
        loadStats();
      }, 1000);
    });
  }

  // ==================== 7. TEST EMAIL SENDER ====================
  btnSendTest.addEventListener('click', async () => {
    const toEmail = testEmailInput.value.trim();
    if (!toEmail) {
      showTestResult('Please enter an email to send the test message to.', false);
      return;
    }

    btnSendTest.disabled = true;
    btnSendTest.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
    testResultMsg.style.display = 'none';

    try {
      const selectedAccId = (ctrlSenderAccountSelect && ctrlSenderAccountSelect.value !== 'auto') ? ctrlSenderAccountSelect.value : '';
      const res = await fetch('/api/test-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to_email: toEmail,
          subject: ctrlSubject.value.trim(),
          sender_name: ctrlSenderName.value.trim(),
          html_body: editorHtml.value,
          plain_body: editorPlain.value,
          account_id: selectedAccId
        })
      });

      const data = await res.json();
      if (data.success) {
        showTestResult(`✓ Success! Test email delivered to ${toEmail}. Check your inbox!`, true);
      } else {
        showTestResult(`✗ Error: ${data.error}`, false);
      }
    } catch (err) {
      showTestResult(`Network error: ${err.message}`, false);
    } finally {
      btnSendTest.disabled = false;
      btnSendTest.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Send Test';
    }
  });

  function showTestResult(msg, isSuccess) {
    testResultMsg.style.display = 'block';
    testResultMsg.className = `alert-box ${isSuccess ? 'alert-success' : 'alert-danger'}`;
    testResultMsg.textContent = msg;
  }

  // ==================== 8. CAMPAIGN CONTROLS ====================
  btnStart.addEventListener('click', async () => {
    const isResume = parseInt(statSent.textContent.replace(/,/g, ''), 10) > 0;
    const qInfo = fileQueue && fileQueue.length > 0 ? ` (Queue active with ${fileQueue.length} remaining list[s])` : '';
    const confirmMsg = isResume 
      ? `Resume sending to the remaining ${statPending.textContent} pending leads in '${activeFile}'${qInfo}?` 
      : `Start sending emails to list '${activeFile}'${qInfo}?`;

    if (!confirm(confirmMsg)) return;

    btnStart.disabled = true;
    try {
      const selectedSenderAcc = ctrlSenderAccountSelect ? ctrlSenderAccountSelect.value : 'auto';
      const res = await fetch('/api/campaign/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject: ctrlSubject.value.trim(),
          sender_name: ctrlSenderName.value.trim(),
          html_body: editorHtml.value,
          plain_body: editorPlain.value,
          file_name: activeFile,
          file_queue: fileQueue,
          sender_account_id: selectedSenderAcc
        })
      });
      const data = await res.json();
      if (!data.success) {
        alert(data.error || 'Failed to start campaign.');
      }
      fetchStats();
      fetchLogs();
    } catch (err) {
      alert('Error starting campaign: ' + err.message);
    }
  });

  btnPause.addEventListener('click', async () => {
    try {
      await fetch('/api/campaign/pause', { method: 'POST' });
      fetchStats();
      fetchLogs();
    } catch (err) {
      console.error(err);
    }
  });

  btnStop.addEventListener('click', async () => {
    if (!confirm('Stop the campaign? You can restart or resume later.')) return;
    try {
      await fetch('/api/campaign/stop', { method: 'POST' });
      fetchStats();
      fetchLogs();
    } catch (err) {
      console.error(err);
    }
  });

  btnReset.addEventListener('click', async () => {
    if (!confirm(`Reset all leads in '${activeFile}' back to "Pending" status?`)) return;
    try {
      await fetch('/api/campaign/reset', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_name: activeFile })
      });
      fetchStats();
      fetchLogs();
      loadRecipients();
    } catch (err) {
      console.error(err);
    }
  });

  // ==================== 9. RECIPIENTS LIST ====================
  async function loadRecipients() {
    const search = recSearch.value.trim();
    const status = recFilterStatus.value;
    const offset = (currentPage - 1) * pageSize;

    recipientsTableBody.innerHTML = '<tr><td colspan="5" class="text-center">Loading...</td></tr>';

    try {
      const res = await fetch(`/api/recipients?file_name=${encodeURIComponent(activeFile)}&search=${encodeURIComponent(search)}&status=${status}&limit=${pageSize}&offset=${offset}`);
      const list = await res.json();

      if (list.length === 0) {
        recipientsTableBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No recipients found in this list.</td></tr>';
        return;
      }

      recipientsTableBody.innerHTML = list.map(r => `
        <tr>
          <td>#${r.id}</td>
          <td><strong>${escapeHtml(r.email)}</strong></td>
          <td><span class="status-badge ${r.status}">${r.status}</span></td>
          <td>${r.sent_at || '<span class="text-muted">—</span>'}</td>
          <td>${r.error_msg ? `<span class="text-danger">${escapeHtml(r.error_msg)}</span>` : '<span class="text-muted">—</span>'}</td>
        </tr>
      `).join('');

      pageIndicator.textContent = `Page ${currentPage}`;
      btnPrevPage.disabled = currentPage <= 1;
      btnNextPage.disabled = list.length < pageSize;
    } catch (err) {
      recipientsTableBody.innerHTML = `<tr><td colspan="5" class="text-danger">Failed to load leads: ${err.message}</td></tr>`;
    }
  }

  recSearch.addEventListener('input', () => {
    currentPage = 1;
    loadRecipients();
  });

  recFilterStatus.addEventListener('change', () => {
    currentPage = 1;
    loadRecipients();
  });

  btnPrevPage.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      loadRecipients();
    }
  });

  btnNextPage.addEventListener('click', () => {
    currentPage++;
    loadRecipients();
  });

  if (btnRetryFailed) {
    btnRetryFailed.addEventListener('click', async () => {
      if (!confirm(`Re-queue failed emails in '${activeFile}' back to Pending?`)) return;
      btnRetryFailed.disabled = true;
      try {
        const res = await fetch('/api/campaign/retry-failed', { 
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_name: activeFile })
        });
        const data = await res.json();
        alert(data.message || 'Failed emails re-queued.');
        fetchStats();
        loadRecipients();
      } catch (err) {
        alert('Error: ' + err.message);
      } finally {
        btnRetryFailed.disabled = false;
      }
    });
  }

  // ==================== 10. SETTINGS ====================
  async function loadSettings() {
    try {
      const res = await fetch('/api/config');
      const cfg = await res.json();
      document.getElementById('cfg-smtp-host').value = cfg.smtp_host || 'smtp.hostinger.com';
      document.getElementById('cfg-smtp-port').value = cfg.smtp_port || 465;
      document.getElementById('cfg-sender-email').value = cfg.sender_email || 'verified@winningheaven.com';
      document.getElementById('cfg-sender-pass').value = cfg.sender_password || '';
      document.getElementById('cfg-sender-name').value = cfg.sender_name || 'Winning Heaven VIP';
      document.getElementById('cfg-reply-to').value = cfg.reply_to || 'verified@winningheaven.com';
      if (document.getElementById('cfg-tracking-base-url')) {
        document.getElementById('cfg-tracking-base-url').value = cfg.tracking_base_url || 'http://127.0.0.1:5050';
      }
      document.getElementById('cfg-min-delay').value = cfg.min_delay_seconds || 3;
      document.getElementById('cfg-max-delay').value = cfg.max_delay_seconds || 6;
      document.getElementById('cfg-batch-size').value = cfg.batch_size || 50;
      document.getElementById('cfg-batch-pause').value = cfg.batch_pause_seconds || 60;
      if (document.getElementById('cfg-daily-limit')) {
        document.getElementById('cfg-daily-limit').value = cfg.daily_limit || 850;
      }
    } catch (err) {
      console.error('Failed to load settings:', err);
    }
  }

  settingsForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      smtp_host: document.getElementById('cfg-smtp-host').value.trim(),
      smtp_port: parseInt(document.getElementById('cfg-smtp-port').value, 10),
      sender_email: document.getElementById('cfg-sender-email').value.trim(),
      sender_password: document.getElementById('cfg-sender-pass').value,
      sender_name: document.getElementById('cfg-sender-name').value.trim(),
      reply_to: document.getElementById('cfg-reply-to').value.trim(),
      tracking_base_url: document.getElementById('cfg-tracking-base-url') ? document.getElementById('cfg-tracking-base-url').value.trim() : 'http://127.0.0.1:5050',
      min_delay_seconds: parseFloat(document.getElementById('cfg-min-delay').value),
      max_delay_seconds: parseFloat(document.getElementById('cfg-max-delay').value),
      batch_size: parseInt(document.getElementById('cfg-batch-size').value, 10),
      batch_pause_seconds: parseFloat(document.getElementById('cfg-batch-pause').value),
      daily_limit: parseInt(document.getElementById('cfg-daily-limit').value, 10) || 850
    };

    try {
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        saveCfgMsg.style.display = 'inline';
        setTimeout(() => { saveCfgMsg.style.display = 'none'; }, 3000);
      }
    } catch (err) {
      alert('Error saving settings: ' + err.message);
    }
  });

  // ==================== 11. SENDER ACCOUNTS & MULTI-ACCOUNT ROTATION ====================
  let senderAccounts = [];
  const tabSendersCount = document.getElementById('tab-senders-count');
  const sendersCardsContainer = document.getElementById('senders-cards-container');
  const btnOpenAddSenderModal = document.getElementById('btn-open-add-sender-modal');
  const btnCloseAddSenderModal = document.getElementById('btn-close-add-sender-modal');
  const btnCancelAddSender = document.getElementById('btn-cancel-add-sender');
  const modalAddSender = document.getElementById('modal-add-sender');
  const formAddSender = document.getElementById('form-add-sender');
  const presetBtnHostinger = document.getElementById('preset-btn-hostinger');
  const presetBtnGmail = document.getElementById('preset-btn-gmail');
  const presetBtnCustom = document.getElementById('preset-btn-custom');
  const gmailNoticeBox = document.getElementById('gmail-notice-box');
  const addSenderModalMsg = document.getElementById('add-sender-modal-msg');

  async function loadSenderAccounts() {
    try {
      const res = await fetch('/api/senders');
      const data = await res.json();
      if (data.success) {
        senderAccounts = data.accounts || [];
        renderSenderAccounts();
      }
    } catch (err) {
      console.error('Error loading sender accounts:', err);
    }
  }

  function updateCtrlSenderAccountSelect() {
    if (!ctrlSenderAccountSelect) return;
    const currentVal = ctrlSenderAccountSelect.value || 'auto';
    ctrlSenderAccountSelect.innerHTML = '';

    const autoOpt = document.createElement('option');
    autoOpt.value = 'auto';
    autoOpt.textContent = '🤖 Auto-Rotate All Enabled Senders';
    ctrlSenderAccountSelect.appendChild(autoOpt);

    senderAccounts.forEach(acc => {
      const opt = document.createElement('option');
      opt.value = acc.id;
      const statusStr = acc.enabled ? (acc.sent_today >= acc.daily_limit ? '(Cap Full)' : '(Ready)') : '(Disabled)';
      opt.textContent = `📧 ${acc.sender_email} [${acc.provider.toUpperCase()}] - ${acc.sent_today}/${acc.daily_limit} sent ${statusStr}`;
      ctrlSenderAccountSelect.appendChild(opt);
    });

    ctrlSenderAccountSelect.value = currentVal;
  }

  function renderSenderAccounts() {
    updateCtrlSenderAccountSelect();
    if (tabSendersCount) tabSendersCount.textContent = senderAccounts.length;
    if (!sendersCardsContainer) return;

    sendersCardsContainer.innerHTML = '';
    if (senderAccounts.length === 0) {
      sendersCardsContainer.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; background: rgba(18, 24, 38, 0.8); border-radius: 12px; border: 1px dashed var(--border-color);">
          <i class="fa-solid fa-at" style="font-size: 32px; color: var(--gold-bright); margin-bottom: 12px;"></i>
          <h3 style="color:#fff;">No Sender Email Accounts Configured</h3>
          <p class="card-desc">Click "Add Email Account" above to connect Hostinger, Gmail, or custom SMTPs for auto-rotation.</p>
        </div>
      `;
      return;
    }

    senderAccounts.forEach(acc => {
      const isFull = acc.sent_today >= acc.daily_limit;
      const pct = Math.min(100, Math.round((acc.sent_today / acc.daily_limit) * 100));
      const providerIcon = acc.provider === 'gmail' 
        ? '<i class="fa-brands fa-google" style="color: #ea4335;"></i>' 
        : (acc.provider === 'hostinger' ? '<i class="fa-solid fa-server" style="color: #a855f7;"></i>' : '<i class="fa-solid fa-envelope text-gold"></i>');
      
      const badgeHtml = !acc.enabled 
        ? '<span class="badge badge-idle" style="background: rgba(255,255,255,0.08); color: #94a3b8;"><i class="fa-solid fa-power-off"></i> Disabled</span>'
        : (isFull 
            ? '<span class="badge badge-warning" style="background: rgba(239, 68, 68, 0.15); color: #f87171;"><i class="fa-solid fa-triangle-exclamation"></i> 80 Limit Full</span>'
            : '<span class="badge badge-running" style="background: rgba(34, 197, 94, 0.15); color: #4ade80;"><i class="fa-solid fa-circle-check"></i> Ready</span>');

      const card = document.createElement('div');
      card.className = 'card sender-account-card';
      card.style.cssText = 'position: relative; border: 1px solid var(--border-color); border-radius: 12px; padding: 18px; background: rgba(18, 24, 38, 0.8);';
      
      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; border-radius: 8px; background: rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: center; font-size: 20px;">
              ${providerIcon}
            </div>
            <div>
              <h3 style="font-size: 15px; margin: 0; color: #fff;">${escapeHtml(acc.name)}</h3>
              <code style="font-size: 12px; color: var(--gold-bright);">${escapeHtml(acc.sender_email)}</code>
            </div>
          </div>
          <div>${badgeHtml}</div>
        </div>

        <div style="margin: 14px 0 10px 0;">
          <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
            <span style="color: var(--text-muted);">Today's Dispatched Progress:</span>
            <strong style="color: ${isFull ? '#f87171' : 'var(--gold-bright)'};">${acc.sent_today} / ${acc.daily_limit} emails</strong>
          </div>
          <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
            <div style="width: ${pct}%; height: 100%; background: ${isFull ? '#f87171' : 'linear-gradient(90deg, #f59e0b, #eab308)'}; transition: width 0.4s ease;"></div>
          </div>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 14px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 12px;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <label style="font-size: 11px; color: var(--text-muted);">Daily Limit:</label>
            <input type="number" class="form-input acc-limit-input" data-id="${acc.id}" value="${acc.daily_limit}" style="width: 70px; padding: 4px 6px; font-size: 12px;" min="1" max="5000">
            <button class="btn btn-xs btn-outline btn-save-acc-limit" data-id="${acc.id}" title="Save limit"><i class="fa-solid fa-check"></i></button>
          </div>

          <div style="display: flex; gap: 6px;">
            <button class="btn btn-xs btn-outline btn-test-acc" data-id="${acc.id}" data-email="${escapeHtml(acc.sender_email)}" title="Send test email from this account">
              <i class="fa-solid fa-paper-plane"></i> Test
            </button>
            <button class="btn btn-xs ${acc.enabled ? 'btn-warning' : 'btn-secondary'} btn-toggle-acc" data-id="${acc.id}" data-enabled="${acc.enabled}">
              <i class="fa-solid fa-power-off"></i> ${acc.enabled ? 'Disable' : 'Enable'}
            </button>
            <button class="btn btn-xs btn-danger btn-delete-acc" data-id="${acc.id}" title="Delete account">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        </div>
      `;

      sendersCardsContainer.appendChild(card);
    });

    attachSenderCardEvents();
  }

  function attachSenderCardEvents() {
    // Save Limit
    document.querySelectorAll('.btn-save-acc-limit').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-id');
        const input = document.querySelector(`.acc-limit-input[data-id="${id}"]`);
        const limitVal = parseInt(input.value, 10);
        if (!limitVal || limitVal < 1) return alert('Enter a valid daily limit.');
        
        try {
          const res = await fetch('/api/senders/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_id: id, daily_limit: limitVal })
          });
          const data = await res.json();
          if (data.success) {
            loadSenderAccounts();
            fetchStats();
          } else {
            alert(data.error || 'Failed to update limit.');
          }
        } catch (err) {
          alert('Error: ' + err.message);
        }
      });
    });

    // Toggle Account (Enable / Disable)
    document.querySelectorAll('.btn-toggle-acc').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-id');
        const currentEnabled = parseInt(btn.getAttribute('data-enabled'), 10);
        const newEnabled = currentEnabled ? 0 : 1;

        try {
          const res = await fetch('/api/senders/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_id: id, enabled: newEnabled })
          });
          const data = await res.json();
          if (data.success) {
            loadSenderAccounts();
            fetchStats();
          } else {
            alert(data.error || 'Failed to toggle account.');
          }
        } catch (err) {
          alert('Error: ' + err.message);
        }
      });
    });

    // Delete Account
    document.querySelectorAll('.btn-delete-acc').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-id');
        if (!confirm('Are you sure you want to delete this sender account?')) return;
        try {
          const res = await fetch('/api/senders/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ account_id: id })
          });
          const data = await res.json();
          if (data.success) {
            loadSenderAccounts();
            fetchStats();
          } else {
            alert(data.error || 'Failed to delete account.');
          }
        } catch (err) {
          alert('Error: ' + err.message);
        }
      });
    });

    // Test Account
    document.querySelectorAll('.btn-test-acc').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-id');
        const email = btn.getAttribute('data-email');
        const testTo = prompt(`Send a test email from [${email}] to:`, testEmailInput ? testEmailInput.value : '');
        if (!testTo || !testTo.includes('@')) return;

        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        try {
          const res = await fetch('/api/test-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              account_id: id,
              to_email: testTo,
              subject: ctrlSubject ? ctrlSubject.value : 'Test Email',
              sender_name: ctrlSenderName ? ctrlSenderName.value : 'Winning Heaven VIP',
              html_body: editorHtml ? editorHtml.value : '<p>Test email</p>',
              plain_body: editorPlain ? editorPlain.value : 'Test email'
            })
          });
          const data = await res.json();
          alert(data.message || (data.success ? 'Test email sent!' : data.error));
        } catch (err) {
          alert('Test email error: ' + err.message);
        } finally {
          btn.disabled = false;
          btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Test';
        }
      });
    });
  }

  // Modal Open / Close Handlers for Add Sender Account
  if (btnOpenAddSenderModal) {
    btnOpenAddSenderModal.addEventListener('click', () => {
      if (addSenderModalMsg) addSenderModalMsg.style.display = 'none';
      if (modalAddSender) modalAddSender.style.display = 'flex';
    });
  }

  if (btnCloseAddSenderModal) {
    btnCloseAddSenderModal.addEventListener('click', () => {
      if (modalAddSender) modalAddSender.style.display = 'none';
    });
  }

  if (btnCancelAddSender) {
    btnCancelAddSender.addEventListener('click', () => {
      if (modalAddSender) modalAddSender.style.display = 'none';
    });
  }

  if (modalAddSender) {
    modalAddSender.addEventListener('click', (e) => {
      if (e.target === modalAddSender) modalAddSender.style.display = 'none';
    });
  }

  // Preset Buttons
  if (presetBtnHostinger) {
    presetBtnHostinger.addEventListener('click', () => {
      presetBtnHostinger.classList.add('active');
      if (presetBtnGmail) presetBtnGmail.classList.remove('active');
      if (presetBtnCustom) presetBtnCustom.classList.remove('active');

      document.getElementById('sender-provider').value = 'hostinger';
      document.getElementById('sender-name-label').value = 'Hostinger Main';
      document.getElementById('sender-host-input').value = 'smtp.hostinger.com';
      document.getElementById('sender-port-input').value = 465;
      document.getElementById('sender-use-ssl').checked = true;
      if (gmailNoticeBox) gmailNoticeBox.style.display = 'none';
    });
  }

  if (presetBtnGmail) {
    presetBtnGmail.addEventListener('click', () => {
      if (presetBtnHostinger) presetBtnHostinger.classList.remove('active');
      presetBtnGmail.classList.add('active');
      if (presetBtnCustom) presetBtnCustom.classList.remove('active');

      document.getElementById('sender-provider').value = 'gmail';
      document.getElementById('sender-name-label').value = 'Gmail Personal 1';
      document.getElementById('sender-host-input').value = 'smtp.gmail.com';
      document.getElementById('sender-port-input').value = 587;
      document.getElementById('sender-use-ssl').checked = false;
      if (gmailNoticeBox) gmailNoticeBox.style.display = 'block';
    });
  }

  if (presetBtnCustom) {
    presetBtnCustom.addEventListener('click', () => {
      if (presetBtnHostinger) presetBtnHostinger.classList.remove('active');
      if (presetBtnGmail) presetBtnGmail.classList.remove('active');
      presetBtnCustom.classList.add('active');

      document.getElementById('sender-provider').value = 'custom';
      document.getElementById('sender-name-label').value = 'Custom SMTP';
      document.getElementById('sender-host-input').value = '';
      document.getElementById('sender-port-input').value = 465;
      document.getElementById('sender-use-ssl').checked = true;
      if (gmailNoticeBox) gmailNoticeBox.style.display = 'none';
    });
  }

  // Submit Add Sender Form
  if (formAddSender) {
    formAddSender.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        name: document.getElementById('sender-name-label').value.trim(),
        provider: document.getElementById('sender-provider').value,
        sender_email: document.getElementById('sender-email-input').value.trim(),
        sender_password: document.getElementById('sender-pass-input').value.trim(),
        smtp_host: document.getElementById('sender-host-input').value.trim(),
        smtp_port: parseInt(document.getElementById('sender-port-input').value, 10),
        sender_name: document.getElementById('sender-display-name').value.trim(),
        daily_limit: parseInt(document.getElementById('sender-daily-limit').value, 10),
        use_ssl: document.getElementById('sender-use-ssl').checked
      };

      try {
        const res = await fetch('/api/senders/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
          if (addSenderModalMsg) {
            addSenderModalMsg.style.display = 'block';
            addSenderModalMsg.className = 'alert-box alert-success';
            addSenderModalMsg.textContent = data.message;
          }
          loadSenderAccounts();
          fetchStats();
          setTimeout(() => {
            if (modalAddSender) modalAddSender.style.display = 'none';
            formAddSender.reset();
          }, 1200);
        } else {
          if (addSenderModalMsg) {
            addSenderModalMsg.style.display = 'block';
            addSenderModalMsg.className = 'alert-box alert-danger';
            addSenderModalMsg.textContent = data.error || 'Failed to add sender account.';
          }
        }
      } catch (err) {
        if (addSenderModalMsg) {
          addSenderModalMsg.style.display = 'block';
          addSenderModalMsg.className = 'alert-box alert-danger';
          addSenderModalMsg.textContent = 'Error: ' + err.message;
        }
      }
    });
  }

  // ==================== 12. QUICK DAILY LIMIT MODAL ====================
  const modalDailyLimit = document.getElementById('modal-daily-limit');
  const btnOpenLimitModal = document.getElementById('btn-open-limit-modal');
  const btnCloseLimitModal = document.getElementById('btn-close-limit-modal');
  const modalTodaySent = document.getElementById('modal-today-sent');
  const modalCurrentLimit = document.getElementById('modal-current-limit');
  const inputCustomLimit = document.getElementById('input-custom-limit');
  const btnSaveCustomLimit = document.getElementById('btn-save-custom-limit');
  const limitModalMsg = document.getElementById('limit-modal-msg');
  const btnPresetLimits = document.querySelectorAll('.btn-preset-limit');

  if (btnOpenLimitModal) {
    btnOpenLimitModal.addEventListener('click', () => {
      if (modalTodaySent && statTodaySent) modalTodaySent.textContent = statTodaySent.textContent;
      if (modalCurrentLimit && statDailyLimit) modalCurrentLimit.textContent = statDailyLimit.textContent;
      if (inputCustomLimit && statDailyLimit) inputCustomLimit.value = statDailyLimit.textContent.replace(/,/g, '');
      if (limitModalMsg) limitModalMsg.style.display = 'none';
      if (modalDailyLimit) modalDailyLimit.style.display = 'flex';
    });
  }

  if (btnCloseLimitModal) {
    btnCloseLimitModal.addEventListener('click', () => {
      if (modalDailyLimit) modalDailyLimit.style.display = 'none';
    });
  }

  if (modalDailyLimit) {
    modalDailyLimit.addEventListener('click', (e) => {
      if (e.target === modalDailyLimit) {
        modalDailyLimit.style.display = 'none';
      }
    });
  }

  async function applyDailyLimitUpdate(payload) {
    try {
      const res = await fetch('/api/daily-limit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        if (limitModalMsg) {
          limitModalMsg.style.display = 'block';
          limitModalMsg.className = 'alert-box alert-success';
          limitModalMsg.textContent = data.message;
        }
        fetchStats();
        loadSettings();
        setTimeout(() => {
          if (modalDailyLimit) modalDailyLimit.style.display = 'none';
        }, 1200);
      } else {
        if (limitModalMsg) {
          limitModalMsg.style.display = 'block';
          limitModalMsg.className = 'alert-box alert-danger';
          limitModalMsg.textContent = data.error || 'Failed to update limit.';
        }
      }
    } catch (err) {
      if (limitModalMsg) {
        limitModalMsg.style.display = 'block';
        limitModalMsg.className = 'alert-box alert-danger';
        limitModalMsg.textContent = 'Error: ' + err.message;
      }
    }
  }

  btnPresetLimits.forEach(btn => {
    btn.addEventListener('click', () => {
      const extend = btn.getAttribute('data-extend');
      const limit = btn.getAttribute('data-limit');
      if (extend) {
        applyDailyLimitUpdate({ extend_by: parseInt(extend, 10) });
      } else if (limit) {
        applyDailyLimitUpdate({ daily_limit: parseInt(limit, 10) });
      }
    });
  });

  if (btnSaveCustomLimit) {
    btnSaveCustomLimit.addEventListener('click', () => {
      const customVal = parseInt(inputCustomLimit.value, 10);
      if (!customVal || customVal < 1) {
        alert('Please enter a valid daily limit number.');
        return;
      }
      applyDailyLimitUpdate({ daily_limit: customVal });
    });
  }

  function escapeHtml(text) {
    if (!text) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // ==================== SMART LEAD CLEANER & DEDUPLICATOR ====================
  const cleanerRawInput = document.getElementById('cleaner-raw-input');
  const btnCleanFilter = document.getElementById('btn-clean-filter');
  const btnCleanerClear = document.getElementById('btn-cleaner-clear');
  const cleanerResultsBox = document.getElementById('cleaner-results-box');
  const cleanerPlaceholder = document.getElementById('cleaner-placeholder');
  const cleanerStatRaw = document.getElementById('cleaner-stat-raw');
  const cleanerStatDup = document.getElementById('cleaner-stat-dup');
  const cleanerStatUnique = document.getElementById('cleaner-stat-unique');
  const cleanerTargetFileSelect = document.getElementById('cleaner-target-file-select');
  const cleanerNewFilename = document.getElementById('cleaner-new-filename');
  const btnSaveCleanedLeads = document.getElementById('btn-save-cleaned-leads');
  const cleanerPreviewList = document.getElementById('cleaner-preview-list');
  const saveModeRadios = document.querySelectorAll('input[name="cleaner-save-mode"]');

  let currentCleanedEmails = [];

  // Populate target files select
  function populateCleanerTargetFiles() {
    if (!cleanerTargetFileSelect) return;
    cleanerTargetFileSelect.innerHTML = '';
    fetch('/api/files').then(res => res.json()).then(data => {
      const files = data.files || [];
      files.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f.name;
        opt.textContent = `${f.name} (${f.total} leads)`;
        cleanerTargetFileSelect.appendChild(opt);
      });
    }).catch(err => console.error('Error loading cleaner target files:', err));
  }

  populateCleanerTargetFiles();

  if (btnCleanerClear) {
    btnCleanerClear.addEventListener('click', () => {
      if (cleanerRawInput) cleanerRawInput.value = '';
      if (cleanerResultsBox) cleanerResultsBox.style.display = 'none';
      if (cleanerPlaceholder) cleanerPlaceholder.style.display = 'block';
      currentCleanedEmails = [];
    });
  }

  // Toggle mode inputs
  saveModeRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      if (radio.value === 'merge') {
        if (cleanerTargetFileSelect) cleanerTargetFileSelect.style.display = 'block';
        if (cleanerNewFilename) cleanerNewFilename.style.display = 'none';
      } else {
        if (cleanerTargetFileSelect) cleanerTargetFileSelect.style.display = 'none';
        if (cleanerNewFilename) cleanerNewFilename.style.display = 'block';
      }
      if (cleanerRawInput && cleanerRawInput.value.trim()) {
        if (btnCleanFilter) btnCleanFilter.click();
      }
    });
  });

  if (btnCleanFilter) {
    btnCleanFilter.addEventListener('click', async () => {
      const rawText = cleanerRawInput ? cleanerRawInput.value.trim() : '';
      if (!rawText) {
        alert('Please paste raw emails into the box first!');
        return;
      }

      btnCleanFilter.disabled = true;
      btnCleanFilter.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cleaning & Deduplicating...';

      const selectedModeRadio = document.querySelector('input[name="cleaner-save-mode"]:checked');
      const selectedMode = selectedModeRadio ? selectedModeRadio.value : 'new';
      const targetFile = cleanerTargetFileSelect ? cleanerTargetFileSelect.value : '';

      try {
        const res = await fetch('/api/leads/clean', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ raw_text: rawText, target_file: targetFile, mode: selectedMode })
        });
        const data = await res.json();

        if (data.success) {
          currentCleanedEmails = data.new_unique_emails || [];

          if (cleanerStatRaw) cleanerStatRaw.textContent = data.raw_count.toLocaleString();
          if (cleanerStatDup) cleanerStatDup.textContent = (data.duplicates_in_input + (selectedMode === 'merge' ? data.already_in_target_file : 0)).toLocaleString();
          if (cleanerStatUnique) cleanerStatUnique.textContent = currentCleanedEmails.length.toLocaleString();

          if (cleanerPreviewList) {
            if (currentCleanedEmails.length === 0) {
              cleanerPreviewList.innerHTML = '<em style="color:#ef4444;">No new unique emails found.</em>';
            } else {
              cleanerPreviewList.innerHTML = currentCleanedEmails.slice(0, 50).map(e => `<div>✓ ${escapeHtml(e)}</div>`).join('') +
                (currentCleanedEmails.length > 50 ? `<div style="color:#eab308; margin-top:4px;">... and ${currentCleanedEmails.length - 50} more unique emails.</div>` : '');
            }
          }

          if (cleanerPlaceholder) cleanerPlaceholder.style.display = 'none';
          if (cleanerResultsBox) cleanerResultsBox.style.display = 'block';

        } else {
          alert(data.error || 'Failed to filter emails.');
        }
      } catch (err) {
        alert('Cleaning error: ' + err.message);
      } finally {
        btnCleanFilter.disabled = false;
        btnCleanFilter.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> 1-Click Clean & Deduplicate';
      }
    });
  }

  if (btnSaveCleanedLeads) {
    btnSaveCleanedLeads.addEventListener('click', async () => {
      if (currentCleanedEmails.length === 0) {
        alert('No unique cleaned emails available to save. Please clean raw emails first!');
        return;
      }

      const selectedModeRadio = document.querySelector('input[name="cleaner-save-mode"]:checked');
      const selectedMode = selectedModeRadio ? selectedModeRadio.value : 'new';
      const targetFile = cleanerTargetFileSelect ? cleanerTargetFileSelect.value : '';
      const newFilename = cleanerNewFilename ? cleanerNewFilename.value.trim() : '';

      if (selectedMode === 'new' && !newFilename) {
        alert('Please type a filename for the new CSV list!');
        return;
      }

      btnSaveCleanedLeads.disabled = true;
      btnSaveCleanedLeads.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving & Syncing DB...';

      try {
        const res = await fetch('/api/leads/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            emails: currentCleanedEmails,
            mode: selectedMode,
            target_file: targetFile,
            filename: newFilename
          })
        });
        const data = await res.json();

        if (data.success) {
          alert(data.message || 'Saved successfully!');
          await loadFiles();
          await fetchStats();
          populateCleanerTargetFiles();
          
          if (cleanerRawInput) cleanerRawInput.value = '';
          if (cleanerResultsBox) cleanerResultsBox.style.display = 'none';
          if (cleanerPlaceholder) cleanerPlaceholder.style.display = 'block';
          currentCleanedEmails = [];
        } else {
          alert(data.error || 'Failed to save leads.');
        }
      } catch (err) {
        alert('Save error: ' + err.message);
      } finally {
        btnSaveCleanedLeads.disabled = false;
        btnSaveCleanedLeads.innerHTML = '<i class="fa-solid fa-cloud-arrow-up"></i> Save List & Sync to Campaign Dispatcher';
      }
    });
  }

  // ==================== DEEP EMAIL VERIFIER & LIST SCRUBBER ====================
  const verifierFileSelect = document.getElementById('verifier-file-select');
  const verifierEngineSelect = document.getElementById('verifier-engine-select');
  const btnStartVerify = document.getElementById('btn-start-verify');
  const verifierSingleInput = document.getElementById('verifier-single-input');
  const btnVerifySingle = document.getElementById('btn-verify-single');
  const verifierSingleResult = document.getElementById('verifier-single-result');
  const verifierStatusLabel = document.getElementById('verifier-status-label');
  const verifierSpinner = document.getElementById('verifier-spinner');
  const verifierProgressPercent = document.getElementById('verifier-progress-percent');
  const verifierProgressBar = document.getElementById('verifier-progress-bar');
  const verifierCurrentScanning = document.getElementById('verifier-current-scanning');
  const verifierStatDeliverable = document.getElementById('verifier-stat-deliverable');
  const verifierStatDead = document.getElementById('verifier-stat-dead');
  const verifierStatRisky = document.getElementById('verifier-stat-risky');
  const verifierActionsBox = document.getElementById('verifier-actions-box');
  const btnApplyVerifierClean = document.getElementById('btn-apply-verifier-clean');
  const verifierDetailContainer = document.getElementById('verifier-detail-container');
  const verifierDetailList = document.getElementById('verifier-detail-list');
  const vtabDeadCount = document.getElementById('vtab-dead-count');
  const vtabRiskyCount = document.getElementById('vtab-risky-count');
  const vtabDeliverableCount = document.getElementById('vtab-deliverable-count');
  const verifierTabBtns = document.querySelectorAll('.verifier-tab-btn');

  let verifierPollingInterval = null;
  let lastVerifierStatus = null;
  let currentVerifierTab = 'dead';

  function renderVerifierDetails(tab = 'dead') {
    if (!verifierDetailList || !lastVerifierStatus) return;
    currentVerifierTab = tab;

    // Update active tab styles
    verifierTabBtns.forEach(btn => {
      const vtab = btn.getAttribute('data-vtab');
      if (vtab === tab) {
        btn.classList.add('active');
        if (vtab === 'dead') {
          btn.style.background = 'rgba(239, 68, 68, 0.25)';
          btn.style.borderColor = 'rgba(239, 68, 68, 0.5)';
        } else if (vtab === 'risky') {
          btn.style.background = 'rgba(245, 158, 11, 0.25)';
          btn.style.borderColor = 'rgba(245, 158, 11, 0.5)';
        } else {
          btn.style.background = 'rgba(34, 197, 94, 0.25)';
          btn.style.borderColor = 'rgba(34, 197, 94, 0.5)';
        }
      } else {
        btn.classList.remove('active');
        btn.style.background = 'rgba(255, 255, 255, 0.05)';
        btn.style.borderColor = 'rgba(255, 255, 255, 0.15)';
      }
    });

    if (tab === 'dead') {
      const deadList = lastVerifierStatus.dead_emails || [];
      if (deadList.length === 0) {
        verifierDetailList.innerHTML = '<div style="color:#4ade80; text-align:center; padding:12px;">🎉 Zero dead emails detected! All emails have valid servers.</div>';
      } else {
        verifierDetailList.innerHTML = deadList.map(item => `
          <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); gap:8px;">
            <div style="color:#f87171; font-weight:700;">✗ ${escapeHtml(item.clean_email || item.email)}</div>
            <div style="color:#fca5a5; font-size:10px; background:rgba(239,68,68,0.15); padding:2px 6px; border-radius:4px; border:1px solid rgba(239,68,68,0.3); max-width:50%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
              ${escapeHtml(item.reason || 'Mailbox dead')}
            </div>
          </div>
        `).join('');
      }
    } else if (tab === 'risky') {
      const riskyList = lastVerifierStatus.risky_emails || [];
      if (riskyList.length === 0) {
        verifierDetailList.innerHTML = '<div style="color:#94a3b8; text-align:center; padding:12px;">No risky or disposable trap emails found.</div>';
      } else {
        verifierDetailList.innerHTML = riskyList.map(item => `
          <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05); gap:8px;">
            <div style="color:#fbbf24; font-weight:700;">⚠ ${escapeHtml(item.clean_email || item.email)}</div>
            <div style="color:#fcd34d; font-size:10px; background:rgba(245,158,11,0.15); padding:2px 6px; border-radius:4px; border:1px solid rgba(245,158,11,0.3); max-width:50%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
              ${escapeHtml(item.reason || 'Risky account')}
            </div>
          </div>
        `).join('');
      }
    } else if (tab === 'deliverable') {
      const sampleList = lastVerifierStatus.sample_deliverable || [];
      if (sampleList.length === 0) {
        verifierDetailList.innerHTML = '<div style="color:#94a3b8; text-align:center; padding:12px;">No deliverable emails to display.</div>';
      } else {
        verifierDetailList.innerHTML = sampleList.map(em => `
          <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.05);">
            <div style="color:#4ade80; font-weight:600;">✓ ${escapeHtml(em)}</div>
            <div style="color:#86efac; font-size:10px; background:rgba(34,197,94,0.15); padding:2px 6px; border-radius:4px;">Active Mailbox</div>
          </div>
        `).join('') + (lastVerifierStatus.deliverable_count > 50 ? `<div style="color:#94a3b8; text-align:center; padding:6px; font-size:10px;">... and ${(lastVerifierStatus.deliverable_count - 50).toLocaleString()} more deliverable inboxes.</div>` : '');
      }
    }
  }

  verifierTabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const vtab = btn.getAttribute('data-vtab');
      renderVerifierDetails(vtab);
    });
  });

  function populateVerifierFiles() {
    if (!verifierFileSelect) return;
    verifierFileSelect.innerHTML = '';
    fetch('/api/files').then(res => res.json()).then(data => {
      const files = data.files || [];
      files.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f.name;
        opt.textContent = `${f.name} (${f.total} leads)`;
        verifierFileSelect.appendChild(opt);
      });
    }).catch(err => console.error('Error loading verifier files:', err));
  }

  populateVerifierFiles();

  if (btnStartVerify) {
    btnStartVerify.addEventListener('click', async () => {
      const selectedFile = verifierFileSelect ? verifierFileSelect.value : '';
      if (!selectedFile) {
        alert('Please select a file to verify!');
        return;
      }

      btnStartVerify.disabled = true;
      btnStartVerify.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Verifying...';
      if (verifierSpinner) verifierSpinner.style.display = 'inline-block';
      if (verifierActionsBox) verifierActionsBox.style.display = 'none';
      if (verifierDetailContainer) verifierDetailContainer.style.display = 'block';

      try {
        const res = await fetch('/api/verifier/start', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_name: selectedFile, check_smtp: true })
        });
        const data = await res.json();
        if (data.success) {
          startVerifierPolling();
        } else {
          alert(data.error || 'Failed to start verification.');
          btnStartVerify.disabled = false;
          btnStartVerify.innerHTML = '<i class="fa-solid fa-play"></i> Run Deep Verification';
          if (verifierSpinner) verifierSpinner.style.display = 'none';
        }
      } catch (err) {
        alert('Network error starting verifier: ' + err.message);
        btnStartVerify.disabled = false;
        btnStartVerify.innerHTML = '<i class="fa-solid fa-play"></i> Run Deep Verification';
        if (verifierSpinner) verifierSpinner.style.display = 'none';
      }
    });
  }

  function startVerifierPolling() {
    if (verifierPollingInterval) clearInterval(verifierPollingInterval);
    verifierPollingInterval = setInterval(async () => {
      try {
        const res = await fetch('/api/verifier/status');
        const status = await res.json();
        lastVerifierStatus = status;

        if (verifierProgressPercent) verifierProgressPercent.textContent = `${status.percent}%`;
        if (verifierProgressBar) verifierProgressBar.style.width = `${status.percent}%`;
        if (verifierCurrentScanning) {
          verifierCurrentScanning.textContent = status.is_running ? `Checking: ${status.current_email} (${status.progress}/${status.total})` : `Completed ${status.total} leads scanned!`;
        }

        if (verifierStatDeliverable) verifierStatDeliverable.textContent = status.deliverable_count.toLocaleString();
        if (verifierStatDead) verifierStatDead.textContent = status.dead_count.toLocaleString();
        if (verifierStatRisky) verifierStatRisky.textContent = status.risky_count.toLocaleString();

        if (vtabDeadCount) vtabDeadCount.textContent = status.dead_count.toLocaleString();
        if (vtabRiskyCount) vtabRiskyCount.textContent = status.risky_count.toLocaleString();
        if (vtabDeliverableCount) vtabDeliverableCount.textContent = status.deliverable_count.toLocaleString();

        if (verifierStatusLabel) {
          verifierStatusLabel.innerHTML = status.is_running ? '<i class="fa-solid fa-circle-notch fa-spin text-gold"></i> Status: Scanning in progress...' : '<i class="fa-solid fa-circle-check" style="color:#4ade80;"></i> Status: Verification Complete!';
        }

        renderVerifierDetails(currentVerifierTab);

        if (!status.is_running) {
          clearInterval(verifierPollingInterval);
          verifierPollingInterval = null;
          if (btnStartVerify) {
            btnStartVerify.disabled = false;
            btnStartVerify.innerHTML = '<i class="fa-solid fa-play"></i> Run Deep Verification';
          }
          if (verifierSpinner) verifierSpinner.style.display = 'none';
          if (verifierActionsBox) {
            verifierActionsBox.style.display = 'flex';
          }
        }
      } catch (err) {
        console.error('Error polling verifier status:', err);
      }
    }, 600);
  }

  if (btnApplyVerifierClean) {
    btnApplyVerifierClean.addEventListener('click', async () => {
      const selectedFile = verifierFileSelect ? verifierFileSelect.value : '';
      if (!confirm(`Are you sure you want to purge all dead/invalid emails from '${selectedFile}' and sync to database?`)) {
        return;
      }

      btnApplyVerifierClean.disabled = true;
      btnApplyVerifierClean.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Cleaning & Purging DB...';

      try {
        const res = await fetch('/api/verifier/apply', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ target_file: selectedFile })
        });
        const data = await res.json();
        if (data.success) {
          alert(data.message || 'Clean list applied successfully!');
          await loadFiles();
          await fetchStats();
          populateVerifierFiles();
          populateCleanerTargetFiles();
          if (verifierActionsBox) verifierActionsBox.style.display = 'none';
        } else {
          alert(data.error || 'Failed to apply clean list.');
        }
      } catch (err) {
        alert('Error applying clean list: ' + err.message);
      } finally {
        btnApplyVerifierClean.disabled = false;
        btnApplyVerifierClean.innerHTML = '<i class="fa-solid fa-trash-can"></i> 1-Click Purge Dead Emails & Sync Campaign';
      }
    });
  }

  if (btnVerifySingle) {
    btnVerifySingle.addEventListener('click', async () => {
      const email = verifierSingleInput ? verifierSingleInput.value.trim() : '';
      if (!email) {
        alert('Please enter an email address to test!');
        return;
      }

      btnVerifySingle.disabled = true;
      btnVerifySingle.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
      if (verifierSingleResult) verifierSingleResult.style.display = 'none';

      try {
        const res = await fetch('/api/verifier/single', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, check_smtp: true })
        });
        const data = await res.json();
        if (data.success) {
          const r = data.result;
          if (verifierSingleResult) {
            let badgeClass = r.deliverable ? 'color:#4ade80; background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.3);' : (r.status === 'dead' ? 'color:#f87171; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.3);' : 'color:#fbbf24; background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.3);');
            let icon = r.deliverable ? '✓ Active Mailbox' : (r.status === 'dead' ? '✗ Dead / Invalid' : '⚠ Risky');
            verifierSingleResult.innerHTML = `<div style="padding:8px 12px; border-radius:6px; font-weight:700; ${badgeClass}">
              ${icon} - ${escapeHtml(r.clean_email || email)} <span style="font-weight:normal; font-size:11px; margin-left:6px;">(${escapeHtml(r.reason)})</span>
            </div>`;
            verifierSingleResult.style.display = 'block';
          }
        }
      } catch (err) {
        alert('Single verify error: ' + err.message);
      } finally {
        btnVerifySingle.disabled = false;
        btnVerifySingle.innerHTML = '<i class="fa-solid fa-bolt"></i> Test';
      }
    });
  }

  // ==================== 10. PEER-TO-PEER GMAIL WARMUP POOL ====================
  let warmupAccounts = [];
  let warmupLogs = [];
  let isWarmupEngineActive = false;

  // DOM Elements - Warmup Tab
  const tabWarmupCount = document.getElementById('tab-warmup-count');
  const warmupStatTotal = document.getElementById('warmup-stat-total');
  const warmupStatMature = document.getElementById('warmup-stat-mature');
  const warmupStatSentToday = document.getElementById('warmup-stat-sent-today');
  const warmupStatRepliesToday = document.getElementById('warmup-stat-replies-today');
  const warmupStatUnspammedToday = document.getElementById('warmup-stat-unspammed-today');
  const warmupStatAvgHealth = document.getElementById('warmup-stat-avg-health');
  const warmupEngineStatusBadge = document.getElementById('warmup-engine-status-badge');
  const btnToggleWarmupEngine = document.getElementById('btn-toggle-warmup-engine');
  const warmupTableCount = document.getElementById('warmup-table-count');
  const warmupAccountsTableBody = document.getElementById('warmup-accounts-table-body');
  const warmupSearchInput = document.getElementById('warmup-search-input');
  const chkSelectAllWarmup = document.getElementById('chk-select-all-warmup');
  const btnGraduateSelected = document.getElementById('btn-graduate-selected');
  const btnRefreshWarmup = document.getElementById('btn-refresh-warmup');
  const warmupConsole = document.getElementById('warmup-console');
  const btnClearWarmupLogs = document.getElementById('btn-clear-warmup-logs');

  // Single Add Modal Elements
  const modalAddWarmup = document.getElementById('modal-add-warmup');
  const btnOpenAddWarmup = document.getElementById('btn-open-add-warmup');
  const btnCloseAddWarmup = document.getElementById('btn-close-add-warmup');
  const formAddWarmup = document.getElementById('form-add-warmup');
  const warmupInputEmail = document.getElementById('warmup-input-email');
  const warmupInputPwd = document.getElementById('warmup-input-pwd');
  const warmupInputName = document.getElementById('warmup-input-name');
  const btnTestWarmupAccount = document.getElementById('btn-test-warmup-account');
  const addWarmupModalMsg = document.getElementById('add-warmup-modal-msg');

  // Bulk Import Modal Elements
  const modalBulkWarmup = document.getElementById('modal-bulk-warmup');
  const btnOpenBulkWarmup = document.getElementById('btn-open-bulk-warmup');
  const btnCloseBulkWarmup = document.getElementById('btn-close-bulk-warmup');
  const btnCancelBulkWarmup = document.getElementById('btn-cancel-bulk-warmup');
  const formBulkWarmup = document.getElementById('form-bulk-warmup');
  const bulkWarmupTextarea = document.getElementById('bulk-warmup-textarea');
  const bulkWarmupModalMsg = document.getElementById('bulk-warmup-modal-msg');

  async function loadWarmupData() {
    try {
      const [statsRes, accountsRes, logsRes] = await Promise.all([
        fetch('/api/warmup/stats'),
        fetch('/api/warmup/accounts'),
        fetch('/api/warmup/logs')
      ]);

      const statsData = await statsRes.json();
      const accountsData = await accountsRes.json();
      const logsData = await logsRes.json();

      if (statsData.success && statsData.stats) {
        renderWarmupStats(statsData.stats);
      }
      if (accountsData.success && accountsData.accounts) {
        warmupAccounts = accountsData.accounts;
        renderWarmupAccounts();
      }
      if (logsData.success && logsData.logs) {
        warmupLogs = logsData.logs;
        renderWarmupLogs();
      }
    } catch (err) {
      console.error('Error loading warmup data:', err);
    }
  }

  function renderWarmupStats(s) {
    if (tabWarmupCount) tabWarmupCount.textContent = s.total_accounts || 0;
    if (warmupTableCount) warmupTableCount.textContent = `${s.total_accounts || 0} Accounts`;
    if (warmupStatTotal) warmupStatTotal.textContent = s.total_accounts || 0;
    if (warmupStatMature) warmupStatMature.textContent = s.mature_accounts || 0;
    if (warmupStatSentToday) warmupStatSentToday.textContent = s.sent_today || 0;
    if (warmupStatRepliesToday) warmupStatRepliesToday.textContent = s.replied_today || 0;
    if (warmupStatUnspammedToday) warmupStatUnspammedToday.textContent = s.unspammed_today || 0;
    if (warmupStatAvgHealth) warmupStatAvgHealth.textContent = `${s.avg_health || 0}%`;

    isWarmupEngineActive = !!s.is_engine_running;
    if (warmupEngineStatusBadge) {
      if (isWarmupEngineActive) {
        warmupEngineStatusBadge.style.background = 'rgba(34, 197, 94, 0.15)';
        warmupEngineStatusBadge.style.color = '#15803d';
        warmupEngineStatusBadge.innerHTML = '<i class="fa-solid fa-circle" style="font-size: 8px; color: #16a34a;"></i> Engine Running (P2P Active)';
      } else {
        warmupEngineStatusBadge.style.background = 'rgba(148, 163, 184, 0.15)';
        warmupEngineStatusBadge.style.color = '#64748b';
        warmupEngineStatusBadge.innerHTML = '<i class="fa-solid fa-circle" style="font-size: 8px;"></i> Engine Stopped';
      }
    }

    if (btnToggleWarmupEngine) {
      if (isWarmupEngineActive) {
        btnToggleWarmupEngine.className = 'btn btn-danger';
        btnToggleWarmupEngine.innerHTML = '<i class="fa-solid fa-pause"></i> <span>Stop Warmup Engine</span>';
      } else {
        btnToggleWarmupEngine.className = 'btn btn-success';
        btnToggleWarmupEngine.innerHTML = '<i class="fa-solid fa-play"></i> <span>Start Warmup Engine</span>';
      }
    }
  }

  function renderWarmupAccounts() {
    if (!warmupAccountsTableBody) return;
    const query = (warmupSearchInput ? warmupSearchInput.value : '').toLowerCase().trim();
    const filtered = warmupAccounts.filter(a => {
      if (!query) return true;
      return (a.email && a.email.toLowerCase().includes(query)) ||
             (a.name && a.name.toLowerCase().includes(query));
    });

    if (filtered.length === 0) {
      warmupAccountsTableBody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center text-muted" style="padding: 35px;">
            <i class="fa-solid fa-inbox" style="font-size: 28px; margin-bottom: 8px; display: block; color: #94a3b8;"></i>
            No Gmail accounts found in the Warmup Pool.<br>
            <span style="font-size: 12px;">Click <strong>"Bulk Import (50+ Accounts)"</strong> or <strong>"Add Gmail"</strong> above to add your accounts!</span>
          </td>
        </tr>
      `;
      return;
    }

    let rowsHtml = '';
    filtered.forEach(acc => {
      const days = acc.warmup_days || 1;
      let stageBadge = '';
      if (days <= 4) {
        stageBadge = `<span class="badge badge-cold"><i class="fa-regular fa-snowflake"></i> Day ${days} (Cold: 4-8/day)</span>`;
      } else if (days <= 9) {
        stageBadge = `<span class="badge badge-maturing"><i class="fa-solid fa-fire"></i> Day ${days} (Maturing: 10-16/day)</span>`;
      } else {
        stageBadge = `<span class="badge badge-mature"><i class="fa-solid fa-circle-check"></i> Day ${days} (Mature: 18-25/day)</span>`;
      }

      const score = Math.max(0, Math.min(100, acc.health_score || 0));
      let barColor = '#64748b';
      if (score >= 90) barColor = '#16a34a';
      else if (score >= 50) barColor = '#f59e0b';

      let statusBadge = '';
      if (acc.is_graduated) {
        statusBadge = `<span class="badge badge-graduated"><i class="fa-solid fa-graduation-cap"></i> Graduated</span>`;
      } else if (acc.status === 'paused') {
        statusBadge = `<span class="badge badge-paused"><i class="fa-solid fa-pause"></i> Paused</span>`;
      } else if (score >= 90) {
        statusBadge = `<span class="badge badge-mature"><i class="fa-solid fa-circle-check"></i> Mature 🟢</span>`;
      } else {
        statusBadge = `<span class="badge badge-maturing"><i class="fa-solid fa-fire"></i> Warming</span>`;
      }

      const canGraduate = !acc.is_graduated;
      const graduateBtn = canGraduate 
        ? `<button class="btn-xs-action btn-warmup-graduate" data-id="${acc.id}" title="Graduate to active Campaign Senders (80 daily limit)" style="background: rgba(34, 197, 94, 0.12); color: #16a34a; border-color: rgba(34, 197, 94, 0.3);">
             <i class="fa-solid fa-graduation-cap"></i> Graduate
           </button>`
        : `<span style="font-size: 11px; color: #2563eb; font-weight: 600;"><i class="fa-solid fa-check"></i> In Senders</span>`;

      rowsHtml += `
        <tr>
          <td style="text-align: center;">
            <input type="checkbox" class="chk-warmup-item" data-id="${acc.id}" data-mature="${score >= 90 ? '1' : '0'}" ${acc.is_graduated ? 'disabled' : ''}>
          </td>
          <td>
            <div style="font-weight: 600; color: var(--text-primary); font-size: 13px; display: flex; align-items: center; gap: 6px;">
              <i class="fa-brands fa-google" style="color: #ea4335;"></i>
              ${escapeHtml(acc.email)}
            </div>
            ${acc.name ? `<div style="font-size: 11px; color: var(--text-muted);">${escapeHtml(acc.name)}</div>` : ''}
          </td>
          <td>${stageBadge}</td>
          <td>
            <div style="display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 700; color: ${barColor};">
              <span>Health Score</span>
              <span>${score}%</span>
            </div>
            <div class="health-bar-bg">
              <div class="health-bar-fill" style="width: ${score}%; background: ${barColor};"></div>
            </div>
          </td>
          <td>
            <div style="font-size: 12px; font-weight: 600; color: var(--text-primary);">
              ${acc.sent_today || 0} / ${acc.daily_target || 5} sent
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              ${acc.replied_today || 0} replies • ${acc.unspammed_today || 0} unspammed
            </div>
          </td>
          <td>
            <div style="font-size: 12px; color: var(--text-secondary);">
              <strong>${acc.total_sent || 0}</strong> sent • <strong>${acc.total_received || 0}</strong> recv
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">
              ${acc.total_replied || 0} replies • ${acc.total_unspammed || 0} unspammed
            </div>
          </td>
          <td>${statusBadge}</td>
          <td style="text-align: right;">
            <div style="display: inline-flex; gap: 6px; align-items: center;">
              ${graduateBtn}
              <button class="btn-xs-action btn-warmup-test" data-email="${acc.email}" data-pwd="${acc.password}" title="Test SMTP/IMAP login">
                <i class="fa-solid fa-bolt"></i>
              </button>
              <button class="btn-xs-action btn-warmup-toggle" data-id="${acc.id}" title="${acc.status === 'paused' ? 'Resume' : 'Pause'}">
                <i class="fa-solid ${acc.status === 'paused' ? 'fa-play' : 'fa-pause'}"></i>
              </button>
              <button class="btn-xs-action btn-warmup-delete" data-id="${acc.id}" data-email="${acc.email}" title="Delete account" style="color: #ef4444;">
                <i class="fa-solid fa-trash-can"></i>
              </button>
            </div>
          </td>
        </tr>
      `;
    });

    warmupAccountsTableBody.innerHTML = rowsHtml;
  }

  function renderWarmupLogs() {
    if (!warmupConsole) return;
    if (warmupLogs.length === 0) {
      warmupConsole.innerHTML = `<div style="color: #94a3b8;"><i class="fa-solid fa-info-circle"></i> Waiting for warmup activity... Click "Start Warmup Engine" to begin automated P2P exchanges.</div>`;
      return;
    }

    let logsHtml = '';
    warmupLogs.slice(0, 50).forEach(log => {
      let actionColor = '#38bdf8';
      let icon = 'fa-arrow-right';
      if (log.action === 'SENT_WARMUP') {
        actionColor = '#4ade80';
        icon = 'fa-paper-plane';
      } else if (log.action === 'AUTOREPLIED') {
        actionColor = '#c084fc';
        icon = 'fa-reply';
      } else if (log.action === 'UNSPAMMED') {
        actionColor = '#fbbf24';
        icon = 'fa-shield-virus';
      } else if (log.action === 'ERROR') {
        actionColor = '#f87171';
        icon = 'fa-triangle-exclamation';
      } else if (log.action === 'GRADUATED') {
        actionColor = '#34d399';
        icon = 'fa-graduation-cap';
      }

      logsHtml += `
        <div style="margin-bottom: 4px; display: flex; gap: 8px; flex-wrap: wrap;">
          <span style="color: #64748b;">[${log.timestamp || ''}]</span>
          <span style="color: ${actionColor}; font-weight: 700;"><i class="fa-solid ${icon}"></i> [${log.action}]</span>
          ${log.from_email ? `<span style="color: #cbd5e1;">${escapeHtml(log.from_email)}</span>` : ''}
          ${log.to_email ? `<span style="color: #94a3b8;">&rarr; ${escapeHtml(log.to_email)}</span>` : ''}
          <span style="color: #94a3b8;">${escapeHtml(log.details || '')}</span>
        </div>
      `;
    });

    warmupConsole.innerHTML = logsHtml;
  }

  // Toggle Warmup Engine (Start / Stop)
  if (btnToggleWarmupEngine) {
    btnToggleWarmupEngine.addEventListener('click', async () => {
      btnToggleWarmupEngine.disabled = true;
      const endpoint = isWarmupEngineActive ? '/api/warmup/engine/stop' : '/api/warmup/engine/start';
      try {
        const res = await fetch(endpoint, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
          await loadWarmupData();
        } else {
          alert('Warmup engine error: ' + (data.error || 'Failed to toggle.'));
        }
      } catch (err) {
        alert('Network error toggling warmup engine: ' + err.message);
      } finally {
        btnToggleWarmupEngine.disabled = false;
      }
    });
  }

  // Refresh Warmup Pool
  if (btnRefreshWarmup) {
    btnRefreshWarmup.addEventListener('click', () => {
      btnRefreshWarmup.classList.add('fa-spin');
      loadWarmupData().finally(() => {
        setTimeout(() => btnRefreshWarmup.classList.remove('fa-spin'), 600);
      });
    });
  }

  // Search Filter
  if (warmupSearchInput) {
    warmupSearchInput.addEventListener('input', () => {
      renderWarmupAccounts();
    });
  }

  // Select All Warmup Items
  if (chkSelectAllWarmup) {
    chkSelectAllWarmup.addEventListener('change', () => {
      const isChecked = chkSelectAllWarmup.checked;
      document.querySelectorAll('.chk-warmup-item:not(:disabled)').forEach(chk => {
        chk.checked = isChecked;
      });
    });
  }

  // Graduate Selected Accounts (Bulk)
  if (btnGraduateSelected) {
    btnGraduateSelected.addEventListener('click', async () => {
      const selected = Array.from(document.querySelectorAll('.chk-warmup-item:checked:not(:disabled)'));
      if (selected.length === 0) {
        alert('Please select one or more accounts to graduate into active Campaign Senders rotation.');
        return;
      }

      if (!confirm(`Are you sure you want to graduate ${selected.length} account(s) into active Campaign Senders? They will receive an 80 daily limit and start sending outreach marketing emails.`)) {
        return;
      }

      btnGraduateSelected.disabled = true;
      btnGraduateSelected.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Graduating...';

      let successCount = 0;
      for (const chk of selected) {
        const accId = chk.getAttribute('data-id');
        try {
          const res = await fetch('/api/warmup/accounts/graduate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: accId })
          });
          const d = await res.json();
          if (d.success) successCount++;
        } catch (e) {
          console.error('Graduate error:', e);
        }
      }

      btnGraduateSelected.disabled = false;
      btnGraduateSelected.innerHTML = '<i class="fa-solid fa-graduation-cap" style="color: #16a34a;"></i> Graduate Selected (🟢)';
      alert(`Successfully graduated ${successCount} account(s) to Campaign Senders!`);
      await loadWarmupData();
      await loadSenderAccounts();
    });
  }

  // Table Action Buttons (Graduate, Test, Toggle, Delete)
  if (warmupAccountsTableBody) {
    warmupAccountsTableBody.addEventListener('click', async (e) => {
      const btnGraduate = e.target.closest('.btn-warmup-graduate');
      const btnTest = e.target.closest('.btn-warmup-test');
      const btnToggle = e.target.closest('.btn-warmup-toggle');
      const btnDelete = e.target.closest('.btn-warmup-delete');

      if (btnGraduate) {
        const id = btnGraduate.getAttribute('data-id');
        if (!confirm('Graduate this account to active Campaign Senders? It will immediately be available in your campaign sender rotation with an 80/day safety cap.')) return;
        btnGraduate.disabled = true;
        btnGraduate.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        try {
          const res = await fetch('/api/warmup/accounts/graduate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id })
          });
          const data = await res.json();
          alert(data.message || (data.success ? 'Account graduated!' : 'Failed.'));
          await loadWarmupData();
          await loadSenderAccounts();
        } catch (err) {
          alert('Error: ' + err.message);
        }
      }

      if (btnTest) {
        const email = btnTest.getAttribute('data-email');
        const pwd = btnTest.getAttribute('data-pwd');
        btnTest.disabled = true;
        btnTest.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        try {
          const res = await fetch('/api/warmup/accounts/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: pwd })
          });
          const data = await res.json();
          if (data.success) {
            alert(`✅ Credentials Verified Successfully for ${email}!\n• SMTP SSL (465): Connected & Authenticated\n• IMAP SSL (993): Connected & Authenticated`);
          } else {
            const errs = (data.errors || []).join('\n');
            alert(`❌ Credential Test Failed for ${email}:\n${errs}\n\nPlease verify that 2-Step Verification is ON and a valid 16-character Google App Password was provided.`);
          }
        } catch (err) {
          alert('Network error testing credentials: ' + err.message);
        } finally {
          btnTest.disabled = false;
          btnTest.innerHTML = '<i class="fa-solid fa-bolt"></i>';
        }
      }

      if (btnToggle) {
        const id = btnToggle.getAttribute('data-id');
        btnToggle.disabled = true;
        try {
          const res = await fetch('/api/warmup/accounts/toggle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id })
          });
          const data = await res.json();
          if (data.success) {
            await loadWarmupData();
          }
        } catch (err) {
          console.error(err);
        }
      }

      if (btnDelete) {
        const id = btnDelete.getAttribute('data-id');
        const email = btnDelete.getAttribute('data-email');
        if (!confirm(`Are you sure you want to remove '${email}' from the Warmup Pool?`)) return;
        btnDelete.disabled = true;
        try {
          const res = await fetch('/api/warmup/accounts/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id })
          });
          const data = await res.json();
          if (data.success) {
            await loadWarmupData();
          }
        } catch (err) {
          alert('Delete error: ' + err.message);
        }
      }
    });
  }

  // Clear Warmup Console
  if (btnClearWarmupLogs) {
    btnClearWarmupLogs.addEventListener('click', () => {
      if (warmupConsole) {
        warmupConsole.innerHTML = `<div style="color: #94a3b8;"><i class="fa-solid fa-info-circle"></i> Stream cleared.</div>`;
      }
    });
  }

  // Modal: Add Single Warmup Account
  if (btnOpenAddWarmup && modalAddWarmup) {
    btnOpenAddWarmup.addEventListener('click', () => {
      if (formAddWarmup) formAddWarmup.reset();
      if (addWarmupModalMsg) addWarmupModalMsg.style.display = 'none';
      modalAddWarmup.style.display = 'flex';
    });
  }

  if (btnCloseAddWarmup && modalAddWarmup) {
    btnCloseAddWarmup.addEventListener('click', () => {
      modalAddWarmup.style.display = 'none';
    });
  }

  if (btnTestWarmupAccount) {
    btnTestWarmupAccount.addEventListener('click', async () => {
      const email = (warmupInputEmail ? warmupInputEmail.value : '').trim();
      const pwd = (warmupInputPwd ? warmupInputPwd.value : '').trim();
      if (!email || !pwd) {
        if (addWarmupModalMsg) {
          addWarmupModalMsg.className = 'alert-box alert-error';
          addWarmupModalMsg.textContent = 'Please fill in both Gmail address and 16-character App Password before testing.';
          addWarmupModalMsg.style.display = 'block';
        }
        return;
      }

      btnTestWarmupAccount.disabled = true;
      btnTestWarmupAccount.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Testing...';
      if (addWarmupModalMsg) addWarmupModalMsg.style.display = 'none';

      try {
        const res = await fetch('/api/warmup/accounts/test', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, password: pwd })
        });
        const data = await res.json();
        if (addWarmupModalMsg) {
          if (data.success) {
            addWarmupModalMsg.className = 'alert-box alert-success';
            addWarmupModalMsg.innerHTML = '<strong>✅ Test Passed!</strong> SMTP (465) &amp; IMAP (993) connected and authenticated successfully.';
          } else {
            addWarmupModalMsg.className = 'alert-box alert-error';
            addWarmupModalMsg.innerHTML = '<strong>❌ Test Failed!</strong> ' + ((data.errors || []).join(' | ') || 'Check 2-Step Verification and App Password.');
          }
          addWarmupModalMsg.style.display = 'block';
        }
      } catch (err) {
        if (addWarmupModalMsg) {
          addWarmupModalMsg.className = 'alert-box alert-error';
          addWarmupModalMsg.textContent = 'Test error: ' + err.message;
          addWarmupModalMsg.style.display = 'block';
        }
      } finally {
        btnTestWarmupAccount.disabled = false;
        btnTestWarmupAccount.innerHTML = '<i class="fa-solid fa-bolt"></i> Test Credentials';
      }
    });
  }

  if (formAddWarmup) {
    formAddWarmup.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = (warmupInputEmail ? warmupInputEmail.value : '').trim();
      const pwd = (warmupInputPwd ? warmupInputPwd.value : '').trim();
      const name = (warmupInputName ? warmupInputName.value : '').trim();

      if (!email || !pwd) return;

      const submitBtn = formAddWarmup.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';
      }

      try {
        const res = await fetch('/api/warmup/accounts/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email, password: pwd, name: name })
        });
        const data = await res.json();
        if (data.success) {
          if (addWarmupModalMsg) {
            addWarmupModalMsg.className = 'alert-box alert-success';
            addWarmupModalMsg.textContent = data.message;
            addWarmupModalMsg.style.display = 'block';
          }
          setTimeout(() => {
            if (modalAddWarmup) modalAddWarmup.style.display = 'none';
            loadWarmupData();
          }, 800);
        } else {
          if (addWarmupModalMsg) {
            addWarmupModalMsg.className = 'alert-box alert-error';
            addWarmupModalMsg.textContent = data.message || 'Failed to add account.';
            addWarmupModalMsg.style.display = 'block';
          }
        }
      } catch (err) {
        if (addWarmupModalMsg) {
          addWarmupModalMsg.className = 'alert-box alert-error';
          addWarmupModalMsg.textContent = 'Network error: ' + err.message;
          addWarmupModalMsg.style.display = 'block';
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<i class="fa-solid fa-plus"></i> Add to Warmup Pool';
        }
      }
    });
  }

  // Modal: Bulk Import Warmup Accounts (50+ Accounts)
  if (btnOpenBulkWarmup && modalBulkWarmup) {
    btnOpenBulkWarmup.addEventListener('click', () => {
      if (formBulkWarmup) formBulkWarmup.reset();
      if (bulkWarmupModalMsg) bulkWarmupModalMsg.style.display = 'none';
      modalBulkWarmup.style.display = 'flex';
    });
  }

  if (btnCloseBulkWarmup && modalBulkWarmup) {
    btnCloseBulkWarmup.addEventListener('click', () => {
      modalBulkWarmup.style.display = 'none';
    });
  }

  if (btnCancelBulkWarmup && modalBulkWarmup) {
    btnCancelBulkWarmup.addEventListener('click', () => {
      modalBulkWarmup.style.display = 'none';
    });
  }

  if (formBulkWarmup) {
    formBulkWarmup.addEventListener('submit', async (e) => {
      e.preventDefault();
      const rawText = (bulkWarmupTextarea ? bulkWarmupTextarea.value : '').trim();
      if (!rawText) {
        if (bulkWarmupModalMsg) {
          bulkWarmupModalMsg.className = 'alert-box alert-error';
          bulkWarmupModalMsg.textContent = 'Please paste at least one account (email,password).';
          bulkWarmupModalMsg.style.display = 'block';
        }
        return;
      }

      const submitBtn = formBulkWarmup.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Importing...';
      }

      try {
        const res = await fetch('/api/warmup/accounts/bulk', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ raw_text: rawText })
        });
        const data = await res.json();
        if (data.success) {
          if (bulkWarmupModalMsg) {
            bulkWarmupModalMsg.className = 'alert-box alert-success';
            bulkWarmupModalMsg.innerHTML = `<strong>🎉 ${data.message}</strong><br>All accounts placed in <strong>Day 1 (Cold: 4–8 emails/day)</strong>.`;
            bulkWarmupModalMsg.style.display = 'block';
          }
          setTimeout(() => {
            if (modalBulkWarmup) modalBulkWarmup.style.display = 'none';
            loadWarmupData();
          }, 1400);
        } else {
          if (bulkWarmupModalMsg) {
            bulkWarmupModalMsg.className = 'alert-box alert-error';
            bulkWarmupModalMsg.textContent = data.message || 'Import failed.';
            bulkWarmupModalMsg.style.display = 'block';
          }
        }
      } catch (err) {
        if (bulkWarmupModalMsg) {
          bulkWarmupModalMsg.className = 'alert-box alert-error';
          bulkWarmupModalMsg.textContent = 'Network error: ' + err.message;
          bulkWarmupModalMsg.style.display = 'block';
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<i class="fa-solid fa-upload"></i> Import Accounts';
        }
      }
    });
  }

  // Close modals on overlay backdrop click
  window.addEventListener('click', (e) => {
    if (e.target === modalAddWarmup) modalAddWarmup.style.display = 'none';
    if (e.target === modalBulkWarmup) modalBulkWarmup.style.display = 'none';
  });

  // ==================== INITIALIZATION ====================
  loadFiles();
  loadTemplates();
  loadSettings();
  loadSenderAccounts();
  loadWarmupData();
  fetchStats();
  fetchLogs();

  setInterval(() => {
    if (isPolling) {
      fetchStats();
      fetchLogs();
      // Periodically refresh warmup stats & stream
      const warmupTab = document.getElementById('tab-warmup');
      if (isWarmupEngineActive || (warmupTab && warmupTab.classList.contains('active'))) {
        loadWarmupData();
      }
    }
  }, 1800);
});

