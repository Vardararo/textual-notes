'''Entry-point script'''

from database import Database
from tui_notes import NotesApp

def main():
    '''Main function loop'''
    app = NotesApp(db=Database())
    app.run()

if __name__ == "__main__":
    main()
# End-of-file (EOF)
