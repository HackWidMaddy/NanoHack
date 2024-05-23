import network
import time
import usocket as socket
import machine
import ujson
import urandom
# Replace 'your_ssid' and 'your_password' with your WiFi credentials
WIFI_SSID = 'ab'
WIFI_PASSWORD = '12345678'

# Connect to the WiFi Access Point
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait until the connection is established
while not wifi.isconnected():
    pass

print('Connected to WiFi:', wifi.ifconfig())

# Set up the microwave sensor on D4 pin
microwave_sensor = machine.Pin(2, machine.Pin.IN)
servo = machine.PWM(machine.Pin(5), freq=50)
pin_d2 = machine.Pin(4, machine.Pin.OUT)  # D2 corresponds to GPIO4 on NodeMCU
servo.duty(20)

# Function to handle HTTP requests
def handle_request(client):
    request = client.recv(1024)
    if b"GET /get_sensor_value" in request:
        microwave_sensor_value = microwave_sensor.value()
        if microwave_sensor_value=="1" or microwave_sensor_value==1:
                microwave_sensor_value="INTRUSION DETECTED"
        else:
                microwave_sensor_value="INTRUSION NOT DETECTED"
        json_response = ujson.dumps({"sensor_value": microwave_sensor_value})
        client.send(json_response)
        client.close()
        return
    
    elif b"GET /drop" in request:
         servo.duty(130)
         time.sleep(2)
         servo.duty(20)
         client.close()
         return 
    elif b"GET /bomb" in request:
        pin_d2.on() 
        time.sleep(1) 
        pin_d2.off()  
        time.sleep(1) 
        pin_d2.on() 
        time.sleep(1) 
        pin_d2.off()  
        time.sleep(1) 
        pin_d2.on() 
        time.sleep(1) 
        pin_d2.off()  
        time.sleep(1)        
        return 

    html_response = """
HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<script>
function sendRequest() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_sensor_value", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var jsonResponse = JSON.parse(xhr.responseText);
            document.getElementById("msensor").innerHTML = jsonResponse.sensor_value;
        }
    };
    xhr.send();
}


function drop(argument) {
    const xhr = new XMLHttpRequest();
    if (argument === 1) {
        xhr.open("GET", "/bomb");
    } else {
        xhr.open("GET", "/drop");
    }
    xhr.send();
}


</script>
<title>ESP8266 Web Server</title>
</head>
<body>
<h1>NanoHack Sensor Network</h1>

Auto Destruct : <button onclick="drop(1)">Press me</button><br>
Microwave Sensor Output: <button onclick="sendRequest()">Check Sensor Value</button> <p id="msensor"></p>
Drop : <button onclick="drop()">DROP</button>



</body>
</html>

    """

    client.send(html_response)
    client.close()

# Set up the socket for the HTTP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(2)

try:
    while True:
        client, addr = server_socket.accept()
        handle_request(client)

except KeyboardInterrupt:
    print("KeyboardInterrupt: Stopping Web Server")
    server_socket.close()