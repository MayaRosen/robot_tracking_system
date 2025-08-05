import time
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient

def take_picture(filename="go2_photo.jpg"):
    # Create and initialize the video client
    client = VideoClient()
    client.SetTimeout(3.0)
    client.Init()

    # Capture one image frame
    print("Capturing image from Go2 camera...")
    code, data = client.GetImageSample()

    # Handle result
    if code != 0:
        print("Error capturing image. Code:", code)
        return False
    else:
        with open(filename, "wb") as f:
            f.write(bytes(data))
        print(f"Image saved as {filename}")
        return True

if __name__ == "__main__":
    take_picture()
