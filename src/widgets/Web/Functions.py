from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *

from .Layout import Layout

class Logic:
    def __init__(self, ui: Layout):
        self.ui: Layout = ui

    def change_url(self) -> None:
        url = self.ui.url_input.text()
        self.ui.eWebPage.setUrl(QUrl(url))

    def load_url(self, url):
        self.ui.eWebPage.setUrl(QUrl(url))
        script = """
        document.cookie = "subscribed=true";
        localStorage.setItem("loggedIn", "true");
        """
        
        self.ui.eWebPage.loadFinished.connect(lambda: self.ui.eWebPage.page().runJavaScript(script))

    def click_element(self, xpath):
        print(f"Clicking element with XPath: {xpath}")
        self.execute_js(xpath, "element.click")

    def change_value_element(self,xpath, new_value):
        print(f"Editing element with XPath: {xpath}")
        self.execute_js(xpath, f'element.value = "{new_value}"')

    def inject_css(self,xpath):
        # CSS string to change the background color of the webpage content
        css = "document.body.style.backgroundColor = 'black';"
        self.execute_js(xpath, css, wait=False)

        # # Wait until the page is loaded, then inject the CSS
        # webview.loadFinished.connect(inject_css)

    def disable_element(self, xpath):
        print(f"Disabling element with XPath: {xpath}")
        # execute_js(xpath, "element.disabled = true;")
        self.execute_js(xpath, "element.style.display = 'none'", wait=True)

    def highlight_element(self, xpath):
        print(f"Highlighting element with XPath: {xpath}")
        # Add style to highlight the element
        highlight_style = """
        element.style.border = "3px solid red";
        element.style.backgroundColor = "yellow";
        """
        self.execute_js(xpath, highlight_style)

    def type_text(self, xpath, text_to_type):
        print(f"Typing into element with XPath: {xpath}")
        # Use JavaScript to simulate typing
        type_script = f"""
        var element = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element && element.tagName === 'INPUT') {{
            element.value = '{text_to_type}';  // Set the text in the input field
        }}
        """
        self.execute_js(xpath, type_script)

    def get_value_at_xpath(self,xpath):
        print(f"Getting value from element with XPath: {xpath}")
        # JavaScript to get the value of an element based on XPath
        get_value_script = f"""
        var element = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {{
            return element.value || element.textContent || element.innerText || 'No value found';
        }} else {{
            return 'Element not found';
        }}
        """
        # Use the existing execute_js method to run JavaScript and pass the callback function
        self.execute_js(xpath, get_value_script)

    def execute_js(self, xpath, action_js, wait=False):
        if wait:
            script = f"""
            (function() {{
                const observer = new MutationObserver(function(mutations) {{
                    const element = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (element) {{
                        observer.disconnect();
                        {action_js}
                    }}
                }});
                observer.observe(document.body, {{
                    childList: true,
                    subtree: true
                }});
            }})();
            """
        else:
            script = f"""
            var element = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (element) {{
                {action_js};
            }}
        """
        self.ui.eWebPage.page().runJavaScript(script)

    def activate_design_mode(self):
        """
        In the console it is just 
        document.designMode = 'on';"
        """
        toggle_js = """
        document.designMode = (document.designMode === 'on') ? 'off' : 'on';
        """
        self.ui.eWebPage.page().runJavaScript(toggle_js)

    def activate_devtools(self):
        if self.ui.devtools_view.isVisible():
            self.ui.eWebPage.page().setDevToolsPage(None)
            self.ui.devtools_view.hide()
        else:
            self.ui.eWebPage.page().setDevToolsPage(self.ui.devtools_view.page())
            self.ui.devtools_view.show()
            