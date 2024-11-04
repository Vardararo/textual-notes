'''Note-taking app created using Textual framework'''

from textual.app import App
from textual.widgets import Header, Footer, Button, Label, DataTable, Static
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import Screen


class NotesApp(App):
    '''A Textual app for note-taking'''

    CSS_PATH = "notes.tcss"
    BINDINGS = [("t", "toggle_dark", "Toggle dark mode"),
                ("q", "request_quit", "Quit"),
                ("a", "add", "Add New"),
                ("d", "delete", "Delete"),
                ("c", "clear_all", "Clear All")]
    
    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self):
        yield Header()

        notes = DataTable(classes="notes")
        notes.focus()
        notes.add_columns("Subject", "Text")
        notes.cursor_type = "row"
        notes.zebra_stripes = True

        button_panel = Vertical(
            Button("Add", variant="success", id="add"),
            Button("Delete", variant="warning", id="delete"),
            Static(classes="separator"),
            Button("Clear All", variant="error", id="clear"),
            classes="button-panel"
        )

        yield Horizontal(notes, button_panel)
        yield Footer()

    def on_mount(self):
        '''Main screen properties'''

        self.title = "Textual Notes"
        self.sub_title = "A Note Taking App With Textual & Python"
        self._load_notes()

    def _load_notes(self):
        notes_list = self.query_one(DataTable)
        for data in self.db.get_all_notes():
            note_id, *note = data
            notes_list.add_row(*note, key=note_id)

    def action_toggle_dark(self):
        self.dark = not self.dark

    def action_request_quit(self):
        def check_answer(accepted):
            if accepted:
                self.exit()
        self.push_screen(ExitDialog("Do you want to quit?", check_answer))


class ExitDialog(Screen):
    '''Prompts dialog to leave the app'''

    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def compose(self):
        no_button = Button("No", variant="primary", id="no")

        yield Grid(
            Label(self.message, id="question"),
            Button("Yes", variant="error", id="yes"), no_button, id="question-dialog",
        )

    def on_button_pressed(self, event):
        '''Check if the Yes button was pressed'''
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
# End-of-file (EOF)
