from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_selection_list import UISelectionList
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine

import pygame_gui
from ui.ui import *

import file_utils

from pathlib import Path

class SaveLoadWindow(UIWindow):
    def __init__(self, rect, path, title, confirm_callback, save):
        super().__init__(
            rect,
            ui_manager,
            window_display_title=title,
            resizable=True
        )

        # set initial path
        self.path = path
        self.current_file_list = []
        self.confirm_callback = confirm_callback
        self.save = save

        # set minimum dimensions
        minimum_dimensions = (300, 300)
        self.set_minimum_dimensions(minimum_dimensions)

        # file browser panel
        file_selection_rect = pygame.Rect(
            10,
            20,
            self.get_container().get_size()[0] - 20,
            self.get_container().get_size()[1] - 70
        )

        self.update_file_list()
        self.file_selection_list = UISelectionList(
            relative_rect=file_selection_rect,
            item_list=self.current_file_list,
            manager=ui_manager,
            container=self,
            object_id='#file_display_list',
            anchors=
            {
                'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )
        register_ui_callback(
            self.file_selection_list,
            pygame_gui.UI_SELECTION_LIST_NEW_SELECTION,
            lambda e: self.file_name_text_line.set_text(e.text)
        )

        # text entry line to write file name
        text_line_rect = pygame.Rect(10, -40, self.get_container().get_size()[0] - 110, 25)
        self.file_name_text_line = UITextEntryLine(
            relative_rect=text_line_rect,
            manager=self.ui_manager,
            container=self,
            object_id='#file_path_text_line',
            anchors=
            {
                'left': 'left',
                'right': 'right',
                'top': 'bottom',
                'bottom': 'bottom'
            }
        )
        if not save:
            self.file_name_text_line.disable()

        # confirm button
        confirm_btn_rect = pygame.Rect(-90, -40, 80, 30)
        self.confirm_btn = UIButton(
            relative_rect=confirm_btn_rect,
            text="OK",
            manager=self.ui_manager,
            container=self,
            anchors=
            {
                'left': 'right',
                'right': 'right',
                'top': 'bottom',
                'bottom': 'bottom'
            }
        )
        register_ui_callback(
            self.confirm_btn,
            pygame_gui.UI_BUTTON_PRESSED,
            lambda e: (
                self.on_confirm_btn_click()
            )
        )

        self.set_blocking(True)

    def on_confirm_btn_click(self):
        target_file = self.file_name_text_line.get_text()
        if not self.save:
            files = self.get_files_in_path()
            if target_file not in files:
                show_message_box("<b><font face='verdana' color='#FF3333' size=3.5>"
                                 "Invalid file name"
                                 "</font></b>")
                self.kill()
                return

        self.confirm_callback(target_file),
        self.kill()

    def update_file_list(self):
        #files = [f.name for f in Path(self.path).iterdir() if f.is_file() ]
        files = self.get_files_in_path()
        files = sorted(files, key=str.casefold)
        self.current_file_list = files

    def get_files_in_path(self):
        files = file_utils.get_all_files_in_path(self.path, MAPS_EXTENSION)
        files = [f.split('/')[1] for f in files]
        return files

