from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dynamic Table with Editable Cells, Axis Labels, and Save Feature</title>
    <style>
        table, td {
            border: 1px solid black;
        }
        td, .axis-label {
            width: 50px;
            height: 50px;
            text-align: center;
            vertical-align: middle;
        }
        .axis-label {
            font-weight: bold;
        }
        .y-axis-label {
            writing-mode: vertical-rl;
            transform: rotate(180deg);
            white-space: nowrap;
        }
        #x-axis-labels div, #y-axis-labels div {
            display: inline-block;
            width: 50px;
            text-align: center;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.3.2/html2canvas.min.js"></script>
</head>
<body>
    <h2>TableSetter DynamicTableMaker</h2>
    <label for="rows">Rows (Y-axis):</label>
    <input type="number" id="rows" value="5">
    <label for="cols">Columns (X-axis):</label>
    <input type="number" id="cols" value="5">
    <br>
    <label for="x-axis">X-axis Label:</label>
    <input type="text" id="x-axis" value="X-Label">
    <input type="checkbox" id="x-axis-toggle" onchange="toggleXAxisInput()"> Toggle comma-separated values
    <br>
    <label for="y-axis">Y-axis Label:</label>
    <input type="text" id="y-axis" value="Y-Label">
    <input type="checkbox" id="y-axis-toggle" onchange="toggleYAxisInput()"> Toggle comma-separated values
    <br>
    <label for="color">Cell Color:</label>
    <input type="color" id="color" value="#FFFFFF">
    <button onclick="generateTable()">Generate Table</button>
    <button onclick="saveTableAsImage()">Save Table as Image</button>

    <div style="display: flex;">
        <div id="y-axis-labels" style="flex-direction: column;"></div>
        <div>
            <div id="x-axis-labels"></div>
            <div id="tableContainer"></div>
        </div>
    </div>

    <script>
        function generateTable() {
            var rows = parseInt(document.getElementById('rows').value);
            var cols = parseInt(document.getElementById('cols').value);
            var xAxisValue = document.getElementById('x-axis').value;
            var yAxisValue = document.getElementById('y-axis').value;
            var xAxisToggle = document.getElementById('x-axis-toggle').checked;
            var yAxisToggle = document.getElementById('y-axis-toggle').checked;
            var table = '<table>';
            var xAxisLabels = '<div class="axis-label">&nbsp;</div>'; // Offset for y-axis labels
            var yAxisLabels = '';

            for (var i = 0; i < cols; i++) {
                var xLabel = xAxisToggle ? (xAxisValue.split(',')[i] || '') : (i === 0 ? xAxisValue : '');
                xAxisLabels += '<div class="axis-label">' + xLabel + '</div>';
            }

            for (var i = 0; i < rows; i++) {
                var yLabel = yAxisToggle ? (yAxisValue.split(',')[i] || '') : (i === 0 ? yAxisValue : '');
                yAxisLabels += '<div class="axis-label y-axis-label">' + yLabel + '</div>';
                table += '<tr>';
                for (var j = 0; j < cols; j++) {
                    table += '<td contenteditable="true" onclick="changeColor(this)"></td>';
                }
                table += '</tr>';
            }
            table += '</table>';

            document.getElementById('tableContainer').innerHTML = table;
            document.getElementById('x-axis-labels').innerHTML = xAxisLabels;
            document.getElementById('y-axis-labels').innerHTML = yAxisLabels;
        }

        function changeColor(cell) {
            var color = document.getElementById('color').value;
            cell.style.backgroundColor = color;
        }

        function toggleXAxisInput() {
            var toggle = document.getElementById('x-axis-toggle').checked;
            document.getElementById('x-axis').value = toggle ? '1,2,3,4,5' : 'X-Label';
        }

        function toggleYAxisInput() {
            var toggle = document.getElementById('y-axis-toggle').checked;
            document.getElementById('y-axis').value = toggle ? 'A,B,C,D,E' : 'Y-Label';
        }

        function saveTableAsImage() {
            html2canvas(document.querySelector("#tableContainer")).then(canvas => {
                // Create an "a" element to trigger download
                var link = document.createElement('a');
                link.download = 'table.png';
                link.href = canvas.toDataURL();
                link.click();
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
