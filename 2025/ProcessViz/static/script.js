
function initWebSocket() {
    const socket = new WebSocket("ws://localhost:5000/ws");
    socket.onopen = handleOpen;
    socket.onmessage = handleMessage;
    socket.onerror = handleError;
    socket.onclose = handleClose;

    return socket;
}

function handleOpen() {
    console.log("WebSocket connected");
}

function handleMessage(event) {
    try {
        if (!event.data) return;
        const message = JSON.parse(event.data);

        if (message.status === "ok") {
            renderProcesses(message.data);
        } else {
            showLoadingMessage();
        }
    } catch (err) {
        console.error("Parsing error JSON", err);
    }
}

function handleError(err){
    console.error("WebSocket error", err);
}

function handleClose() {
    console.warn("Closed WebSocket, new attempt in 5s");
    setTimeout(initWebSocket, 5000);
}

function renderProcesses(processData) {
    const container = document.getElementById("process-list");
    const template = document.getElementById("process-template");
    const currentTables = Array.from(container.querySelectorAll("table"));
    const currentPIDs = new Set(currentTables.map(t => t.dataset.pid));

    //Build new tables
    for (const [name, proc] of Object.entries(processData)) {
        let table = container.querySelector(`table[data-pid="${proc.PID}"]`);

        if (!table){
            //Build new table if not existing
            const clone = template.content.cloneNode(true);
            table = clone.querySelector("table");
            table.dataset.pid = proc.PID;
            container.appendChild(clone);
        }
        
        fillTable(table, name, proc);
        currentPIDs.delete(String(proc.PID));
    }
    removeObsoleteProcesses(container, currentPIDs);

}

function fillTable(table, name, proc){
    const caption = table.querySelector("caption");
    const tbody = table.querySelector("tbody");
    
    caption.textContent = name;
    tbody.innerHTML = ""

    for (const [key,val] of Object.entries(proc)) {
        const row = document.createElement('tr');
        
        const th = document.createElement('th');
        th.textContent = key;

        const td = document.createElement('td');
        td.textContent = val;

        row.appendChild(th);
        row.appendChild(td);
        tbody.appendChild(row);
    }

}

function removeObsoleteProcesses(container, pidSet) {
    pidSet.forEach(pid => {
        const oldTable = container.querySelector(`table[data-pid="${pid}"]`);
        if (oldTable) oldTable.remove();
    });
}

function showLoadingMessage(){
    const container = document.getElementById("process-list");
    container.innerHTML = "<p>Loading...</p>";
}

function setupClickHandler() {
    const container = document.getElementById("process-list");
    container.addEventListener("click", event => {
        if (event.target.tagName === "BUTTON") {
            const card = event.target.closest(".process-card");
            if (card) {
                const table = card.querySelector("table");
                const pid = table.dataset.pid;
                navigateToProcess(pid);
            }
        }
    });
}

function navigateToProcess(pid){
    window.location.href = `/process/${pid}`;
}

function main(){
    setupClickHandler();
    initWebSocket();
}

main();