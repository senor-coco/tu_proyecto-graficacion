async function fetchData() {
    const response = await fetch('/get_data');
    const data = await response.json();
    renderPlot(data);
    updateTable(data);
}

function renderPlot(data) {
    const traces = [];

    data.lines.forEach(line => {
        traces.push({
            x: line.x_values,
            y: line.y_values,
            z: Array(line.x_values.length).fill(0),
            mode: 'lines+markers',
            line: { color: 'blue', width: 2 },
            marker: { size: 4, color: 'red' },
            type: 'scatter3d'
        });
    });

    const layout = {
        scene: {
            xaxis: { range: [-999, 999], title: "X" },
            yaxis: { range: [-999, 999], title: "Y" },
            zaxis: { range: [-10, 10], title: "Z" }, 
        }
    };

    Plotly.newPlot('plot', traces, layout);
}

async function addLine() {
    const xa = parseFloat(document.getElementById('xa').value);
    const ya = parseFloat(document.getElementById('ya').value);
    const xb = parseFloat(document.getElementById('xb').value);
    const yb = parseFloat(document.getElementById('yb').value);

    if (isNaN(xa) || isNaN(ya) || isNaN(xb) || isNaN(yb)) {
        alert('Por favor, ingresa valores numéricos válidos');
        return;
    }

    if (xa < -999 || xa > 999 || ya < -999 || ya > 999 || xb < -999 || xb > 999 || yb < -999 || yb > 999) {
        alert('Los valores deben estar entre -999 y 999');
        return;
    }

    const response = await fetch('/add_line', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ xa, ya, xb, yb })
    });

    const updatedData = await response.json();
    renderPlot(updatedData);
    updateTable(updatedData);
}

function updateTable(data) {
    const tableBody = document.getElementById('coordTableBody');
    tableBody.innerHTML = ''; 

    data.lines.forEach(line => {
        line.x_values.forEach((x, i) => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${x.toFixed(2)}</td>
                             <td>${line.y_values[i].toFixed(2)}</td>
                             <td>${line.pendiente === "Indefinida" ? "Indefinida" : line.pendiente}</td>`;
            tableBody.appendChild(row);
        });
    });
}

async function clearData() {
    await fetch('/clear_data', { method: 'POST' });
    fetchData();
}

fetchData();
