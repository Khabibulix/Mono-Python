
function send_data(pid) {
    window.location.href = `/process/${pid}`;
}

async function fetchProcesses() {
    const container = document.getElementById("process-list");
    const template = document.getElementById("process-template");
    const scrollPos = window.scrollY;

    container.innerHTML = "";


    try {
        const res = await fetch("/api/processes");
        const data = await res.json();

        if (data.status !== "ok") {
            container.innerHTML = "<p>Chargement en cours...</p>";
            return;
        }
        
        for (const [name, v] of Object.entries(data.data)) {
            const clone = template.content.cloneNode(true);
            
            clone.querySelector("caption").textContent = name;

            const tbody = clone.querySelector("tbody");
            tbody.innerHTML = Object.entries(v).map(([key, val]) => (
                `<tr><th>${key}</th><td>${val}</td></tr>`
            )).join("");

            clone.querySelector("button").onclick = () => send_data(v.PID);

            container.appendChild(clone);
        }

    } catch (e) {
        console.error("Fetch error:", e);
        container.innerHTML = "<p>Error while loading</p>";
    } finally {
        window.scrollTo(0, scrollPos);
        setTimeout(fetchProcesses, 10000);
    }
}

fetchProcesses();
