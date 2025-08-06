from PyQt6.QtCore import QSettings

# class SettingsHandler:
#     def __init__(self, fields, org="MyCompany", app="MyApp"):
#         self.fields = fields
#         self.settings = QSettings(org, app)

#     def load(self):
#         for key, widget, cast, default in self.fields:
#             if not widget:
#                 continue
#             try:
#                 val = cast(self.settings.value(key, default))
#                 getattr(widget, self._setter(widget))(val)
#             except Exception as e:
#                 print(f"[Load error] {key}: {e}")

#     def connect_autosave(self):
#         print("CONNECTED")
#         for key, widget, *_ in self.fields:
#             if not widget:
#                 continue
#             try:
#                 signal = self._signal(widget)
#                 getter = getattr(widget, self._getter(widget))
#                 signal.connect(lambda _, w=widget, k=key, g=getter: self.settings.setValue(k, g()))
#             except Exception as e:
#                 print(f"[Connect error] {key}: {e}")

#     def _setter(self, widget):
#         return "setValue" if hasattr(widget, "setValue") else "setText"

#     def _getter(self, widget):
#         return "value" if hasattr(widget, "valueChanged") else "text"

#     def _signal(self, widget):
#         return widget.valueChanged if hasattr(widget, "valueChanged") else widget.textChanged


class SettingsHandler:
    def __init__(self, fields, org="MyCompany", app="MyApp"):
        self.fields = fields
        self.settings = QSettings(org, app)

    def _setter(self, w):
        # If it has setChecked method, treat as checkbox
        if hasattr(w, "setChecked"):
            return "setChecked"
        return "setValue" if hasattr(w, "setValue") else "setText"

    def _getter(self, w):
        # If it has isChecked method, treat as checkbox
        if hasattr(w, "isChecked"):
            return "isChecked"
        return "value" if hasattr(w, "valueChanged") else "text"

    def _signal(self, w):
        # If it has stateChanged signal, treat as checkbox
        if hasattr(w, "stateChanged"):
            return w.stateChanged
        return w.valueChanged if hasattr(w, "valueChanged") else w.textChanged

    def load(self):
        for key, widget, cast, default in self.fields:
            if not widget:
                continue
            try:
                val = self.settings.value(key, default)
                # Check if widget uses checked state
                if hasattr(widget, "setChecked") and hasattr(widget, "isChecked"):
                    val = val in ("true", "1", 1, True)
                else:
                    val = cast(val)
                getattr(widget, self._setter(widget))(val)
            except Exception as e:
                print(f"[Load error] {key}: {e}")

    def connect_autosave(self):
        for key, widget, *_ in self.fields:
            if not widget:
                continue
            try:
                sig = self._signal(widget)
                getter = getattr(widget, self._getter(widget))
                sig.connect(lambda _, w=widget, k=key, g=getter: self.settings.setValue(k, g()))
            except Exception as e:
                print(f"[Connect error] {key}: {e}")
