import argparse
import time
import os
import numpy as np
import pandas as pd
from datetime import datetime


from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter
import ipdb

def main():
    
    # PARAMETERS
    wait_time = 2
    count_time = 3
    fingers = ["THUMB", "POINTER", "MIDDLE", "RING", "PINKY", "HAND"]
    # motion = ["CURL", "SLOW FOLD", "FAST FOLD"] 
    # motion = ["FOLD", "RELEASE"] 
    """
    Motion definitions:
    CURL: roll finger into a ball by bending ALL joints on the finger.
        e.g. bending HAND = making a fist
    FOLD: keep finger straight, bending only the largest joint of the finger
        until perpendicular with palm.
    """

    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    """
    Tip: use terminal command `ls /dev` to list all available ports. 
    On Macs, Ganglion Bluetooth Dongle is `cu.usbmodem11` or `tty.usbmodem11`. The `cu` one worked for Phil.
    """
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    params.timeout = 15

    board = BoardShim(BoardIds.GANGLION_BOARD, params)
    board.prepare_session()
    board.start_stream()
    print("STARTING STREAM")

    for j in range(len(fingers)): # loop over fingers
        for k in range(2): # how many times per action
            print(fingers[j] + ":")
            for i in range(count_time)[::-1]:
                print(i+1) 
                if i == 0: # to insert marker just before the motion is peformed
                    time.sleep(0.9)
                    # come up with a more comprehensive marker system, suitable for different combinations of fingers and motions
                    board.insert_marker((j+1)*4)
                    print("action marker")
                    time.sleep(0.1)
                else:
                    time.sleep(1)
            print("[ACTION]" + "\n") 
            time.sleep(0.9)
            board.insert_marker((j+1)*3-1)
            print("return marker")
            time.sleep(0.1)
            print("[RETURN]")
            time.sleep(wait_time)


    
    data = board.get_board_data()


    df = pd.DataFrame(data=data.T, columns=['Packet', 'Ch. 1', 'Ch. 2', 'Ch. 3', 'Ch. 4', '?1', '?2', '?3', '?4', '?5', '?6', '?7', '?8', 'Time', 'Marker'])


    # write data to file
    outdir = "./data/"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    fn = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    df.to_csv(outdir + fn + ".csv")
    # DataFilter.write_file(data, fn + "_raw.csv", 'w')  # use 'a' for append mode
    print("Saved Data!")
    
    try:
        board.stop_stream()
        board.release_session()
    except:
        print("Stream Session didn't stop or release properly. Activating the debugger.")
        ipdb.set_trace()

if __name__ == "__main__":
    main()