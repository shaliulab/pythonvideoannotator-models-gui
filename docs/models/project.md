# Class models.Project([Project](http://pythonvideoannotator-models.readthedocs.io/en/latest/models/project/), [BaseWidget](http://pyforms.readthedocs.io/en/v1.0.beta/api-documentation/basewidget/))

### \_\_init\_\_(parent=None)

Constructer.
**parent** - pointer to the python video annotator main window.


## **Variables**
***************************

### self.\_parent

Pointer to the main window

### self.\_tree

Tree control where the project structure is shown.

### self.\_addvideo

Button control to add a new video.

### self.\_removevideo

Button control to remove a selected video.

## **Properties**
***************************

### mainwindow

Return the main window.

### tree

Returns the tree control.

### objects

Returns the objects of the video.


## **Functions**
***************************

### draw(frame, frame_index)

Function called to draw information on the main window player.

### player_on_click(event, x, y)

Function called by the main window when the mouse click in the image of the video player.

## **Reemplemented functions**
***************************

### \_\_add\_\_(obj)

Calls super.
If a new video is added trigger the function **added_video_event(video)** of the main window.

### \_\_sub\_\_(obj)

Calls super.
If a new video is added trigger the function **removed_video_event(video)** of the main window.

### create_video()

Factory for the video gui model.

### load(data, project_path=None)

Calls super.
Loads the timeline annotations.

### save(data, project_path=None)

Calls super.
Saves the timeline annotations.

## **Events**
***************************

### tree_item_selection_changed_event()

Event called everytime a new selection is done in the project tree.

### \_\_create_video_event()

Event called when the button add video is pressed.

### \_\_remove_video_event()

Event called when the button remove video is pressed.