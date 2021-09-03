from pynput import mouse, keyboard
from datetime import datetime, timedelta
import pandas as pd
import ctypes

PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

start_time  = datetime.now()
mouse_df = pd.DataFrame(columns=["Timestamp", "x", "y", "Action"])
keyboard_df = pd.DataFrame(columns=["Timestamp", "key"])

class Listeners:

    '''

    Class to initialise mouse and keyboard listeners

    '''

    def __init__(self):
        self.mouse = ''
        self.keyboard = ''
        self.mousetime = start_time
        self.keyboard_df = keyboard_df
        self.mouse_df = mouse_df

    def on_press(self, key):

        '''

         Function to collate keyboard events

        Args:
            key (object) : key pressed

        Returns:
            If key f12 is pressed:
                False (Boolean) to force stop listener.
            Else:
                update pandas dataframe with collected data
        '''

        kcurrent_time = datetime.now()
        self.keyboard_df = self.keyboard_df.append({'Timestamp': kcurrent_time,
                                                    'key': key}, ignore_index=True,)
        if key == keyboard.Key.f12:
            print('Stopping keyboard')
            return False

    def on_move(self, x, y):

        '''

        Function to collate mouse movements events

        Args:
            x (float): X-location of mouse hover
            y (float): Y-location of mouse hover

        Returns:
             If keyboard is stopped :
                False (boolean) to force stop listener and create 2 csv files for keyboard and mouse events collection
            Else:
                update pandas dataframe with collected data

        '''

        mcurrent_time = datetime.now()
        self.mouse_df = self.mouse_df.append({'Timestamp': mcurrent_time,
                                              'x': x ,
                                              'y': y,
                                              "Action": 'Move'}, ignore_index=True, )
        if self.keyboard.running is False:
            end_time = datetime.now()
            self.keyboard_df.to_csv('keyboard.csv')
            self.mouse_df.to_csv('mouse.csv')
            print('Stopping Mouse')
            print('Total Time taken : {}'.format(end_time-start_time))
            return False

    def on_click(self, x, y, button, pressed):

        '''

        Function to collate mouse click events

        Args:
            x (float) : X-location of mouse hover
            y(float) : Y-location of mouse hover
            button (str): mouse button click
            pressed (boolean): True for click, False for release

        Returns:
            update pandas dataframe with collected data

        '''

        mcurrent_time = datetime.now()
        if pressed:
            self.mouse_df = self.mouse_df.append({'Timestamp': mcurrent_time,
                                                  'x': x ,
                                                  'y': y,
                                                  "Action": 'Click {}'.format(button)}, ignore_index=True, )
        else:
            self.mouse_df = self.mouse_df.append({'Timestamp': mcurrent_time,
                                                  'x': x,
                                                  'y': y,
                                                  "Action": 'Release {}'.format(button)}, ignore_index=True, )

    def on_scroll(self, x, y, dx, dy):

        '''

        Function to collate mouse scroll events

        Args:
            x (float): X-location of mouse hover
            y (float): Y-location of mouse hover
            dx (float): horizontal movement by scoll
            dy (float): vertical movement by scoll

        Returns:
            update pandas dataframe with collected data
        '''

        mcurrent_time = datetime.now()
        if dy > 0:
            self.mouse_df = self.mouse_df.append({'Timestamp': mcurrent_time,
                                                  'x': x,
                                                  'y': y,
                                                  "Action": 'Scroll Up'}, ignore_index=True, )
        else:
            self.mouse_df = self.mouse_df.append({'Timestamp': mcurrent_time,
                                                  'x': x,
                                                  'y': y,
                                                  "Action": 'Scroll Down'}, ignore_index=True, )

    def start_recording(self):

        '''

        Function to initialise and start recording data

        Returns:
            None

        '''

        self.mouse = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)

        self.keyboard = keyboard.Listener(
            on_press=self.on_press)

        self.keyboard.start()
        self.mouse.start()
        self.keyboard.join()
        self.mouse.join()

listen = Listeners()
listen.start_recording()

