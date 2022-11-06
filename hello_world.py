import sys
from json import (load as jsonload, dump as jsondump)
from os import path
print(path.dirname(sys.executable))
print(sys.version)
import time
import PySimpleGUI as sg

def load_settings(settings_file, default_settings):
    try:
        print(settings_file)
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)


SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'db_name': 'cae-dga-euwe-sqldb-d', 'db_password': None}
# "Map" from the settings dictionary keys to the window's element keys
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'db_name': '-INPUT-DB-', 'db_password': '-INPUT-PASSWORD-'}

WIN_SIZE=(600,400)
FRAME_SIZE=(580,350)

def create_main_window():

    layout = [
              [sg.T('This is my main application')],
              [sg.B('Start'), sg.B('Exit')]]

    return sg.Window('Main Application', layout)


def create_db_connection_window(settings):

    container = [  [sg.Text('Database:'), sg.InputText( key='-INPUT-DB-',default_text='aaaa')],
                   [sg.Text('Password :'), sg.InputText( key='-INPUT-PASSWORD-')]
                ]

    frame =  sg.Frame('Frame', container, size=FRAME_SIZE, key='-FRAME-')
    next = [ [ sg.Button('Prev'),sg.Push(), sg.Button('Next',key='-BUTTON-NEXT-')] ]
    layout = [[frame],
             [next]]
     # Create the Window
    window = sg.Window('Connect to Database', layout,size=WIN_SIZE)
    window['Prev'].Disabled=True
    first_load = True
    while True:
        event, values = window.read(300)
        if event == sg.WIN_CLOSED  : # if user closes window or clicks cancel
            break
        elif event == sg.TIMEOUT_KEY:
            if(first_load) :
                window['-INPUT-DB-'].update(value=settings['db_name'])
                window['-INPUT-PASSWORD-'].update(value=settings['db_password'])
                first_load = False
        elif event == '-BUTTON-NEXT-':
            save_settings(SETTINGS_FILE,settings,values)
            break

    window.close()

def create_option_window(settings):

    container = [
        [sg.Radio('Upsert', "RADIO1", default=True,key = '-UPSERT-')],
        [sg.Radio('Scd2', "RADIO1", default=False, key = '-SCD2-')],
        [sg.Radio('Default Value for Dim Table', "RADIO1", default=False, key = '-DEFAULT_VALUE-')]    
        ]

    frame =  sg.Frame('Frame', container, size=FRAME_SIZE, key='-FRAME-')
    next = [ [ sg.Button('Prev'),sg.Push(), sg.Button('Next',key='-BUTTON-NEXT-')] ]
    layout = [[frame],
             [next]]
     # Create the Window
    window = sg.Window('Generate SQL', layout,size=WIN_SIZE)
    window['Prev'].Disabled=True
    first_load = True
    while True:
        event, values = window.read(300)
        if event == sg.WIN_CLOSED  : # if user closes window or clicks cancel
            break
        elif event == sg.TIMEOUT_KEY:
            if(first_load) :
                window['-INPUT-DB-'].update(value=settings['db_name'])
                window['-INPUT-PASSWORD-'].update(value=settings['db_password'])
                first_load = False
        elif event == '-BUTTON-NEXT-':
            save_settings(SETTINGS_FILE,settings,values)
            break

    window.close()



def main():

    settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS)

    window = create_main_window()
    while True:
        event, values = window.read(100)
        if event == sg.WIN_CLOSED  : # if user closes window or clicks cancel
            break
        elif event == 'Exit':
            break

        elif event == 'Start':
            window.Hide()
            create_db_connection_window(settings)
            window.UnHide()

        # if time.time() > end_time:
        #     print(time.time())
        #     break


    window.close()


if __name__ == '__main__':
    main()