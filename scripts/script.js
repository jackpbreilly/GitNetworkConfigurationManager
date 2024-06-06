const apiUrl = 'http://127.0.0.1:5000';

async function listFiles() {
    const response = await fetch(`${apiUrl}/files`);
    const files = await response.json();
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    files.forEach(file => {
        const li = document.createElement('li');
        li.textContent = file;
        li.onclick = () => getFile(file);
        fileList.appendChild(li);
    });
}

async function getFile(fileName) {
    const response = await fetch(`${apiUrl}/files/${fileName}`);
    const data = await response.json();
    document.getElementById('fileName').value = fileName;
    document.getElementById('fileContent').value = data.content;
}

async function createFile() {
    const fileName = document.getElementById('fileName').value;
    const content = document.getElementById('fileContent').value;
    await fetch(`${apiUrl}/files`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ file_name: fileName, content })
    });
    listFiles();
}

async function updateFile() {
    const fileName = document.getElementById('fileName').value;
    const content = document.getElementById('fileContent').value;
    await fetch(`${apiUrl}/files/${fileName}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content })
    });
    listFiles();
}

async function deleteFile() {
    const fileName = document.getElementById('fileName').value;
    await fetch(`${apiUrl}/files/${fileName}`, {
        method: 'DELETE'
    });
    listFiles();
}

async function cloneRepo() {
    const repoUrl = document.getElementById('repoUrl').value;
    await fetch(`${apiUrl}/git/clone`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ repo_url: repoUrl })
    });
    listFiles();
}

async function commitChanges() {
    const message = prompt('Enter commit message:');
    await fetch(`${apiUrl}/git/commit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    });
}

async function pushChanges() {
    await fetch(`${apiUrl}/git/push`, {
        method: 'POST'
    });
}