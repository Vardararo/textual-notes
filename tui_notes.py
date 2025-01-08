'''Note-taking app created using Textual framework'''

from textual.app import App, on
from textual.widgets import Header, Footer, Button, Label, DataTable, Static, Input
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
        self.theme = "nord"

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
            Button("Clear All", variant="error", id="clear_all"),
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

    @on(Button.Pressed, "#add")
    def action_add(self):
        '''Add a new note'''

        def check_note(data):
            if data:
                self.db.add_new_note(data)
                note_id, *note = self.db.get_last_note()
                self.query_one(DataTable).add_row(*note, key=note_id)
        self.push_screen(InputDialog(), check_note)

    @on(Button.Pressed, "#delete")
    def action_delete(self):
        '''Delete a single note'''

        notes_list = self.query_one(DataTable)
        row_key, _ = notes_list.coordinate_to_cell_key(notes_list.cursor_coordinate)

        def check_answer(accepted):
            if accepted and row_key:
                self.db.delete_note(note_id=row_key.value)
                notes_list.remove_row(row_key)

        note_title = notes_list.get_row(row_key)[0]
        self.push_screen(
            QuestionDialog(f"Do you want to delete {note_title}?"), check_answer
        )

    @on(Button.Pressed, "#clear_all")
    def action_delete_all(self):
        '''Remove all notes from the database and the app'''

        def check_answer(accepted):
            if accepted:
                self.db.clear_all_notes()
                self.query_one(DataTable).clear()

        self.push_screen(
            QuestionDialog("Do you want to remove all notes?"), check_answer
        )

    def action_toggle_dark(self):
        """An action to toggle dark mode."""
        self.theme = (
            "nord" if self.theme == "solarized-light" else "solarized-light"
        )

    @on(Button.Pressed, "#request_quit")
    def action_request_quit(self):
        '''Quit application'''

        def check_answer(accepted):
            if accepted:
                self.exit()

        self.push_screen(QuestionDialog("Do you want to quit?"), check_answer)

class InputDialog(Screen):
    '''Dialog screen for new notes'''

    def compose(self):
        yield Grid(
            Label("Add Note", id="title"),
            Label("Name:", classes="label"),
            Input(
                placeholder="Note Title",
                classes="input",
                id="note",
            ),
            Label("Text:", classes="label"),
            Input(
                placeholder="Input text",
                classes="input",
                id="text",
            ),

            Static(),
            Button("Cancel", variant="warning", id="cancel"),
            Button("Ok", variant="success", id="ok"),
            id="input-dialog",
        )

    def on_button_pressed(self, event):
        '''Dialog for adding new notes'''

        if event.button.id == "ok":
            title = self.query_one("#note", Input).value
            text = self.query_one("#text", Input).value
            self.dismiss((title, text))
        else:
            self.dismiss(())


class QuestionDialog(Screen):
    '''Prompts a confirmation dialog'''

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
