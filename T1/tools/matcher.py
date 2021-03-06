from src.base import *

'''
Matcher class
    Methods (All statics):
        find_subsequence: finds consecutive frames according on the filename, number of the frame and the given epsilon
            (this last one give a tolerance of blank frames)       
'''
class Matcher:

    @staticmethod
    def find_subsequence(frame, i, kbox, epsilon=0):
        sequence = []
        previous_frame = frame
        strikes = 0
        j = i + 1
        while j < kbox.size():
            knf_array = kbox.get_knf(j).get_array()
            has_next = False
            h = 0
            while not has_next and h < len(knf_array):
                other_frame = knf_array[h]
                if previous_frame == other_frame and previous_frame.is_next(other_frame, strikes + 1):
                    has_next = True
                h += 1

            if has_next:
                sequence.append(other_frame)
                previous_frame = other_frame
                strikes = 0
            elif strikes == epsilon:
                return sequence
            else:
                sequence.append(None)
                strikes += 1
            j += 1

        return sequence

