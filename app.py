from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go

app = Flask(__name__)

# Lista global para almacenar los puntos y líneas
data = {"points": [], "lines": []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_point', methods=['POST'])
def add_point():
    global data
    point = request.json  # Recibe JSON con x, y, z
    data["points"].append(point)
    return jsonify(data)

@app.route('/add_line', methods=['POST'])
def add_line():
    global data
    line = request.json  # Recibe JSON con dos puntos (inicio y fin)
    data["lines"].append(line)
    return jsonify(data)

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/clear_data', methods=['POST'])
def clear_data():
    global data
    data = {"points": [], "lines": []}  # Reiniciar datos
    return jsonify({"message": "Datos limpiados"})

def create_plot():
    fig = go.Figure()
    for point in data["points"]:
        fig.add_trace(go.Scatter3d(x=[point["x"]], y=[point["y"]], z=[point["z"]],
                                   mode='markers', marker=dict(size=5, color='red')))
    for line in data["lines"]:
        fig.add_trace(go.Scatter3d(x=[line["start"]["x"], line["end"]["x"]],
                                   y=[line["start"]["y"], line["end"]["y"]],
                                   z=[line["start"]["z"], line["end"]["z"]],
                                   mode='lines', line=dict(color='blue', width=2)))
    return fig.to_html(full_html=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
