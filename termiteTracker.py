#!/usr/bin/env python3

import time

class termiteTracker:

    def __init__(self):
        self.actions = list()
        self.start_time = None
        self.idx_last_action = None
        self.started = False
        self.paused = False

        self.start_of_paused_time = 0

    def start(self, action, one_time_only = False):
        self.start_or_pause(action)

    def start_or_pause(self, action = None, one_time_only = False):
        """
        Start or pause or restart tracking

        NOTE: These unittests are probably not how you should do this
        >>> tt = termiteTracker()
        >>> tt.start_or_pause('spam')
        >>> time.sleep(0.1)
        >>> tt.start_or_pause()
        >>> time.sleep(0.1)
        >>> tt.start_or_pause()
        >>> time.sleep(0.1)
        >>> tt.get_time()
        0.2

        """
        # first start
        if not self.started:
            self.start_time = time.time()

            assert action is not None, ("Please specify an action when starting first time")
            assert not one_time_only, ("You can't start recording with a one-time-only action")

            self.actions.append([action, 0, -1])
            self.idx_last_action = 0

            self.started = True

            return

        # if we're here, apparently we should pause or unpause
        # We should pause
        if not self.paused:
            self.pause()
        # we should resume
        else:
            self.unpause()

    def unpause(self):
        if self.paused:
            # we simply add the passed time to the start time
            elapsed_time = time.time() - self.start_of_paused_time
            self.start_time += elapsed_time
            self.start_of_paused_time = 0
        self.paused = False

    def pause(self):
        if not self.paused:
            self.start_of_paused_time = time.time()
        self.paused = True

    def stop(self):
        self.actions = list()
        self.start_time = None
        self.idx_last_action = None
        self.started = False
        self.paused = False

        self.start_of_paused_time = 0
        running = False

    def get_time(self):
        if self.paused:
            return round(self.start_of_paused_time - self.start_time, 2)
        else:
            return round(time.time() - self.start_time, 2)

    def record_action(self, action, one_time_only = False):
        """ Records an action and writes in in the actions list.


        @param self The object pointer
        @param action string describing the action
        @param one_time_only Determines whether the action has a duration

        >>> tT = termiteTracker()
        >>> tT.start('stay')
        >>> time.sleep(0.1)
        >>> tT.record_action('run')
        >>> time.sleep(0.1)
        >>> tT.record_action('sleep')
        >>> tT.actions[1][0]
        'run'
        >>> tT.actions[1][1] > 0
        True
        >>> tT.actions[1][2] > 0
        True
        """
        assert self.start_time is not None, (
            "Please start the recording before recording actions!")

        # check if the previous action is the same
        if self.actions[self.idx_last_action][0] == action:
            print("I'm already {}-ing!".format(action))
            return

        # calculate the time that the action occured
        # (down to 100ths of a second)
        t = self.get_time()

        # if the current action is not one-time-only:
        # add a duration to the previous action
        if not one_time_only:
            time_last_action = self.actions[self.idx_last_action][1]
            self.actions[self.idx_last_action][2] = round(t - time_last_action, 2)
            self.idx_last_action = len(self.actions)

        self.actions.append([action, t, 0])

    def get_export_lst(self, delimiter="\t"):
        msg_lst = [delimiter.join(["#Aktion", "StartZeit", "Dauer"])]

        # we need to update the duration of the last action
        time_last_action = self.actions[self.idx_last_action][1]
        self.actions[self.idx_last_action][2] = round(self.get_time -
                                                      time_last_action, 2)

        for act in self.actions:
            print(act)
            msg_lst.append(delimiter.join([str(entry) for entry in act]))

        return "\n".join(msg_lst)
