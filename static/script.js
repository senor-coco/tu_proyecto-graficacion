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
            line: { color: 'blue', width: 3 }, // Línea más gruesa para mayor visibilidad
            marker: { size: 6, color: 'red' }, // Marcadores más grandes
            type: 'scatter3d'
        });
    });

    const layout = {
        width: 900,  // Ajuste de tamaño del gráfico
        height: 650,
        scene: {
            xaxis: { range: [-99, 99], title: "X" },
            yaxis: { range: [-99, 99], title: "Y" },
            zaxis: { range: [-99, 99], title: "Z" },
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

    if (xa < -99 || xa > 99 || ya < -99 || ya > 99 || xb < -99 || xb > 99 || yb < -99 || yb > 99) {
        alert('Los valores deben estar entre -99 y 99');
        return;
    }

    let pendiente = xb - xa === 0 ? "Indefinida" : ((yb - ya) / (xb - xa)).toFixed(4);

    const response = await fetch('/add_line', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ xa, ya, xb, yb, pendiente })
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

// Función para limpiar los valores ingresados en Xa, Ya, Xb, Yb
function clearInputs() {
    document.getElementById('xa').value = "";
    document.getElementById('ya').value = "";
    document.getElementById('xb').value = "";
    document.getElementById('yb').value = "";
}

// Elimina todos los datos almacenados en el historial y borra el gráfico
async function clearData() {
    await fetch('/clear_data', { method: 'POST' });
    fetchData();
}

// Cargar los datos al inicio
fetchData();
