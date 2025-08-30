from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import * 

from PyQt6.QtGui import *

import inspect
import traceback
import sys
import json
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
WIDGET_CAPS = {
    QCheckBox: (
        # getter
        lambda w: w.isChecked(),
        # setter
        lambda w, v: w.setChecked(str(v).lower() in ("true", "1")),
        # signal
        lambda w: w.stateChanged,
    ),

    QSpinBox: (
        lambda w: w.value(),
        lambda w, v: w.setValue(int(v)),
        lambda w: w.valueChanged,
    ),

    QDoubleSpinBox: (
        lambda w: w.value(),                  # getter
        lambda w, v: w.setValue(float(v)),    # setter
        lambda w: w.valueChanged,             # signal
    ),

    QLineEdit: (
        lambda w: w.text(),
        lambda w, v: w.setText(str(v)),
        lambda w: w.textChanged,
    ),

    QComboBox: (
        # getter returns JSON string with items + index
        lambda w: json.dumps({
            "items": [w.itemText(i) for i in range(w.count())],
            "index": w.currentIndex(),
        }),
        # setter restores items + index
        # lambda w, v: (
        #     (lambda data: (
        #         w.clear(),
        #         w.addItems(data.get("items", [])),
        #         w.setCurrentIndex(
        #             data.get("index", 0)
        #             if 0 <= data.get("index", 0) < len(data.get("items", []))
        #             else 0
        #         )
        #     ))(json.loads(v) if isinstance(v, str) else v)
        # ),
        lambda w, v: (
            (lambda data: (
                w.clear(),
                w.addItems(data.get("items", [])),
                w.setCurrentIndex(
                    data.get("index", 0)
                    if 0 <= data.get("index", 0) < len(data.get("items", []))
                    else (0 if len(data.get("items", [])) > 0 else -1)
                )
            ))(json.loads(v) if isinstance(v, str) else v)
        ),
        lambda w: w.currentIndexChanged,
    ),
    # QComboBox: (
    #     # getter returns (items_list, current_index)
    #     lambda w: ([w.itemText(i) for i in range(w.count())], w.currentIndex()),
    #     # setter takes (items_list, index)
    #     lambda w, v: (
    #         w.clear(),
    #         w.addItems(v[0] if v and len(v) > 0 else []),
    #         w.setCurrentIndex(v[1] if v and len(v) > 1 else 0)
    #     ),
    #     # signal
    #     lambda w: w.currentIndexChanged,
    # ),
    
    # QComboBox: (
    #     # getter returns dict with items and index
    #     lambda w: {
    #         "items": [w.itemText(i) for i in range(w.count())],
    #         "index": w.currentIndex()
    #     },
    #     # setter expects dict with 'items' list and 'index'
    #     lambda w, v: (
    #         w.clear(),
    #         w.addItems(v.get("items", [])),
    #         w.setCurrentIndex(v.get("index", 0))
    #     ),
    #     # signal
    #     lambda w: w.currentIndexChanged,
    # ),

    QFileSystemModel : (
        # getter
        lambda m: m.rootPath(),
        # setter
        lambda m, v: m.setRootPath(str(v)),
        # signal
        lambda m: m.rootPathChanged,
        ),
}

class SettingsHandler:
    def __init__(self, fields, target, org="MyCompany", app="MyApp"):

        caller_frame = inspect.currentframe().f_back
        self._origin_filename = caller_frame.f_code.co_filename
        self._origin_lineno = caller_frame.f_lineno

        # caller = inspect.currentframe().f_back
        # filename = caller.f_code.co_filename
        # lineno = caller.f_lineno

        # # --- Validate target ---
        # if target is None:
        #     raise ValueError("SettingsHandler requires a target object for attribute syncing.")
        # if not hasattr(target, "__dict__"):
        #     raise TypeError("Target must be a normal Python object with attributes.")
        # self.target = target

        # # --- Validate fields ---
        # if not isinstance(fields, (list, tuple)):
        #     raise TypeError("fields must be a list or tuple.")
        # if not fields:
        #     raise ValueError("fields list is empty.")
        
        # for i, field in enumerate(fields):
        #     if not isinstance(field, (list, tuple)) or len(field) != 4:
        #         raise ValueError(
        #             f"Field #{i} is invalid — expected tuple of (key, widget, cast, default), got: {field}"
        #         )
            
        #     key, widget, cast, default = field

        #     if not isinstance(key, str):
        #         raise TypeError(f"Field #{i} key must be a string, got {type(key).__name__}: {key!r}")

        #     if widget is None:
        #         raise ValueError(f"Field #{i} ('{key}') has no widget assigned.")

        #     if not callable(cast):
        #         raise TypeError(f"Field #{i} ('{key}') cast must be callable, got {type(cast).__name__}")

        #     if not hasattr(target, key):
        #         raise RuntimeError(
        #             f"SettingsHandler: Field #{i} ('{key}') missing on target.\n  File \"{self._origin_filename}\", line {self._origin_lineno}"
        #         ) from None


        

        # # --- Validate org / app ---
        # if not isinstance(org, str) or not org.strip():
        #     raise ValueError("org must be a non-empty string.")
        # if not isinstance(app, str) or not app.strip():
        #     raise ValueError("app must be a non-empty string.")
        self.target = target
        self.fields = fields
        self.settings = QSettings(org, app)
        self.load()
        self.connect_autosave()

    def reset_settings(self):
        self.settings.clear()
        self.load()

    def _raise_field_error(self, msg):
        """Raise error with wrapper + actual error location"""
        full_msg = (
            f"{msg}\n"
            f"File \"{self._origin_filename}\", line {self._origin_lineno}"
        )
        raise RuntimeError(full_msg) from None

    def __repr__(self):
        lines = []
        for key, widget, default in self.fields:
            try:
                setting_val = self.settings.value(key, default)
                attr_val = getattr(self.target, key, None) if self.target else None
                lines.append(f"{key}: QSettings='{setting_val}'[{type(setting_val)}] | target.{key}='{attr_val}':[{type(setting_val)}]")
            except Exception as e:
                lines.append(f"{key}: ERROR reading values: {e}")
        return "<SettingsHandler>\n" + "\n".join(lines)

    def widget_caps(self, widget):
        for cls, caps in WIDGET_CAPS.items():
            if isinstance(widget, cls):
                return caps
            
        if all(hasattr(widget, name) for name in ("value", "setValue", "valueChanged")):
            return (
                lambda w: w.value(),
                lambda w, v: w.setValue(v),
                lambda w: w.valueChanged,
            )
        raise RuntimeError(f"No widget capabilities for {type(widget).__name__}")


    def load(self):
        for key, widget, default in self.fields:
            try:
                getter, setter, _ = self.widget_caps(widget)
                val = self.settings.value(key, default)
                setter(widget, val)
                # print(f"[DEBUG] [LOAD] | {key}={widget} | setter={setter} |  saved-val={val} |")
                setattr(self.target, key, val)
            except Exception as e:
                self._raise_field_error(f"[Load error] {key}: {e}")


    def connect_autosave(self):
        for key, widget, *_ in self.fields:
            try:
                getter, _, signal = self.widget_caps(widget)
                signal(widget).connect(lambda _, k=key, w=widget, g=getter: self._on_change(k, w, g))
                # print(f"[DEBUG] [AUTOSAVE CONNECTED] | {key}={widget} | SIGNAL={signal} |")
            except Exception as e:
                self._raise_field_error(f"[Connect error] {key}: {e}")


    def _on_change(self, key, widget, getter):
        try:
            val = getter(widget)
            self.settings.setValue(key, val)
            setattr(self.target, key, val)
            # print(f"[DEBUG] [_on_change] '{key}' of object {widget} set to '{val}' with getter={getter}")
        except Exception as e:
            self._raise_field_error(f"[_on_change failed] {key}: {e}")




    

    # def _setter(self, w):
    #     if hasattr(w, "setChecked"):
    #         return "setChecked"
    #     if hasattr(w, "setValue"):
    #         return "setValue"
    #     if hasattr(w, "setText"):
    #         return "setText"
    #     if hasattr(w, "setCurrentIndex"):
    #         return "setCurrentIndex"
    #     self._raise_field_error(f"No compatible setter found inside {type(w).__name__} ")


    # def _getter(self, w):
    #     if hasattr(w, "isChecked"):
    #         return "isChecked"
    #     if hasattr(w, "valueChanged"):
    #         return "value"
    #     if hasattr(w, "text"):
    #         return "text"
    #     if hasattr(w, "currentIndex"):
    #         return "currentIndex"
    #     self._raise_field_error(f"No compatible getter found inside {type(w).__name__}")

    # def _signal(self, w):
    #     if hasattr(w, "stateChanged"):
    #         return w.stateChanged
    #     if hasattr(w, "valueChanged"):
    #         return w.valueChanged
    #     if hasattr(w, "textChanged"):
    #         return w.textChanged
    #     if hasattr(w, "currentIndexChanged"):
    #         return w.currentIndexChanged
    #     self._raise_field_error(f"No compatible signal found inside {type(w).__name__}")
    
    # def load(self):
    #     for key, widget, cast, default in self.fields:
    #         if not widget:
    #             # print(f"1[DEBUG-LOAD] - key={key} |cast={cast} | widget={widget} | default={default} | {repr(widget)}")
    #             continue
    #         try:
    #             # print(f"2[DEBUG-LOAD] - key={key} |cast={cast} | widget={widget} | default={default} | {repr(widget)}")
    #             if isinstance(widget, QComboBox):
    #                 items, default_idx = default if isinstance(default, (list, tuple)) else ([], 0)

                        
    #                 saved_items = self.settings.value(f"{key}_items", items)
    #                 idx = int(self.settings.value(f"{key}_index", default_idx))


    #                 if self.target:
    #                     setattr(self.target, key, saved_items)
    #                     setattr(self.target, f"{key}_index", idx)



    #             else:
    #                 # print(f"3[DEBUG-LOAD] - key={key} |cast={cast} | widget={widget} | default={default} | {repr(widget)}")
    #                 val = self.settings.value(key, default)
    #                 if hasattr(widget, "setChecked") and hasattr(widget, "isChecked"):
    #                     val = val in ("true", "1", 1, True)
    #                 else:
    #                     val = cast(val)
    #                 getattr(widget, self._setter(widget))(val)
    #                 # Set target attribute on load too
    #                 if self.target:
    #                     setattr(self.target, key, val)
    #         except Exception as e:
    #             # print(f"[Load error] {key}")
    #             self._raise_field_error(f"[Load error] with {key}:\n{e}")

    # # def connect_autosave(self):
    # #     for key, widget, *_ in self.fields:
    # #         if not widget:
    # #             continue
    # #         try:
    # #             sig = self._signal(widget)
    # #             getter = getattr(widget, self._getter(widget))
    # #             sig.connect(lambda _, w=widget, k=key, g=getter: self._on_change(k, g))
    # #         except Exception as e:
    # #             # print(f"[Connect error] with {key}: {e}")
    # #             self._raise_field_error(f"[Connect error] {key}: {e}")

    # # def _on_change(self, key, getter):
    # #     try:
    # #         val = getter()
    # #         print(f"[DEBUG] _on_change: key='{key}', new value='{val}'")
    # #         self.settings.setValue(key, val)
    # #         if self.target:
    # #             # print(f"[DEBUG] Setting attribute '{key}' on target to '{val}'")
    # #             setattr(self.target, key, val)
    # #     except Exception as e:
    # #         # print(f"[ERROR] _on_change failed '{key}': {e}")
    # #         self._raise_field_error(f"[_on_change failed] {key}: {e}")


    # def connect_autosave(self):
    #     for key, widget, cast, default in self.fields:
    #         try:
                
    #             sig = self._signal(widget)
    #             print(f"[DEBUG] [AUTOSAVE CONNECTED] | {key}={widget} | SIGNAL={sig} |")

    #             sig.connect(lambda: self._on_change(key, widget))
    #         except Exception as e:
    #             self._raise_field_error(f"[Connect error] {key}: {e}")


    # def _on_change(self, key, widget):
    #     try:
    #         # if ):

    #         #     self.settings.setValue(f"{key}_items", ",".join(items))
    #         #     self.settings.setValue(f"{key}_index", idx)
    #         #     if self.target:
    #         #         print(f"[DEBUG] Setting attribute '{key}' on target idx:{idx} with items: {items}")
    #         #         setattr(self.target, key, items)
    #         #         setattr(self.target, f"{key}_index", idx)
    #         # else:
    #         try:
    #             getter_name = self._getter(widget)
    #             if not isinstance(getter_name, str):
    #                 raise TypeError(f"_getter must return a string, got {type(getter_name).__name__}")

    #             getter = getattr(widget, getter_name)

    #         except AttributeError as e:
    #             self._raise_field_error(f"[_on_change failed] {key}: Widget has no attribute '{getter_name}' ({e})")

    #         except TypeError as e:
    #             self._raise_field_error(f"[_on_change failed] {key}: {e}")

    #         except Exception as e:
    #             self._raise_field_error(f"[_on_change failed] {key}: Unexpected error during getter resolution: {e}")

    #         try:
    #             val = getter() if callable(getter) else getter
    #         except Exception as e:
    #             self._raise_field_error(f"[_on_change failed] {key}: Error calling getter '{getter_name}': {e}")

    #         self.settings.setValue(key, val)

    #         if self.target:
    #             print(f"[DEBUG] [_on_change] | {key}={widget} | getter={getter} | val={val}|")
    #             setattr(self.target, key, val)
    #     except Exception as e:
    #         self._raise_field_error(f"[_on_change failed] {key}: {e}")