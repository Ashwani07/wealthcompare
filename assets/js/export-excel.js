let xlsxLoadingPromise = null;

function loadXLSX() {
    if (typeof XLSX !== "undefined") {
        return Promise.resolve();
    }
    if (xlsxLoadingPromise) {
        return xlsxLoadingPromise;
    }
    xlsxLoadingPromise = new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js";
        script.async = true;
        script.onload = () => resolve();
        script.onerror = () => {
            xlsxLoadingPromise = null;
            reject(new Error("Failed to load XLSX library"));
        };
        document.head.appendChild(script);
    });
    return xlsxLoadingPromise;
}

function exportWorkbook(filename, sheets) {
    loadXLSX().then(() => {
        const workbook = XLSX.utils.book_new();
        Object.entries(sheets).forEach(([name, rows]) => {
            const worksheet = XLSX.utils.aoa_to_sheet(rows);
            const columnCount = rows.reduce((count, row) => Math.max(count, row.length), 0);
            worksheet["!cols"] = Array.from({ length: columnCount }, (_, columnIndex) => ({
                wch: Math.min(48, Math.max(14, ...rows.map(row => String(row[columnIndex] ?? "").length + 2)))
            }));
            worksheet["!freeze"] = { xSplit: 0, ySplit: 2 };
            XLSX.utils.book_append_sheet(workbook, worksheet, name.slice(0, 31));
        });
        XLSX.writeFile(workbook, filename);
    }).catch(err => {
        console.error("Export error:", err);
        window.alert("Excel export is unavailable right now. Please try again.");
    });
}
