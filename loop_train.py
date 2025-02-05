import argparse
import time
import os
import numpy as np
import pandas as pd
from datetime import datetime


from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets
from brainflow.data_filter import DataFilter

def countdown(sec):
    "Delay by SEC and display countdown by second."
    for s in range(sec)[::-1]:
        print(s+1)
        time.sleep(1)

def collect_and_average(board, duration, preptime=3, channel=4, message="Calibrating. Please be ready in:"):
    """ Used for calibration. Single Channel Averager over a period of time."""
    print(message)
    countdown(3)
    print("COLLECTING:")
    countdown(8)

    sample_size = duration * 200 # Ganglion 200 Hz sample rate
    data = board.get_current_board_data(sample_size)
    channel_data = data[channel]
    average = np.array(channel_data).mean()
    
    print(average)

    return average



if __name__ == "__main__":
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
    try:
        """
        skeleton code below
        save predictions:
            predictions = np.empty(0)
        """
        predictions = np.empty(0)
        """
        # CALIBRATE:
        # - print(Rest your arm. Calculating resting threshold in 3, 2, 1... Measuring resting state") -> take average to set resting threshold (8s)
        # - print(Grasp motion in 3, 2, 1.... Calculating grasping threshold...) -> take avg over 8 second
        # threshold = mid point between two averages
        """

        resting_avg = collect_and_average(board, 8, preptime=3, channel=4, message="RESTING CALIBRATION: Put your arm at rest in:")
        grasp_avg = collect_and_average(board, 8, preptime=3, channel=4, message="GRASPING CALIBRATION: START GRASPING in:")
        
        alpha = 0.9
        threshold = resting_avg + (grasp_avg - resting_avg) * alpha # add alpha

        """
        CLASSIFICATION:
        loop forever:
            Get latest 26 datapoints
            sample_size = 26 # because humans' perception of real time is 13ms, and sample rate is 200Hz
            -> new_data = get_current_board_data() # get latest collected data, can return less than “num_samples”, doesnt flush it from ringbuffer
            get the correct channel
            Take average and compare to threshold
            pred = avg > threshold
            if pred:
                print('GRASP DETECTED')
                np.append(predictions, np.ones(26))
            else:
                print('-')
                np.append(predictions, np.zeros(26))



            if press 'q' -> break loop and save all data from streaming sesh

        """
        # list of epoch testing accuracies
        import pywt
        while True:
            ######################
            #      TRAINING      #
            ######################
            sample_size = 500 # might need to increase this
            new_data = board.get_current_board_data(sample_size)
            channel_data = np.array(new_data[4]) # make copies depending on how many channels we use

            # wavelet transform (chunking, preprocessing, and more)
                # num coefficients should equal to sample_size

            # windowing? (overlap and save FFT method?)

            # pass into model -> train
                # if first time, initialize model
                # else, deserialize model
            # data = data_loader
            # model = RNN()
            # train_loop()
            # serialize model / save checkpoint
            serialize(model)

            ######################
            #      TESTING       #
            ######################

            # list of motions
            # empty list of predictions
            # for motion in motions:
                # collect chunk   or do this by calculating sample size needed
                
                # same wavelet preprocessing

                # model.predict
            n_trials = 20
            chan_mask = [3, 4, 5, 6]
            finger = "MIDDLE"
            sample_size = 500 # 2.5 seconds
            sampling_period = 1 # seconds
            comp_delays = []
            sleep_delays = []
            for n in range(n_trials):
                # coin flip
                control = True
                if control:
                    print("flex something else in:")
                    label = 0
                    
                else: 
                    print("FLEX " + finger)
                    label = 1
                start_time = time.time()

                # keep test data size constant 
                test_data = board.get_current_board_data(sample_size) # removes from ringbuffer
                # get specified channels 
                test_data = np.array(test_data[chan_mask]) 
                
                # shape -> (chn * sample_size / 2) 
                coef_ca, coef_cd = pywt.dwt(test_data, "db1", mode="per", axis=-1) 
                
                assert coef_ca.shape == coef_cd.shape
                assert coef_ca.shape[0] == len(chan_mask) 
                
                # classifier
                # res -> (chn)
                i = np.random.rand(coef_ca.shape[1])
                res = np.dot(coef_ca, i)

                end_time = time.time()
                # computation latency
                # store latecy
                # compute average
                comp_delay = end_time - start_time
                print(f"Execusion time: {comp_delay}")

                # threshold and report
                print(res > threshold)

                # sampling latency
                print(f"Delay for: {sampling_period}")
                sleep_start = time.time()
                time.sleep(sampling_period)
                sleep_end = time.time()
                sleep_delay = sleep_end - sleep_start
                sleep_delays.append(sleep_delay)
                comp_delays.append(comp_delay)
            
            # compute_accuracy()


    
        
    except KeyboardInterrupt:
        print('\nEnded')
        print('Saving Data...')
        data = board.get_board_data() 
        df = pd.DataFrame(data=data.T, columns=['Packet', 'Ch. 1', 'Ch. 2', 'Ch. 3', 'Ch. 4', '?1', '?2', '?3', '?4', '?5', '?6', '?7', '?8', 'Time', 'Marker'])
        df['pred'] = predictions

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