from obswebsocket import obsws, requests

host = "localhost"
port = 4455  # OBS Websocket port
password = "your_password_here"

def switch_scene(scene_name):
    ws = obsws(host, port, password)
    ws.connect()
    ws.call(requests.SetCurrentProgramScene(scene_name))
    ws.disconnect()

# Usage example:
# switch_scene("Outage Live")
