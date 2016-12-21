# Python video annotator Model GUI

This library is part of [Python Video Annotator](http://pythonvideoannotator.readthedocs.io) application.

This library implements the GUI for the [Python Video Annotator Models](http://pythonvideoannotator.readthedocs.io) library.

## What are the models?

The models are classes used to organize the data within the application.

## What are the models GUI?

The Models GUI are a graphical user interface to manage the models objects.

### Data and models structure

```
+ Project (model)
  + Video (model)
	+ objects (package)
	  + Object2d (model)
		+ datasets (package)
		  + Path (Model)
```

**(model)** - It means that the element in the hierarchy exists and is implemented in a class.
**(package)** - It means that the element in the hierarchy is present just as a concept and does not have any class implementing it.

| Class name | Description |
|---|---|
|[models.Project](/models/project/)| This class is responsible for manage the videos. |
|[models.video.Video](/models/video/)| This class is responsible for manage the diferent types of objects present in the video. Currently only the Object2d exists. |
|models.video.objects| This package is present just as a concept and should include all the types of objects a video can contain|
|[models.video.objects.object2d.Objects2D](/models/object2d/)| This class is responsible for manage the object datasets. Currently only the path dataset is implemented|
|models.video.objects.object2d.datasets| This package is present just as a concept and should include all types of dataset that an object has.|
|[models.video.objects.object2d.datasets.path.Path](/models/path/)| Implementation of the object path dataset.|