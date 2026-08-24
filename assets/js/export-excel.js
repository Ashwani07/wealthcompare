function exportWorkbook(filename, sheets) {
    if (typeof XLSX === "undefined") {
        window.alert("Excel export is unavailable right now. Please try again.");
        return;
    }

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
}