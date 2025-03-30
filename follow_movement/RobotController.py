import time
import signal
import sys
from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from unitree_sdk2py.idl.unitree_go.msg.dds_ import UwbState_

from uwb_state_manager import UwbStateManager
from robot_motion_executor import RobotMotionExecutor

class RobotController:
    def __init__(self):
        self.state_manager = UwbStateManager()
        self.robot = None

    def signal_handler(self, signum, frame):
        print("Interrupt signal received.")
        if self.robot:
            self.robot.cleanup()
        sys.exit(0)

    def run(self):
        ChannelFactoryInitialize(0)
        uwb_sub = ChannelSubscriber("rt/uwbstate", UwbState_)
        uwb_sub.Init(self.state_manager.update_state, 10)
        time.sleep(1)

        self.robot = RobotMotionExecutor(self.state_manager)
        signal.signal(signal.SIGINT, self.signal_handler)
        self.robot.move_based_on_remote(duration=90.0)
