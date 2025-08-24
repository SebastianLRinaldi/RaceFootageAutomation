from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        
        # self.ui.dir_drive_selector.layout.drive_combo.currentTextChanged.connect(self.ui.footage_file_selector.logic.update_directory)
        # self.ui.footage_file_selector.logic.valueChanged.connect(self.ui.dir_drive_selector.layout.drive_combo.setCurrentText)


        self.ui.drive_selector_input.logic.current_directory_changed.connect(
            self.ui.file_selector_input.logic.update_directory
            )
        
        # # SETTINGS ONLY CALL
        # self.ui.file_selector_input.logic.valueChanged.connect(
        #     self.ui.drive_selector_input.logic.set_current_directory
        #     )





        
        # self.ui.pick_files_btn.clicked.connect(self.logic.pick_files)
        # self.ui.change_output_btn.clicked.connect(self.logic.change_output_location)
        # self.ui.merge_btn.clicked.connect(self.logic.merge_files)
        self.ui.reset_settings_btn.clicked.connect(self.logic.settings_handler.reset_settings)
