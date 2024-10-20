from model.note_storage import NoteStorage
from controller.note_controller import NoteController
from view.gui_view import GUIView

if __name__ == "__main__":
    storage = NoteStorage()  
    controller = NoteController(storage) 
    gui = GUIView(controller)  
    gui.run()  
