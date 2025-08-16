from PyQt6.QtCore import QSettings
import inspect
import traceback
import sys
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
    def __init__(self, fields, target, org="MyCompany", app="MyApp"):

        caller_frame = inspect.currentframe().f_back
        self._origin_filename = caller_frame.f_code.co_filename
        self._origin_lineno = caller_frame.f_lineno

        # caller = inspect.currentframe().f_back
        # filename = caller.f_code.co_filename
        # lineno = caller.f_lineno

        # --- Validate target ---
        if target is None:
            raise ValueError("SettingsHandler requires a target object for attribute syncing.")
        if not hasattr(target, "__dict__"):
            raise TypeError("Target must be a normal Python object with attributes.")
        self.target = target

        # --- Validate fields ---
        if not isinstance(fields, (list, tuple)):
            raise TypeError("fields must be a list or tuple.")
        if not fields:
            raise ValueError("fields list is empty.")
        
        for i, field in enumerate(fields):
            if not isinstance(field, (list, tuple)) or len(field) != 4:
                raise ValueError(
                    f"Field #{i} is invalid — expected tuple of (key, widget, cast, default), got: {field}"
                )
            
            key, widget, cast, default = field

            if not isinstance(key, str):
                raise TypeError(f"Field #{i} key must be a string, got {type(key).__name__}: {key!r}")

            if widget is None:
                raise ValueError(f"Field #{i} ('{key}') has no widget assigned.")

            if not callable(cast):
                raise TypeError(f"Field #{i} ('{key}') cast must be callable, got {type(cast).__name__}")

            if not hasattr(target, key):
                raise RuntimeError(
                    f"SettingsHandler: Field #{i} ('{key}') missing on target.\n  File \"{self._origin_filename}\", line {self._origin_lineno}"
                ) from None


        self.fields = fields

        # --- Validate org / app ---
        if not isinstance(org, str) or not org.strip():
            raise ValueError("org must be a non-empty string.")
        if not isinstance(app, str) or not app.strip():
            raise ValueError("app must be a non-empty string.")
        self.settings = QSettings(org, app)
        self.load()
        self.connect_autosave()

    def reset_settings(self):
        self.settings.clear()
        self.load()

    # def _raise_field_error(self, msg, include_internal=False):
    #     """Raise error pointing to constructor by default, optionally include internal trace."""
    #     base_msg = f"{msg}\n  File \"{self._origin_filename}\", line {self._origin_lineno}"
    #     if include_internal:
    #         internal_tb = traceback.format_exc()
    #         raise RuntimeError(f"{base_msg}\n[Internal traceback]\n{internal_tb}") from None
    #     else:
    #         raise RuntimeError(base_msg) from None

    def _raise_field_error(self, msg):
        """Raise error with wrapper + actual error location"""
        # exc_type, exc_value, exc_tb = sys.exc_info()
        # if exc_tb is not None:
        #     while exc_tb.tb_next:
        #         exc_tb = exc_tb.tb_next
        #     exc_file = exc_tb.tb_frame.f_code.co_filename
        #     exc_line = exc_tb.tb_lineno
        # else:
        #     exc_file = self._origin_filename
        #     exc_line = self._origin_lineno
        full_msg = (
            
            f"{msg}\n"
            f"File \"{self._origin_filename}\", line {self._origin_lineno}"
        )

        # print(f"\033[91m{full_msg}\033[0m") 
        raise RuntimeError(full_msg) from None

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
        if hasattr(w, "setValue"):
            return "setValue"
        if hasattr(w, "setText"):
            return "setText"
        
        # raise AttributeError(f"No compatible setter found for {type(w).__name__}")
        self._raise_field_error(f"No compatible setter found inside {type(w).__name__} ")


    def _getter(self, w):
        if hasattr(w, "isChecked"):
            return "isChecked"
        if hasattr(w, "valueChanged"):
            return "value"
        if hasattr(w, "text"):
            return "text"
        # raise AttributeError(f"No compatible getter found for {type(w).__name__}")
        self._raise_field_error(f"No compatible getter found inside {type(w).__name__}")

    def _signal(self, w):
        if hasattr(w, "stateChanged"):
            return w.stateChanged
        if hasattr(w, "valueChanged"):
            return w.valueChanged
        if hasattr(w, "textChanged"):
            return w.textChanged
        # raise AttributeError(f"No compatible signal found for {type(w).__name__}")
        self._raise_field_error(f"No compatible signal found inside {type(w).__name__}")
    
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
                # print(f"[Load error] {key}")
                self._raise_field_error(f"[Load error] with {key}:\n{e}")

    def connect_autosave(self):
        for key, widget, *_ in self.fields:
            if not widget:
                continue
            try:
                sig = self._signal(widget)
                getter = getattr(widget, self._getter(widget))
                sig.connect(lambda _, w=widget, k=key, g=getter: self._on_change(k, g))
            except Exception as e:
                # print(f"[Connect error] with {key}: {e}")
                self._raise_field_error(f"[Connect error] {key}: {e}")

    def _on_change(self, key, getter):
        try:
            val = getter()
            print(f"[DEBUG] _on_change: key='{key}', new value='{val}'")
            self.settings.setValue(key, val)
            if self.target:
                print(f"[DEBUG] Setting attribute '{key}' on target to '{val}'")
                setattr(self.target, key, val)
        except Exception as e:
            # print(f"[ERROR] _on_change failed '{key}': {e}")
            self._raise_field_error(f"[_on_change failed] {key}: {e}")


