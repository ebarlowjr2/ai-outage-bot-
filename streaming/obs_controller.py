import os
from obswebsocket import obsws, requests, exceptions
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("OBS_WS_HOST", "localhost")
port = int(os.getenv("OBS_WS_PORT", 4455))
password = os.getenv("OBS_WS_PASSWORD")

def switch_scene(scene_name):
    try:
        ws = obsws(host, port, password)
        ws.connect()
        print("✅ Connected to OBS WebSocket")
        scenes = ws.call(requests.GetSceneList())
        scene_names = [scene['sceneName'] for scene in scenes.getScenes()]
        print("Available scenes:", scene_names)
        
        if scene_name not in scene_names:
            print(f"❌ Scene '{scene_name}' not found!")
        else:
            ws.call(requests.SetCurrentProgramScene(scene_name))
            print(f"✅ Switched to scene: {scene_name}")
        ws.disconnect()
    except exceptions.OBSWebSocketError as e:
        print(f"OBS WebSocket error: {e}")
    except Exception as e:
        print(f"General error: {e}")

if __name__ == "__main__":
    switch_scene("Outage Live")
