import argparse
import time
import numpy as np
from datetime import datetime

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter


def main():
    
    # PARAMETERS
    wait_time = 3
    count_time = 3
    fingers = ["THUMB", "POINTER", "MIDDLE", "RING", "PINKY", "FULL"]
    movement = ["CURL", "SLOW FOLD", "FAST FOLD"]

    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.serial_port = args.serial_port

    for j in range(len(fingers)):
        time.sleep(wait_time)
        for i in range(count_time)[::-1]:
            print(fingers[j], "IN" , i+1) 
            time.sleep(1)
        print(fingers[j]) 
        board.insert_marker(j+1)

    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    # write data to file
    fn = now.strftime("%m_%d_%Y") + ".csv"
    DataFilter.write_file(data, fn, 'w')  # use 'a' for append mode

if __name__ == "__main__":
    main()