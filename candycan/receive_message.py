# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/vcantest/receive_messasge.ipynb.

# %% auto 0
__all__ = ['get_argparser', 'receive_msg', 'receive_message']

# %% ../nbs/vcantest/receive_messasge.ipynb 4
import os
import signal
import time
import sys
import io
from multiprocessing import Event
from multiprocessing import synchronize, Manager
from multiprocessing.managers import DictProxy
from typing import Optional
from datetime import datetime
import json
import argparse

# %% ../nbs/vcantest/receive_messasge.ipynb 5
import can
# from can.interface import Bus
# from can import Message 
import cantools
from cantools.database import Message as MessageTpl
from cantools.database.can.database import Database

# %% ../nbs/vcantest/receive_messasge.ipynb 6
def get_argparser() -> argparse.ArgumentParser:
    """_summary_ get CAN bus, dbc config and the message to send

    Returns:
        argparse.ArgumentParser: _description_
    """

    parser = argparse.ArgumentParser("Get the CAN Bus channel, bitrate and dbc path")

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default="socketcan",
        help="The type of the CAN bus",
    )

    parser.add_argument(
        "-c",
        "--channel",
        type=str,
        default="vcan1",
        help="The CAN bus channel to connect to",
    )

    parser.add_argument(
        "-b", "--bitrate", type=int, default=250000, help="The bitrate of the CAN bus"
    )

    parser.add_argument(
        "-d",
        "--dbc",
        type=str,
        default="../res/motohawk_new.dbc",
        help="The path to the dbc file",
    )

    parser.add_argument(
        "-m",
        "--message",
        type=str,
        default="ExampleMessage",
        help="The message to send",
    )

    parser.add_argument(
        "-e",
        "--extended",
        action="store_true",
        help="If the arbitration id is extended",
    )

    return parser


# %% ../nbs/vcantest/receive_messasge.ipynb 13
def receive_msg(db:Database, message:str, channel:str, bitrate:int, bus_type: str) -> dict:

    print('Receiving message')
    with can.interface.Bus(bustype=bus_type, channel=channel, bitrate=bitrate) as bus:
        msg:Message = bus.recv()
    print('Received message')

    return {'timestamp': datetime.fromtimestamp(msg.timestamp),
            'payload': db.decode_message(msg.arbitration_id,msg.data)
            }


# %% ../nbs/vcantest/receive_messasge.ipynb 16
def receive_message(message_proxy: DictProxy,bus: can.interface.Bus)->None:
	print('waiting for message')
	msg:Message = bus.recv()
	print('message received')
	message_proxy['timestamp'] = msg.timestamp
	message_proxy['arbitration_id'] = msg.arbitration_id
	message_proxy['data']=msg.data

# %% ../nbs/vcantest/receive_messasge.ipynb 24
if __name__ == "__main__" and "__file__" in globals():   # in order to be compatible for both script and notebnook

    # print(os.getcwd())
    p = get_argparser()
    args = p.parse_args()

    try:
        db: Database = cantools.database.load_file(args.dbc)
    except FileNotFoundError as e:
        print(f"File not found: {e}")


    
    msg = receive_msg(db=db,
                    message=args.message,
                    channel=args.channel,
                    bitrate=args.bitrate,
                    bus_type=args.type
                    )
    print(msg)
    # sys.stdout.flush()

