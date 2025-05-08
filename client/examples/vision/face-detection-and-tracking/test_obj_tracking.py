# -*- encoding: UTF-8 -*-
"""
Face Tracking Control (Python 3 Version)
Enables/disables NAO's face tracking feature through ALFaceDetection.
Requires proper PYTHONPATH configuration to NAOqi SDK.
"""

import os
import sys

# Locate config file
sys.path.insert(0, os.getcwd())
from config import *
from naoqi3 import ALProxy  # Using Python 3 compatible proxy


USAGE = """USAGE:
python vision_setfacetracking.py [NAO_IP] [0 or 1]

Examples:
Enable tracking: set_tracking.py 192.168.1.102 1
Disable tracking: set_tracking.py 192.168.1.102 0
"""

def set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled):
    """Control NAO's face tracking feature.
    
    Args:
        nao_ip (str): Robot IP address
        nao_port (int): Robot port
        tracking_enabled (bool): True to enable tracking, False to disable
    """
    try:
        face_proxy = ALProxy("ALFaceDetection", nao_ip, nao_port)
        print(f"Setting face tracking to {'enabled' if tracking_enabled else 'disabled'}...")
        
        # Enable/disable tracking
        face_proxy.enableTracking(tracking_enabled)
        
        # Verify current status
        status = face_proxy.isTrackingEnabled()
        print(f"Tracking is now {'enabled' if status else 'disabled'} on the robot")
        
    except Exception as e:
        print(f"Error controlling face tracking: {str(e)}")
        sys.exit(1)

def main():
    """Main execution with default tracking disabled"""
    tracking_enabled = True  # Default to disabled
    set_nao_face_detection_tracking(IP, PORT, tracking_enabled)

if __name__ == "__main__":
    main()