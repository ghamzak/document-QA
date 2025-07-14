// Clear chat history
document.addEventListener('DOMContentLoaded', function() {
    const clearBtn = document.getElementById('clearChatBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            document.getElementById('chatHistory').innerHTML = '';
        });
    }
});
function showTab(tab) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
    document.querySelector(`.tab-btn[onclick*="${tab}"]`).classList.add('active');
}

let processId = null;
let docList = [];

document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('pdfFile');
    if (!fileInput.files.length) return;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    document.getElementById('progressContainer').style.display = 'block';
    document.getElementById('progressBar').value = 0;
    document.getElementById('progressPercent').innerText = '0';
    document.getElementById('uploadStatus').innerText = '';
    const res = await fetch('/api/upload', { method: 'POST', body: formData });
    const data = await res.json();
    if (data.process_id) {
        processId = data.process_id;
        pollProgress(processId);
        await fetchAndPopulateDocs();
    } else {
        document.getElementById('uploadStatus').innerText = data.error || 'Upload failed.';
        document.getElementById('progressContainer').style.display = 'none';
    }
});

async function fetchAndPopulateDocs() {
    const res = await fetch('/api/docs');
    docList = await res.json();
    const select = document.getElementById('docSelect');
    select.innerHTML = '';
    docList.forEach(doc => {
        const opt = document.createElement('option');
        opt.value = doc.process_id;
        opt.textContent = doc.filename;
        select.appendChild(opt);
    });
    // Set processId to selected
    if (docList.length > 0) {
        processId = select.value;
    }
}

document.addEventListener('DOMContentLoaded', fetchAndPopulateDocs);

document.getElementById('docSelect').addEventListener('change', function() {
    processId = this.value;
    // Clear chat history when switching documents
    document.getElementById('chatHistory').innerHTML = '';
});

async function pollProgress(pid) {
    let done = false;
    while (!done) {
        const res = await fetch(`/api/progress/${pid}`);
        const data = await res.json();
        document.getElementById('progressBar').value = data.progress;
        document.getElementById('progressPercent').innerText = data.progress;
        if (data.status === 'ready') {
            document.getElementById('uploadStatus').innerText = 'Ready to chat!';
            done = true;
        } else if (data.status === 'not_found') {
            document.getElementById('uploadStatus').innerText = 'Process not found.';
            done = true;
        }
        await new Promise(r => setTimeout(r, 1000));
    }
}

document.getElementById('chatForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const question = document.getElementById('question').value;
    const k = parseInt(document.getElementById('kChunks').value) || 3;
    if (!question || !processId) return;
    addMessage('user', question);
    const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, process_id: processId, k })
    });
    const data = await res.json();
    // Store latency for next addMessage call
    addMessage.lastLatency = {
        retrieval: data.retrieval_time,
        generation: data.generation_time,
        modelName: data.model_name
    };
    addMessage('bot', data.answer, data.citations, data.disclaimer);
    document.getElementById('question').value = '';
});

function addMessage(sender, text, citations = [], disclaimer = null) {
    const chatHistory = document.getElementById('chatHistory');
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'user' ? 'user-msg' : 'bot-msg';
    msgDiv.innerText = text;
    chatHistory.appendChild(msgDiv);
    // Always show latency after bot answer
    if (sender === 'bot' && addMessage.lastLatency) {
        const latencyDiv = document.createElement('div');
        latencyDiv.className = 'latency-info';
        latencyDiv.style.fontSize = '0.85em';
        latencyDiv.style.color = '#555';
        latencyDiv.style.margin = '0.3em 0 0.5em 0';
        latencyDiv.innerHTML = `<b>Retrieval time:</b> ${addMessage.lastLatency.retrieval.toFixed(2)}s &nbsp; <b>Generation time:</b> ${addMessage.lastLatency.generation.toFixed(2)}s`;
        chatHistory.appendChild(latencyDiv);
        if (addMessage.lastLatency.modelName) {
            const modelDiv = document.createElement('div');
            modelDiv.className = 'llm-model-info';
            modelDiv.style.fontSize = '0.85em';
            modelDiv.style.color = '#888';
            modelDiv.style.margin = '0 0 0.5em 0';
            modelDiv.innerHTML = `<b>LLM Model:</b> ${addMessage.lastLatency.modelName}`;
            chatHistory.appendChild(modelDiv);
        }
        addMessage.lastLatency = null;
    }
    // Citations removed as per user request
    if (disclaimer) {
        const disclaimerDiv = document.createElement('div');
        disclaimerDiv.className = 'disclaimer';
        disclaimerDiv.style.fontSize = '0.85em';
        disclaimerDiv.style.color = '#888';
        disclaimerDiv.style.marginTop = '0.5em';
        disclaimerDiv.innerText = disclaimer;
        chatHistory.appendChild(disclaimerDiv);
    }
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
