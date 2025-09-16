from .logic import Logic
from .bundle import Bundle

class Connections(Bundle):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic

        

        self.drive_selector_input.layout.drive_combo.currentTextChanged.connect(
            self.source_footage_view.logic.set_directory
        )



        self.source_footage_view.layout.files_view.doubleClicked.connect(self.source_footage_view.logic.preview_file)



        # self.source_footage_view.layout.files_view.clicked.connect(      
        #     lambda *_: self.logic.handle_file_items(
        #     self.source_footage_view.logic.collect_selected_items()
        #     )
        # )

        self.source_footage_view.layout.files_view.customContextMenuRequested.connect(
                        lambda *_: self.logic.handle_file_items(
            self.source_footage_view.logic.collect_selected_items()
            )
        )



        self.merge_btn.clicked.connect(self.logic.merge_footage)
        self.reset_settings_btn.clicked.connect(self.logic.settings_handler.reset_settings)
