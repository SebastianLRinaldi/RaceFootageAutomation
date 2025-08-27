from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.ui.drive_selector_input.layout.drive_combo.currentTextChanged.connect(
            self.ui.source_footage_view.logic.set_directory
        )



        self.ui.source_footage_view.layout.files_view.doubleClicked.connect(self.ui.source_footage_view.logic.preview_file)



        # self.ui.source_footage_view.layout.files_view.clicked.connect(      
        #     lambda *_: self.logic.handle_file_items(
        #     self.ui.source_footage_view.logic.collect_selected_items()
        #     )
        # )

        self.ui.source_footage_view.layout.files_view.customContextMenuRequested.connect(
                        lambda *_: self.logic.handle_file_items(
            self.ui.source_footage_view.logic.collect_selected_items()
            )
        )



        self.ui.merge_btn.clicked.connect(self.logic.merge_footage)
        self.ui.reset_settings_btn.clicked.connect(self.logic.settings_handler.reset_settings)
