__author__ = 'mFoxRU'

from time import sleep

from win32gui import FindWindow, EnumChildWindows, GetClassName, GetWindowText


class Hook(object):

    fields = ['Title', 'Author']
    is_dialog = lambda _, x: GetClassName(x) == '#32770'
    is_infobox = lambda s, x: GetWindowText(x) in s.fields

    def __init__(self):
        self.dlgs = None
        self.infobox = None

    def find_mpchc(self):
        mainwindow = FindWindow('MediaPlayerClassicW', None)
        while mainwindow == 0:
            mainwindow = FindWindow('MediaPlayerClassicW', None)
            sleep(1)
        self.dlgs = self.filter_children(mainwindow, self.is_dialog)

    def find_infobox(self):
        if self.dlgs is None:
            self.find_mpchc()
        # Waiting for any track playback to find appropriate dialog box
        while 1:
            for dialog in self.dlgs:
                try:
                    if len(self.filter_children(dialog, self.is_infobox)) > 0:
                        self.infobox = self.filter_children(dialog,
                                                            lambda x: 1)
                        return
                except Exception:
                    pass
            sleep(1)

    def update(self):
        if self.infobox is None:
            self.find_infobox()
        if GetWindowText(self.infobox[0]) not in self.fields:
            self.find_infobox()
        return GetWindowText(self.infobox[1]), GetWindowText(self.infobox[3])

    @staticmethod
    def filter_children(window, condition):
        children = []
        check = lambda x, _: children.append(x) if condition(x) else 1
        EnumChildWindows(window, check, None)
        return children

if __name__ == '__main__':
    hk = Hook()
    while 1:
        print ' - '.join(reversed(hk.update()))
        sleep(1)