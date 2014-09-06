__author__ = 'mFoxRU'

from time import sleep

from win32gui import FindWindow, EnumChildWindows, GetClassName, GetWindowText


class Hook(object):

    fields = ['Title', 'Author']
    is_dialog = lambda _, x: GetClassName(x) == '#32770'
    is_infobox = lambda s, x: GetWindowText(x) in s.fields

    def __init__(self):
        pass

    def find_mpchc(self):
        mainwindow = FindWindow('MediaPlayerClassicW', None)
        while mainwindow == 0:
            mainwindow = FindWindow('MediaPlayerClassicW', None)
            sleep(1)
        return self.filter_children(mainwindow, self.is_dialog)

    def find_infobox(self):
        dlgs = self.find_mpchc()
        # Waiting for any track playback to find appropriate dialog box
        while 1:
            for dialog in dlgs:
                try:
                    if len(self.filter_children(dialog, self.is_infobox)) > 0:
                        return self.filter_children(dialog, lambda x: 1)
                except Exception:
                    pass
            sleep(1)


    def update(self):
        pass

    @staticmethod
    def filter_children(window, condition):
        children = []
        check = lambda x, _: children.append(x) if condition(x) else 1
        EnumChildWindows(window, check, None)
        return children


hk = Hook().find_infobox()

while 1:
    print GetWindowText(hk[1]), '|', GetWindowText(hk[3])
    sleep(1)