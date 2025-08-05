from PyQt6.QtCore import QSettings

class SettingsHandler:
    def __init__(self, obj, fields, org="MyCompany", app="MyApp"):
        self.obj = obj
        self.fields = fields
        self.settings = QSettings(org, app)

    def load(self):
        for key, attr, cast, default in self.fields:
            widget = getattr(self.obj, attr, None)
            if not widget:
                continue
            try:
                val = cast(self.settings.value(key, default))
                getattr(widget, self._setter(widget))(val)
            except Exception as e:
                print(f"[Load error] {key}: {e}")

    def connect_autosave(self):
        print("CONNECTED")
        for key, attr, *_ in self.fields:
            widget = getattr(self.obj, attr, None)
            if not widget:
                continue
            try:
                signal = self._signal(widget)
                getter = getattr(widget, self._getter(widget))
                signal.connect(lambda _, w=widget, k=key, g=getter: self.settings.setValue(k, g()))
            except Exception as e:
                print(f"[Connect error] {key}: {e}")

    def _setter(self, widget):
        return "setValue" if hasattr(widget, "setValue") else "setText"

    def _getter(self, widget):
        return "value" if hasattr(widget, "valueChanged") else "text"

    def _signal(self, widget):
        return widget.valueChanged if hasattr(widget, "valueChanged") else widget.textChanged
