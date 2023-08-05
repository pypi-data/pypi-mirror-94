import numpy as np
import re
from . import utils
from scipy.interpolate import interp1d
import copy
from . import trial
from . import session

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def read(filename, eyes_recorded = "auto", both_eyes_recorded = False, mode="d", start_msg=r"TRIAL \d{1,2} START",
         end_msg=r"TRIAL \d{1,2} END"):

    """
    Read method will read in the ascii file and extract the data
    "file_name" will take in the name of the file you are trying
    to extract data from

    mode: d or u
    d = "defualt"
    u = user defined

    "default" will use the default start and end times given in the file
    "user defined" will take in "start_msg" and "end_msg" to use as the

    eyes_recorded: Define which eye data to extract if both eyes are
                   being recorded
    "left", "right", "auto"
    default is "auto" which will take whichever eye it finds first

    both_eyes_recorded:
    True: if both eyes were recorded
    False: is only the left or right eyes was being recorded

    start and end marker
    "start_msg" will use regular expression to identify the user inputed

    message markers
    ex. r"TRIAL \d START"

    "end_msg" will use regular expression to identify the user inputed end
    message makers
    ex. r"TRIAL \d END"

    Returns Data Object
    """



    if not filename.endswith(".asc"):
        # raise ValueError("Extension must be .csv or .txt")
        pass


    mode = mode.lower()
    if not mode == "d" or not mode == "u":
        # raise ValueError("Mode must be 'd' for default or 'u' for user input")
        pass


    with open(filename) as f:
        start_time = ""
        end_time = ""
        flag = False
        events = []
        events_dict = {}
        timestamps_list = []
        messages_dict = {}
        trial_markers = {"start": [], "end": []}
        pupil_size_list = []
        movement_list = [[], []]
        rate_list = {}
        input_dict = {}
        button_dict = {}
        misc = []

        eyes_recorded = eyes_recorded.lower()

        # Default Mode
        if mode == "d":
            for num, line in enumerate(f, 1):
                elements = line.split()

                if line.startswith("START"):
                    start_time, trial_markers, end_time = find_start(elements, start_time, trial_markers, end_time)

                # to only get END messages
                # adds to trial_markers, messages_dict, timestamps_list
                if line.startswith("END"):
                    end_time, trial_markers, messages_dict, flag, start_time = find_end(elements, end_time, trial_markers, messages_dict, flag, start_time)

                if start_time:
                    if line.startswith(start_time):
                        flag = True
                if "RATE" in elements:
                    sample_rate = get_sample_rate(elements, both_eyes_recorded)

                # check for start
                if flag is True:
                    # will get pupil size, timestamps, and movements
                    if is_number(elements[0]):
                        timestamps_list, pupil_size_list, movement_list = tpm_read(timestamps_list, pupil_size_list, movement_list, elements, eyes_recorded, both_eyes_recorded)

                    # Gets all messages between START and END
                    elif elements[0] == "MSG":
                        messages_dict[int(elements[1])] = elements[2:]

                    # Gets Input triggers
                    elif elements[0] == "INPUT":
                        input_dict = input_read(input_dict, elements)

                    # Gets Button triggers
                    elif elements[0] == "BUTTON":
                        button_dict = button_read(button_dict, elements)

                    # Gets all events between START and END
                    elif not is_number(elements[1]):
                        events_dict = event_read(events_dict, elements, eyes_recorded, both_eyes_recorded)
                    else:
                        misc = misc_read(elements,misc)


        # User Defined Mode
        elif mode == "u":
            # initializes the regular expressions for start and end markers
            start_msg = re.compile(start_msg)
            end_msg = re.compile(end_msg)

            for num, line in enumerate(f, 1):
                elements = line.split()
                # finds start time using user defined marker
                if re.search(start_msg, line[2:]):
                    start_time, trial_markers, end_time = find_start(elements, start_time, trial_markers, end_time)
                    flag = True
                    continue

                # to only get END messages using user defined marker
                # adds to trial_markers, messages_dict, timestamps_list
                if re.search(end_msg, line[2:]):
                    #print(elements)
                    end_time, trial_markers, messages_dict, flag, start_time = find_end(elements, end_time, trial_markers, messages_dict, flag, start_time)
                    flag = False
                    continue

                if "RATE" in elements:
                    sample_rate = get_sample_rate(elements, both_eyes_recorded)

                # check for start marker
                if flag is True:
                    # will get pupil size, timestamps, and movements
                    if is_number(elements[0]):
                        timestamps_list, pupil_size_list, movement_list = tpm_read(timestamps_list, pupil_size_list, movement_list, elements, eyes_recorded, both_eyes_recorded)

                    # Gets messages between START and END markers
                    elif elements[0] == "MSG":
                        messages_dict[int(elements[1])] = elements[2:]

                    # Gets Input triggers
                    elif elements[0] == "INPUT":
                        input_dict = input_read(input_dict, elements)

                    # Gets Button triggers
                    elif elements[0] == "BUTTON":
                        input_dict = button_read(button_dict, elements)

                    # Gets all events between START and END markers
                    elif not is_number(elements[1]):
                        events_dict = event_read(events_dict, elements, eyes_recorded, both_eyes_recorded)

                    else:
                        misc = misc_read(elements,misc)

    # convert list to numpy array
    timestamps = np.array(timestamps_list)
    pupil_size = np.array(pupil_size_list)
    movement = np.array(movement_list)
    return Data(timestamps, pupil_size, movement, sample_rate, {}, messages_dict,
                events_dict, trial_markers, button_dict, input_dict, misc)



def find_start(elements, start_time, trial_markers, end_time):
    """
    Defines Start Times
    - used within read method to find start time of each trial
    - return start timestamp, updates boolean check for start and end
    """
    start_time = elements[1]
    trial_markers["start"].append(int(elements[1]))
    end_time = ""
    return start_time, trial_markers, end_time



def find_end(elements, end_time, trial_markers, messages_dict, flag, start_time):
    """
    Defines End Times
    - used within read method to find start time of each trial
    - return End timestamp, updates boolean check for start and end
    """
    end_time = elements[1]
    trial_markers["end"].append(int(elements[1]))
    messages_dict[int(elements[1])] = elements[2:]
    flag = False
    start_time = ""
    return end_time, trial_markers, messages_dict, flag, start_time


def get_sample_rate(elements, both):
    if both:
        return float(elements[6])
    else:
        return float(elements[4])


def tpm_read(timestamps_list, pupil_size_list, movement_list,
             elements, eyes_recorded, both_eyes_recorded):
    """
    Finds And Returns Timestamps, Pupil Size, and Movements From Each Trial
    """
    if both_eyes_recorded:
        if (eyes_recorded == "left"):
            if(elements[1] == "."):
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(np.nan)
                movement_list[0].append(np.nan)  # x-axis
                movement_list[1].append(np.nan)
            else:
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(float(elements[3]))
                movement_list[0].append(float(elements[1]))  # x-axis
                movement_list[1].append(float(elements[2]))  # y-axis

        elif(eyes_recorded == "right"):
            if(elements[4] == "."):
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(np.nan)
                movement_list[0].append(np.nan)  # x-axis
                movement_list[1].append(np.nan)
            else:
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(float(elements[6]))
                movement_list[0].append(float(elements[4]))  # x-axis
                movement_list[1].append(float(elements[5]))  # y-axis
        else:
            raise NameError("Define if eyes_recorded was either the left eye or the right eye")
    else:
        if(elements[1] == "."):
            timestamps_list.append(int(elements[0]))
            pupil_size_list.append(np.nan)
            movement_list[0].append(np.nan)  # x-axis
            movement_list[1].append(np.nan)
        else:
            timestamps_list.append(int(elements[0]))
            pupil_size_list.append(float(elements[3]))
            movement_list[0].append(float(elements[1]))  # x-axis
            movement_list[1].append(float(elements[2]))  # y-axis
    return timestamps_list, pupil_size_list, movement_list


def input_read(input_dict, elements):
    input_num = int(elements[2])
    if input_num not in input_dict:
        input_dict[input_num] = []
    input_dict[input_num].append(int(elements[1]))
    # print(input_dict)

    return input_dict


def button_read(button_dict, elements):
    button_num = int(elements[2])
    button_press = int(elements[3])
    if button_num not in button_dict:
        button_dict[button_num] = [[],[]]

    if button_press == 1:
        button_dict[button_num][1].append(int(elements[1]))

    elif button_press == 0:
        button_dict[button_num][0].append(int(elements[1]))

    return button_dict



    button_name = f"{elements[0]} {elements[2]}"
    # will extract left or right eye data from recording set set from both eye recordings

    if (button_name not in button_dict):
        button_dict[button_name] = [[],[]]
    if(button_name in button_dict):
        button_list_variable = int(elements[3])
        temp_list = []
        for var in event_list_variable:
            temp_list.append(int(var))
        event_list_variable = temp_list

def misc_read(elements,misc):
    misc.append([elements])
    return misc

def event_read(events_dict, elements, eyes_recorded, both_eyes_recorded):
    """
    Finds And Returns Events
    - Checks if event name already exists before appending
    """
    event_name = f"{elements[0]} {elements[1]}"
    # will extract left or right eye data from recording set set from both eye recordings
    if both_eyes_recorded:
        if(eyes_recorded == "left"):
            if (elements[1] == "R" and event_name not in events_dict):
                events_dict[event_name] = []
        elif(eyes_recorded == "right"):
            if (elements[1] == "R" and event_name not in events_dict):
                events_dict[event_name] = []
        if(event_name in events_dict):
            event_list_variable = elements[2:]
            temp_list = []
            for var in event_list_variable:
                if var == ".":
                    var = np.nan
                    temp_list.append(var)
                else:
                    temp_list.append(float(var))
            event_list_variable = temp_list

            temp_list = list(map(float,temp_list))
            events_dict[event_name].append(temp_list)

    # will extract data from one eye data, 'auto'
    else:
        if event_name not in events_dict:
            events_dict[event_name] = []

        event_list_variable = elements[2:]
        temp_list = []
        for var in event_list_variable:
            if var == ".":
                var = np.nan
                temp_list.append(var)
            else:
                temp_list.append(float(var))
        event_list_variable = temp_list

        temp_list = list(map(float,temp_list))
        events_dict[event_name].append(temp_list)
    return events_dict



def remove_eye_blinks(abra_obj, buffer=50, interpolate='linear', inplace=False):
    """
    The remove_eye_blinks method replaces the eyeblinks (NAS) with
    interpolated data, with a buffer of 50 data points and linear spline
    to do interpolation.
    ### Linear interpolation is what is supported right now.
    """
    ##keep NAs for the movemnt
    #Buffer
    pupilsize_ = np.copy(abra_obj.pupil_size)
    movements_ = np.copy(abra_obj.movement)
    blink_times = np.isnan(pupilsize_)

    for j in range(len(blink_times)):
        if blink_times[j]==True:
            pupilsize_[j-buffer:j+buffer]=np.nan
            movements_[0][j-buffer:j+buffer]=np.nan
            movements_[1][j-buffer:j+buffer]=np.nan
    abra_obj.movement = movements_

    # Interpolate
    interp_move = [[],[]]
    if interpolate=='linear':
        interp_pupil_size = utils.linear_interpolate(pupilsize_)
        # interp_move = utils.linear_interpolate(movements_)
        # interp_move = utils.linear_interpolate(movements_)

        if inplace == True:
            abra_obj.pupil_size = interp_pupil_size
            # abra_obj.pupil_size = interp_move
        elif inplace == False:
            tmp_obj = copy.deepcopy(abra_obj)
            tmp_obj.pupil_size = interp_pupil_size
            # tmp_obj.movement = movements_
            return tmp_obj
    else:
        print("We haven't implement anyother interpolation methods yet")
        return False



class Data:
    """
    The Data class for the data structure

    Use read function to create Data object

    - Stores data values of timestamps, pupil_size, movement, sample_rate,
      calibration, messages, events, trial_markers

    - Value Types:
        - timestamps: List (1xn)

        - pupil_size: List (1xn)

        - Movement: List (2xn)
            > index 0: x-coordinates
            > index 1: y-coordinates

        - sample_rate: int

        -calibration: Dictionary (not implimented yet)

        - message: Dictionary
            > key: timestamp integer
            > value: message

        - events: Dictionary
            > key: event name
            > value: list of [start timestamp, end timestamp,
                              avg y-coordinate, avg x-coordinate,
                              avg pupil size]

        - trial_markers: Dictionary
            > key: 'Start' or 'End'
            > value: list of time stamps

        -buttons: Dictionary
            > key: button number
            > value: list [unpress (0)] and [press (1)]
                > index 0 is unpress
                > index 1 is press
    """


    def __init__(self, timestamps, pupil_size, movement, sample_rate,
                 calibration, messages, events, trial_markers, buttons,
                 inputs, misc):
        self.timestamps = timestamps
        self.pupil_size = pupil_size
        self.movement = movement
        self.sample_rate = sample_rate
        self.calibration = calibration
        self.messages = messages
        self.events = events
        self.trial_markers = trial_markers
        self.buttons = buttons
        self.inputs = inputs
        self.misc = misc



    def create_session(self, conditions=None, start_marker = 'msg',
                       end_marker = 'msg', input_start = None, input_end = None,
                       button_start = None, button_end = None):
        """
        This function splits the pupil size and timestamp data into
        its respective trials and returns an array of trial class
        objects

        - condition: event condition

        - start_marker: type of marker set to identify the start of the session
            - 'msg': defualt marker type. Inputs message in data to identify start
            - 'input': Uses an input marker to symbolize the start of the session
            - 'button': Uses buttons events to identify the start of a session

        - end_marker: type of marker set to identify the end of the session
            - 'msg': defualt marker type. Inputs message in data to identify end
            - 'input': Uses an input marker to symbolize the end of the session
            - 'button': Uses buttons events to identify the end of a session

        - input_start: input number (eg. input_start = 1)

        - input_end: input number (eg. input_end = 2)

        - button_start: button number and whether you want the press event or
                        release event. (eg. button_start = 1_1 for press
                                            button_start = 1_0 for release)

        - button_end: button number and whether you want the press event or
                      release event (eg. button_start = 1_1 for press
                                         button_start = 1_0 for release)

        """


        t_Time = self.timestamps
        if(start_marker.lower() == 'msg'):
            t_Mark = self.trial_markers
            start = t_Mark['start']

        elif(start_marker.lower() == 'input'):
            start = self.inputs[input_start]
        elif(start_marker.lower() == 'button'):
            start = self.buttons[button_start[0]][button_start[1]]

        if(end_marker.lower() == 'msg'):
            end = t_Mark['end']
        elif end_marker.lower() == 'input':
            end = self.inputs[input_end]
        elif end_marker.lower() == 'button':
            end = self.buttons[button_end[0]][button_start[1]]


        # All trial start and end markers in array ([start,end])
        trial_IDX = []

        for i in range(len(start)):
            temp = []
            st = start[i]
            en = end[i]
            temp.append(st)
            temp.append(en)
            trial_IDX.append(temp)

        # Get the pupil size in the events between the starting and ending markers
        trial_pupil = []
        trial_mov_x = []
        trial_mov_y = []
        trial_stamp = []
        trial_event_L_fix = []
        trial_event_R_fix = []
        index_L = 0
        index_R = 0
        for i in range(len(trial_IDX)):
            st = trial_IDX[i][0]
            en = trial_IDX[i][1]

            # Find the indexes to call the pupil size within the timestamps for a trial
            idx = np.where((self.timestamps >= st) & (self.timestamps <= en))[0]

            # Add the pupil sizes for each timestamp
            temp_pupil = []
            temp_movex = []
            temp_movey = []
            temp_stamp = []
            temp_L_event = []
            temp_R_event = []
            for k in idx:
                temp_pupil.append(self.pupil_size[k])
                temp_stamp.append(self.timestamps[k])
                temp_movex.append(self.movement[0][k])
                temp_movey.append(self.movement[1][k])
                if('EFIX L' in self.events and index_L < len(self.events['EFIX L']) and self.events['EFIX L'][index_L][1] == self.timestamps[k]):
                    temp_L_event.append(self.events['EFIX L'][index_L])
                    index_L += 1
                if('EFIX R' in self.events and index_R < len(self.events['EFIX R']) and self.events['EFIX R'][index_R][1] == self.timestamps[k]):
                    temp_R_event.append(self.events['EFIX R'][index_R])
                    index_R += 1
            trial_pupil.append(np.array(temp_pupil))
            trial_mov_x.append(np.array(temp_movex))
            trial_mov_y.append(np.array(temp_movey))
            trial_stamp.append(np.array(temp_stamp))
            trial_event_L_fix.append(np.array(temp_L_event))
            trial_event_R_fix.append(np.array(temp_R_event))


        # Create a list of new trials with each pupil_size
        trials = []
        for i in range(len(trial_IDX)):
            t = trial.Trial(trial_stamp[i], trial_pupil[i],
                            trial_mov_x[i], trial_mov_y[i],
                            trial_event_L_fix[i], trial_event_R_fix[i])
            trials.append(t)

        # Check for conditions
        num_trials = len(trials)
        if conditions is not None:
            if (len(conditions) != num_trials):
                raise ValueError('Condition length must be equal to the number of trials: ', num_trials)

        return session.Session(np.array(trials), self.sample_rate, conditions)

    def create_epochs(self, event_timestamps, conditions=None, pre_event=200,
                      post_event=200, pupil_baseline=None):
        """
        Create Time Locking Epochs

        event_timestamps: starting timestamps for all time locking events
        conditions: event condition
        pre_event: milliseconds before defined starting timestamps
        post_event: milliseconds after defined starting timestamps
        pupil_baseline: Baselining for pupil size data,
                        baseline period will be the milliseconds
                        before pre_event
        """

        #Create an empty array for storing the epoch information
        win_size = int((pre_event+post_event)*self.sample_rate/1000)
        all_epochs = []

        # Iterate timestamp events get each epoch pupil size
        for i in range(len(event_timestamps)):
            start = event_timestamps[i]-pre_event
            end = event_timestamps[i]+post_event
            idx = (self.timestamps >= (event_timestamps[i]-pre_event)) & (self.timestamps <= (event_timestamps[i]+post_event))

            if np.sum(idx) != win_size:
                non_zero_idx = np.nonzero(idx)

                # Explicitly set all values beyond window size to False
                # Enforcing the length to be the defined window size
                idx[non_zero_idx[0][0]+win_size:]=False
            epoch_pupil = self.pupil_size[idx]
            epoch_movex = self.movement[1][idx]
            epoch_movey = self.movement[0][idx]

            # Do baselining using the mean and standard deviation of the mean and variance
            if pupil_baseline:
                baseline_idx = (self.timestamps >= (event_timestamps[i]-pre_event+pupil_baseline[0])) & (self.timestamps <= (event_timestamps[i]-pre_event+pupil_baseline[1]))
                baseline_period = self.pupil_size[baseline_idx]
                baseline_mean = np.mean(baseline_period)
                baseline_std = np.std(baseline_period)
                epoch_pupil = (epoch_pupil - baseline_mean)/baseline_std

            t = trial.Trial(self.timestamps[idx], epoch_pupil, epoch_movex, epoch_movey)
            all_epochs.append(t)

        epochs = session.Epochs(all_epochs, self.sample_rate, conditions)
        return epochs
