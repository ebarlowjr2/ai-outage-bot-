import os
import logging
from obswebsocket import obsws, requests, exceptions
from dotenv import load_dotenv

load_dotenv()

def switch_scene(scene_name):
    """Switch OBS scene using WebSocket connection"""
    try:
        host = os.getenv("OBS_WS_HOST", "localhost")
        port = int(os.getenv("OBS_WS_PORT", 4455))
        password = os.getenv("OBS_WS_PASSWORD")
        
        ws = obsws(host, port, password)
        ws.connect()
        logging.info("Connected to OBS WebSocket")
        
        scenes = ws.call(requests.GetSceneList())
        scene_names = [scene['sceneName'] for scene in scenes.getScenes()]
        logging.info(f"Available scenes: {scene_names}")
        
        if scene_name not in scene_names:
            logging.warning(f"Scene '{scene_name}' not found!")
            raise ValueError(f"Scene '{scene_name}' not found in available scenes: {scene_names}")
        else:
            ws.call(requests.SetCurrentProgramScene(scene_name))
            logging.info(f"Switched to scene: {scene_name}")
        
        ws.disconnect()
        
    except exceptions.OBSWebSocketError as e:
        logging.error(f"OBS WebSocket error: {e}")
        raise
    except Exception as e:
        logging.error(f"OBS connection error: {e}")
        raise

if __name__ == "__main__":
    switch_scene("Outage Live")
