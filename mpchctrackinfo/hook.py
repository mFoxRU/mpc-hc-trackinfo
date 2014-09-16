__author__ = 'mFoxRU'

from time import sleep

from win32gui import FindWindow, EnumChildWindows, GetClassName, \
    GetWindowText, IsWindow


class Hook(object):

    def __init__(
            self,
            window='MediaPlayerClassicW',
            class_name='#32770',
            fields=('Title', 'Author')
    ):
        self._mpc_name = window
        self._fields = fields
        self._is_dialog = lambda x: GetClassName(x) == class_name
        self._is_infobox = lambda x: GetWindowText(x) in self._fields
        self._find_mpchc()
        self._find_infobox()

    def _find_mpchc(self):
        mainwindow = FindWindow(self._mpc_name, None)
        # Waiting for mpc-hc to start
        while mainwindow == 0:
            mainwindow = FindWindow(self._mpc_name, None)
            sleep(1)
        self._mpc = mainwindow
        self._dlgs = self._filter_children(self._mpc, self._is_dialog)

    def _find_infobox(self):
        if not IsWindow(self._mpc):
            if GetClassName(self._mpc) != self._mpc_name:
                self._find_mpchc()
        # Waiting for any track playback to find appropriate dialog box
        while 1:
            for dialog in self._dlgs:
                try:
                    if len(self._filter_children(dialog, self._is_infobox)) > 0:
                        self._infobox = self._filter_children(dialog,
                                                              lambda x: 1)
                        return
                except Exception:
                    pass
            sleep(1)

    @staticmethod
    def _filter_children(window, condition):
        children = []
        check = lambda x, _: children.append(x) if condition(x) else 1
        EnumChildWindows(window, check, None)
        return children

    def get_info(self, reverse=True):
        if GetWindowText(self._infobox[0]) not in self._fields:
            self._find_infobox()
        retval = [GetWindowText(x) for x in self._infobox[1::2]]
        return reversed(retval) if reverse else retval


if __name__ == '__main__':
    hk = Hook()
    while 1:
        print ' - '.join(hk.get_info())
        sleep(1)
