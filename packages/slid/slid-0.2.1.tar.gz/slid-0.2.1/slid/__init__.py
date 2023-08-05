import PySimpleGUI as sg


def slid_alert(alert, custom_layout=None, use_custom=False, theme=None, title='Morph Alert', anilist=None,
                close_end=True, delay=0, delay_action=0.5, titlebar_visible=False, sound=None, use_sound=False, alpha=1, start_size=None, lamcheck=None,resize_start=False):
    layout = [[sg.Text(alert),sg.Button('OK')]]
    if anilist is None:
        anilist = ['-1*']
    if custom_layout is not None and use_custom is True:
        layout = custom_layout
    if theme is not None:
        sg.theme(theme)
    if delay != 0 or delay is not None:
        schedule = (delay,delay_action,close_end)
    else:
        schedule = (0,delay_action,close_end)
    if use_sound is True and sound is not None:
        try:
            import pygame
            pygame.init()
        except:
            print('pygame is not installed or has an error. Sounds disabled.')
            sound = None;use_sound=False
    if start_size:
        window = sg.Window(title,layout, no_titlebar=not titlebar_visible,alpha_channel=alpha,size=start_size,finalize=True)
    else:
        window = sg.Window(title,layout, no_titlebar=not titlebar_visible, alpha_channel=alpha,finalize=True)
    event, values = window.read()
    if anilist == ['-1*'] or anilist == ['-2*']:
        import time;time.sleep(schedule[0])
        if lamcheck is None:
            while window.size[0] > 10 and window.size[1] > 10:
                if anilist == ['-1*']:
                    window.size = (window.size[0]-1,window.size[1]-1)
                else:
                    window.size = (window.size[0] - 2, window.size[1] - 2)
                time.sleep(schedule[1])
        else:
            while lamcheck(window.size):
                if anilist == ['-1*']:
                    window.size = (window.size[0]-1,window.size[1]-1)
                else:
                    window.size = (window.size[0] - 2, window.size[1] - 2)
                time.sleep(schedule[1])
        if schedule[2]:
            window.close()
    else:
        import time;time.sleep(schedule[0])
        for i in anilist:
            if i.endswith('*'):
                if lamcheck is None:
                    while window.size[0] > 10 and window.size[1] > 10:
                        if i.startswith('-'):
                            window.size = (window.size[0]-int(i[1:len(i)-1]),window.size[1]-int(i[1:len(i)-1]))
                        else:
                            window.size = (window.size[0] + int(i[1:len(i) - 1]), window.size[1] + int(i[1:len(i) - 1]))
                        time.sleep(schedule[1])
                    if schedule[2]:
                        window.close()
                else:
                    while lamcheck(window.size):
                        if i.startswith('-'):
                            window.size = (window.size[0] - int(i[1:len(i) - 1]), window.size[1] - int(i[1:len(i) - 1]))
                        else:
                            window.size = (window.size[0] + int(i[1:len(i) - 1]), window.size[1] + int(i[1:len(i) - 1]))
                        time.sleep(schedule[1])
                    if schedule[2]:
                        window.close()
            else:
                if i.startswith('-'):
                    window.size = (window.size[0] - int(i[1:len(i)]), window.size[1] - int(i[1:len(i)]))
                else:
                    window.size = (window.size[0] + int(i[1:len(i)]), window.size[1] + int(i[1:len(i)]))
                time.sleep(schedule[1])
        return 0