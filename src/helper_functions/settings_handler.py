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


# class SettingsHandler:
#     def __init__(self, fields, org="MyCompany", app="MyApp"):
#         self.fields = fields
#         self.settings = QSettings(org, app)
#         self.load()
#         self.connect_autosave()

#     def _setter(self, w):
#         # If it has setChecked method, treat as checkbox
#         if hasattr(w, "setChecked"):
#             return "setChecked"
#         return "setValue" if hasattr(w, "setValue") else "setText"

#     def _getter(self, w):
#         # If it has isChecked method, treat as checkbox
#         if hasattr(w, "isChecked"):
#             return "isChecked"
#         return "value" if hasattr(w, "valueChanged") else "text"

#     def _signal(self, w):
#         # If it has stateChanged signal, treat as checkbox
#         if hasattr(w, "stateChanged"):
#             return w.stateChanged
#         return w.valueChanged if hasattr(w, "valueChanged") else w.textChanged

#     def load(self):
#         for key, widget, cast, default in self.fields:
#             if not widget:
#                 continue
#             try:
#                 val = self.settings.value(key, default)
#                 # Check if widget uses checked state
#                 if hasattr(widget, "setChecked") and hasattr(widget, "isChecked"):
#                     val = val in ("true", "1", 1, True)
#                 else:
#                     val = cast(val)
#                 getattr(widget, self._setter(widget))(val)
#             except Exception as e:
#                 print(f"[Load error] {key}: {e}")

#     def connect_autosave(self):
#         for key, widget, *_ in self.fields:
#             if not widget:
#                 continue
#             try:
#                 sig = self._signal(widget)
#                 getter = getattr(widget, self._getter(widget))
#                 sig.connect(lambda _, w=widget, k=key, g=getter: self.settings.setValue(k, g()))
#             except Exception as e:
#                 print(f"[Connect error] {key}: {e}")


class SettingsHandler:
    def __init__(self, fields, target=None, org="MyCompany", app="MyApp"):
        self.fields = fields
        self.target = target
        self.settings = QSettings(org, app)
        self.load()
        self.connect_autosave()

    def reset_settings(self):
        self.settings.clear()
        self.load()
        


    def __repr__(self):
        lines = []
        for key, widget, cast, default in self.fields:
            try:
                setting_val = self.settings.value(key, default)
                attr_val = getattr(self.target, key, None) if self.target else None
                lines.append(f"{key}: QSettings='{setting_val}' | target.{key}='{attr_val}'")
            except Exception as e:
                lines.append(f"{key}: ERROR reading values: {e}")
        return "<SettingsHandler>\n" + "\n".join(lines)

    def _setter(self, w):
        if hasattr(w, "setChecked"):
            return "setChecked"
        return "setValue" if hasattr(w, "setValue") else "setText"

    def _getter(self, w):
        if hasattr(w, "isChecked"):
            return "isChecked"
        return "value" if hasattr(w, "valueChanged") else "text"

    def _signal(self, w):
        if hasattr(w, "stateChanged"):
            return w.stateChanged
        return w.valueChanged if hasattr(w, "valueChanged") else w.textChanged

    def load(self):
        for key, widget, cast, default in self.fields:
            if not widget:
                continue
            try:
                val = self.settings.value(key, default)
                if hasattr(widget, "setChecked") and hasattr(widget, "isChecked"):
                    val = val in ("true", "1", 1, True)
                else:
                    val = cast(val)
                getattr(widget, self._setter(widget))(val)
                # Set target attribute on load too
                if self.target:
                    setattr(self.target, key, val)
            except Exception as e:
                print(f"[Load error] {key}: {e}")

    def connect_autosave(self):
        for key, widget, *_ in self.fields:
            if not widget:
                continue
            try:
                sig = self._signal(widget)
                getter = getattr(widget, self._getter(widget))
                sig.connect(lambda _, w=widget, k=key, g=getter: self._on_change(k, g))
            except Exception as e:
                print(f"[Connect error] {key}: {e}")

    def _on_change(self, key, getter):
        try:
            val = getter()
            print(f"[DEBUG] _on_change: key='{key}', new value='{val}'")
            self.settings.setValue(key, val)
            if self.target:
                print(f"[DEBUG] Setting attribute '{key}' on target to '{val}'")
                setattr(self.target, key, val)
        except Exception as e:
            print(f"[ERROR] _on_change failed for key='{key}': {e}")


