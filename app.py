from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go

app = Flask(__name__)

# Lista global para almacenar las líneas generadas
data = {"lines": []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_line', methods=['POST'])
def add_line():
    global data
    params = request.json  
    xa, ya, xb, yb = params["xa"], params["ya"], params["xb"], params["yb"]

    # Algoritmo DDA
    dx = xb - xa
    dy = yb - ya
    steps = max(abs(dx), abs(dy))
    x_inc = dx / steps
    y_inc = dy / steps

    x, y = xa, ya
    x_values, y_values = [], []

    for _ in range(int(steps) + 1):
        x_values.append(round(x))
        y_values.append(round(y))
        x += x_inc
        y += y_inc

    data["lines"].append({
        "xa": xa, "ya": ya, "xb": xb, "yb": yb, 
        "x_values": x_values, "y_values": y_values
    })
    
    return jsonify(data)

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/delete_line/<int:index>', methods=['POST'])
def delete_line(index):
    global data
    if 0 <= index < len(data["lines"]):
        del data["lines"][index]
    return jsonify(data)

@app.route('/clear_data', methods=['POST'])
def clear_data():
    global data
    data = {"lines": []}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
