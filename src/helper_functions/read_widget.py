def read_widget_value(widget):
    if hasattr(widget, "isChecked"):
        return widget.isChecked()
    elif hasattr(widget, "value"):
        return widget.value()
    elif hasattr(widget, "text"):
        return widget.text()
    return None


def read_settings(fields):
    return {
        key: read_widget_value(widget)
        for key, widget, *_ in fields if widget
    }


def set_widget_value(widget, value):
    if hasattr(widget, "setChecked"):
        widget.setChecked(bool(value))
    elif hasattr(widget, "setValue"):
        widget.setValue(value)
    elif hasattr(widget, "setText"):
        widget.setText(str(value))


def apply_settings(fields, settings):
    for key, widget, *_ in fields:
        if widget and key in settings:
            set_widget_value(widget, settings[key])