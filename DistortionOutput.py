#
# Sends OSC command to Non-Mixer
# Unmutes DistortionOutput, mutes CleanOutput
#

import argparse
import random
import time

from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=7587,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  client.send_message("/strip/DistortionOutput/Gain/Mute", 0.0)
  client.send_message("/strip/CleanOutput/Gain/Mute", 1.0)

