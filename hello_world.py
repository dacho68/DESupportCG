import sys
from json import (load as jsonload, dump as jsondump)
from os import path
print(path.dirname(sys.executable))
print(sys.version)
import time
import PySimpleGUI as sg


SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'db_name': 'cae-dga-euwe-sqldb-d', 'db_password': None , 'sql_gen_opt':0, 'src_schema':None,
'src_table':None, 'dest_schema':None, 'dest_table':None }
# "Map" from the settings dictionary keys to the window's element keys
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'db_name': '-INPUT-DB-', 'db_password': '-INPUT-PASSWORD-',
'src_schema':'-INPUT-SRC-SCHEMA-','src_table':'-INPUT-SRC-TABLE-','dest_schema':'-INPUT-DEST-SCHEMA-','dest_table':'-INPUT-DEST-TABLE-'}


WIN_SIZE=(600,400)
FRAME_SIZE=(580,350)


def load_settings(settings_file, default_settings, reset):
    try:
        if reset:
            settings = default_settings
            save_settings(settings_file, settings, None)
        else:
            print(settings_file)
            with open(settings_file, 'r') as f:
                settings = jsonload(f)

    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings

def save_default(settings_file, settings):
    with open(settings_file, 'w') as f:
        jsondump(settings, f)

def save_settings(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)



def create_db_connection_window(prev_window,settings):

    container = [  [sg.Text('Database:'), sg.InputText( key='-INPUT-DB-',default_text='')],
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
            window.Hide()
            save_settings(SETTINGS_FILE,settings,values)
            create_option_window(window,settings)
            
        elif event == 'Prev':
            prev_window.UnHide()

    window.close()

def create_option_window(prev_window,settings):

    container = [
        [sg.Radio('Upsert', "RADIO1", default=True,key = '-OPT1-')],
        [sg.Radio('Scd2', "RADIO1", default=False, key = '-OPT2-')],
        [sg.Radio('Default Value for Dim Table', "RADIO1", default=False, key = '-OPT3-')]    
        ]

    frame =  sg.Frame('Frame', container, size=FRAME_SIZE, key='-FRAME-')
    prev_next = [ [ sg.Button('Prev'),sg.Push(), sg.Button('Next',key='-BUTTON-NEXT-')] ]
    layout = [[frame],
             [prev_next]]

     # Create the Window
    window = sg.Window('Generate SQL', layout,size=WIN_SIZE)
    
    first_load = True
    while True:
        event, values = window.read(300)
        if event == sg.WIN_CLOSED  : # if user closes window or clicks cancel
            break
        elif event == sg.TIMEOUT_KEY:
            if(first_load) :
                value=settings['sql_gen_opt']
                if value == 0:
                    window['-OPT1-'].update(value=True)
                elif value == 1:
                    window['-OPT2-'].update(value=True)
                elif value == 2:
                    window['-OPT3-'].update(value=True)

                first_load = False
        
        elif event == '-BUTTON-NEXT-':
            save_settings(SETTINGS_FILE,settings,values)
            window.Hide()
            create_schema_table_window(window, settings)

        elif event == 'Prev':
            save_settings(SETTINGS_FILE,settings,values)
            prev_window.UnHide()
            break

        if values["-OPT1-"]==True:
            settings['sql_gen_opt']=0

        elif values["-OPT2-"]==True:
            settings['sql_gen_opt']=1

        elif values["-OPT3-"]==True:
            settings['sql_gen_opt']=2                        


    window.close()


def create_schema_table_window(prev_window,settings):

    container = [  [sg.Text('Source Schema:'), sg.InputText( key='-INPUT-SRC-SCHEMA-')],
                   [sg.Text('Source Table :'), sg.InputText( key='-INPUT-SRC-TABLE-')],
                   [sg.Text('Destination Schema:'), sg.InputText( key='-INPUT-DEST-SCHEMA-')],
                   [sg.Text('Destination Table :'), sg.InputText( key='-INPUT-DEST-TABLE-')],
                   [sg.Button('Load')]
                ]

    frame =  sg.Frame('Load Meta', container, size=FRAME_SIZE, key='-FRAME-')
    next = [ [ sg.Button('Prev'),sg.Push(), sg.Button('Next',key='-BUTTON-NEXT-')] ]
    layout = [[frame],
             [next]]
     # Create the Window
    window = sg.Window('Load Meta', layout,size=WIN_SIZE)
    first_load = True
    while True:
        event, values = window.read(300)
        if event == sg.WIN_CLOSED  : # if user closes window or clicks cancel
            break
        elif event == sg.TIMEOUT_KEY:
            if(first_load) :
                window['-INPUT-SRC-SCHEMA-'].update(value=settings['src_schema'])
                window['-INPUT-SRC-TABLE-'].update(value=settings['src_table'])
                window['-INPUT-DEST-SCHEMA-'].update(value=settings['dest_schema'])
                window['-INPUT-DEST-TABLE-'].update(value=settings['dest_table'])
                first_load = False

        elif event == '-BUTTON-NEXT-':
            window.Hide()
            save_settings(SETTINGS_FILE,settings,values)
            create_option_window(window,settings)
            
        elif event == 'Prev':
            prev_window.UnHide()

    window.close()


def main():

    settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS,False)

    layout = [
              [sg.B('Reset Config File',key='-BUTTON-RESET-')],
              [sg.B('Start'), sg.B('Exit')]]

    window =  sg.Window('Main Application', layout)

    while True:
        event, values = window.read(100)
        if event == sg.WIN_CLOSED  : # if user closes window or clicks cancel
            break
        elif event == 'Exit':
            break
        elif event == '-BUTTON-RESET-':
            settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS,True)
                    
        elif event == 'Start':
            window.Hide()
            create_db_connection_window(window,settings)

    window.close()


if __name__ == '__main__':
    main()