'''Note-taking app created using Textual framework'''

from textual.app import App
from textual.widgets import Header, Footer


class NotesApp(App):
    def compose(self):
        yield Header()
        yield Footer()

    def on_mount(self):
        self.title = "Textual Notes"
        self.sub_title = "A Note Taking App With Textual & Python"
# End-of-file (EOF)
