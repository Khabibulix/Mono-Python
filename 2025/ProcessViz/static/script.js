
function send_data(pid) {
    window.location.href = `/process/${pid}`;
}

async function fetchProcesses() {
    const container = document.getElementById("process-list");
    const template = document.getElementById("process-template");
    const scrollPos = window.scrollY;

    try {
        const res = await fetch("/api/processes");
        const data = await res.json();

        if (data.status !== "ok") {
            container.innerHTML = "<p>Chargement en cours...</p>";
            return;
        }

        const existingPIDs = new Set(
            Array.from(container.querySelectorAll("table")).map(
                table => table.dataset.pid
            )
        );
        
        const fragment = document.createDocumentFragment();

        for (const [name, v] of Object.entries(data.data)) {
            let table = container.querySelector(`table[data-pid="${v.PID}"]`);

            if (!table) {
                // Clone template only if not created
                const clone = template.content.cloneNode(true);
                table = clone.querySelector("table");
                table.dataset.pid = v.PID;
                fragment.appendChild(clone);
            }
            
            table.querySelector("caption").textContent = name;

            const tbody = table.querySelector("tbody");
            tbody.innerHTML = Object.entries(v).map(
                ([key, val]) => `<tr><th>${key}</th><td>${val}</td></tr>`
            ).join("");

            existingPIDs.delete(String(v.PID));
        }

        // Removing obsolete tables
        existingPIDs.forEach(pid => {
            const obsoleteTable = container.querySelector(`table[data-pid="${pid}"]`);
            if (obsoleteTable) obsoleteTable.remove();
        });

        if (fragment.childNodes.length > 0) {
            container.appendChild(fragment);
        }


    } catch (e) {
        console.error("Fetch error:", e);
        container.innerHTML = "<p>Error while loading</p>";
    } finally {
        window.scrollTo(0, scrollPos);
        setTimeout(fetchProcesses, 10000);
    }
}

// Event listener on all buttons
document.getElementById("process-list").addEventListener("click", (event) => {
    if (event.target.tagName === 'BUTTON') {
        const table = event.target.closest("table");
        if (table && table.dataset.pid) {
            send_data(table.dataset.pid);
        }
    }
})

fetchProcesses();
