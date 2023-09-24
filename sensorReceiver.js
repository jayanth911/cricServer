let websocket;

function connect() {
    websocket = new WebSocket('ws://192.168.29.193:8765');
    websocket.onopen = function () {
        console.log('Connected to the server.');
    };
    websocket.onmessage = function (event) {
        console.log('Received:', event.data);
        updateTable(event.data);
    };
    websocket.onclose = function () {
        console.log('Disconnected from the server.');
    };
    websocket.onerror = function (error) {
        console.error('Error:', error);
    };
}

function updateTable(data) {
    const parts = data.split(': ');
    const type = parts[0];
    const values = parts[1].split(', ');

    if (type === "Accelerometer") {
        document.getElementById('ax').innerText = "x=" + values[0].split('=')[1];
        document.getElementById('ay').innerText = "y=" + values[1].split('=')[1];
        document.getElementById('az').innerText = "z=" + values[2].split('=')[1];
    } else if (type === "Gyroscope") {
        document.getElementById('gx').innerText = "x=" + values[0].split('=')[1];
        document.getElementById('gy').innerText = "y=" + values[1].split('=')[1];
        document.getElementById('gz').innerText = "z=" + values[2].split('=')[1];
    }
}

connect();