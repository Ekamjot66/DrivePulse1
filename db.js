// HTML Escape helper used across all 6 pages
function esc(str) {
    return String(str ?? "").replace(/[&<>"']/g, m => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }[m]));
}

// Difficulty badge Tailwind classes used in index, debriefs, and companies
const DC = {
    Easy: "bg-slate-200 text-slate-800",
    Medium: "bg-slate-300 text-slate-900",
    Hard: "bg-slate-900 text-white"
};

// If opened via file:// or another port, point to FastAPI on port 8000
const API_BASE = location.port === "8000" ? "" : "http://127.0.0.1:8000";

const DB = {
    data: null,

    // Load initial data synchronously so inline scripts in the 6 HTML files work out-of-the-box
    load() {
        try {
            const xhr = new XMLHttpRequest();
            xhr.open("GET", `${API_BASE}/api/db`, false); // synchronous request
            xhr.send(null);
            if (xhr.status === 200) {
                this.data = JSON.parse(xhr.responseText);
                localStorage.setItem("drivepulse_backup", xhr.responseText);
                return;
            }
        } catch (err) {
            console.warn("FastAPI server unreachable, falling back to localStorage cache.", err);
        }

        // Fallback if server isn't running
        const cached = localStorage.getItem("drivepulse_backup");
        if (cached) {
            this.data = JSON.parse(cached);
        }
    },

    // Persist changes (new debriefs, upvotes, saves, pathway ticks) to db.json via FastAPI
    save() {
        localStorage.setItem("drivepulse_backup", JSON.stringify(this.data));
        fetch(`${API_BASE}/api/db`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.data)
        }).catch(err => console.error("Failed to save to FastAPI:", err));
    },

    // Reset db.json to initial state via FastAPI (used in profile.html)
    reset() {
        try {
            const xhr = new XMLHttpRequest();
            xhr.open("POST", `${API_BASE}/api/reset`, false);
            xhr.send(null);
            if (xhr.status === 200) {
                const res = JSON.parse(xhr.responseText);
                this.data = res.data;
                localStorage.setItem("drivepulse_backup", JSON.stringify(this.data));
            }
        } catch (err) {
            console.error("Failed to reset DB on FastAPI:", err);
        }
    },

    // Download current db.json file (used in profile.html)
    exportJSON() {
        const blob = new Blob([JSON.stringify(this.data, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "db.json";
        a.click();
        URL.revokeObjectURL(url);
    }
};

// Initialize immediately on script load
DB.load();