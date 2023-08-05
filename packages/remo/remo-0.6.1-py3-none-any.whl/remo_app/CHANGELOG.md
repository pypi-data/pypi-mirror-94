# Changelog

Here we list the history of changes in Remo across the various releases.


## Coming up in the next releases

This is a general plan on what we are working on next. If you have any feedback or preference, we would love to hear them in our discuss forum.

**1. Improved dataset experience**

Including a list view for images details and folders to organise your images.

**2. Faster processing**

- Improved uploading of thousands of annotations at once

**3. Increase supported formats and tasks**

- DICOM
- Pose Estimation or Semantic Segmentation up next, if we have enough requests

---

## v0.6.0 - 5 Feb 21

Thanks to the support from our friends at [Apeel Sciences](https://www.apeel.com/) who have sponsored the initiative, we are introducing a settings section for dataset, featuring option to sort classes in the annotation tool page (with the ability to add more settings in the future). 

For the rest, we issuing a bug fix to enable export annotations files with images filepath when using Remo from the browser (thanks to Matt who reported it).


---

## v0.5.9 - 15 Jan 21
ure
Issuing a bug fix to shortcuts behaviour within the annotation tool. 
After annotating a picture, the class-hotkey binding used to change on each picture to match the sorting of objects count. We now keep the binding constant within an annotation set.

---

## v0.5.8 - 09 Jan 21

**Bug fixes**

- Fixed uploading CSV files on Windows
- Fixed on hover message on the annotation tool
- Fixed Team page view

---

## v0.5.7 - 20 Nov 20

We are finally introducing a Docker installation for Remo! We are also releasing some changes that make Remo more flexible and a paid Team version.

**Features**

- Installation via Docker is now supported. Among other things, this allows to have a PostgreSQL server running remotely for increased reliability
- Releasing a new pip package for remo-python. Main improvement: search function inside a dataset now works
- Improved documentation across the board
- We have removed limitations to the IP address where you can serve Remo
- Paid Team version of Remo is now available

**Bug fixes**

- Deleting specific images at times failed. This is now fixed

---

## v0.5.4 - 24 Oct 20

Fixed a bug in the dataset page where scrolling with a filter applied did not display all the pictures correctly. Thanks to Richard for reporting it!

---

## v0.5.3 - 23 Oct 20

This release includes some minor optimization and a bug fix. Specifically:


* We optimized load time to count images in annotation export form
* Fixed a bug where we couldn't delete a dataset that had some broken images inside (this issue was affecting our demo too)


---

## v0.5.2 - 6 Oct 20

We are issuing a fix for the registration process we introduced in v0.5, and introducing the ability to export annotations based on filtering by image tag

**Features**

* Now you can export annotations for a selection on images based on filters by image tags

**Bug fixes**

* Fixed upload instance segmentation annotations in CSV format
* Fixed token validation

---

## v0.5.0 - 30 Sep 20

In this major release, we are introducing a breakdown by tags on annotation statistics, and our user registration module. We have also greatly reduced the size of the wheel, which is now about 14 MB (30% of its previous size).

**Features**

* For an annotation set, you can now break down statistics by image tags. Among other things, this allows to easily visualize the distribution of objects and images in train/test splits
* We have added a user registration module. You may now verify your email and register your free token to enjoy unrestricted access to remo.

**Optimizations**

* Reduced the size of distribution pip package from 50 MB to 14 MB

---

## v0.4.24 - 18 Sep 20

This release contains fixes to our notification system.

**Bug fixes**

* Cancel on the upload sessions persisted on the view after being closed.
* When starting an upload, there was a case when the upload statistics arent displayed and the page is cropped from the top.

---

## v0.4.23 - 16 Sep 20

In this release, we are adding persistance of active upload sessions and a shortcut to delete objects in the annotation tool (thanks to user Om for the feedback).

**Features**

* On annotation tool, you can now use the Delete or Backspace key to delete the selected annotation object, without a Delete confirmation form

**Optimizations**

* We are improving the notification system experience. Notifications are now persistent, so you will not lose any of active upload session details in case you close the tab or reload the page. And you will be able to watch status of all active uploads
* In case of failure to access our online demo, we have added a fail-safe view that allows you to access the demo with a button click

**Bug fixes**

* On dataset view, classes and tags from different annotation sets now have colours matching that of the corresponding annotation set
* Dropdown to select annotation sets was overflowing from the page

---

## v0.4.20 - 4 Sep 20

Releasing some minor UI optimization.

---

## v0.4.19 - 2 Sep 20

Adding a tutorial for Object Detection in PyTorch, and fixing a bug that prompted the user for login in browser

* Added PyTorch Object Detection tutorial
* Bug fix: login issue

---

## v0.4.18 - 28 Aug 20

We are moving the discuss forum to [discuss.remo.ai](https://discuss.remo.ai) and doing some small optimization.

**Improvements**

* Added keyboard left/right navigation on Image view
* Optimized screen for Create annotation set page


**Bug fixes**

* Fixed issue where Remo would lose connection to the db when laptop went in sleep or hibernate mode
* Fixed some UI issues around display of boxes, labels and tags on Image view and dataset page

---

## v0.4.17 - 24 Aug 20

Quite a big release, as we are introducing a number of improvements and features.
We are now supporting [Remo on Google Colab](https://remo.ai/docs/colab/), we are showing how to integrate Remo with PyTorch, and we are further improving on the Datasets upload and browsing experience.

**Features and Improvements**

* [Remo on Google Colab](https://remo.ai/docs/colab/): now you can embed and run Remo entirely on Colab servers, including backing up data on GDrive.
* Remo allows upload of annotations with file paths in the filename
* Remo-python: we improved on the library and added a PyTorch image classification tutorial
* Faster upload of tags: according to our benchmarking, it has come down from 25s to 3.5s for 1k tags
* Adding upload data status: we are now showing ETA and progress % while uploading data.
* Introducing a sticky header inside a Dataset, to change filters and image size while scrolling down on the dataset
* Optimized layout for smaller screens (including Colab and Jupyter Notebook)
* Reframed the feedback modal, with more focus on feature request

**Bug fixes**

* UI on upload data: we added a file picker to link local data on Electron view
* In case of notebooks, the "add data" button was missing on dataset view

---

## v0.4.16 - 07 Aug 20

In this release, we did some optimization around search filters and annotations saving. We are also introducing a visual display for tags in dataset view.

**Improvements**

* Faster saving of annotations
* Faster dropdown menus in dataset filters (executing on the backend now)
* Visualizing tags in dataset view
* Pop up asking for confirmation when deleting an annotation object

---

## v0.4.15 - 31 Jul 20

We are introducing filters in datasets. You can filter by class, tag, image names and task. You will also be able to carry over the filters to image view.

**Features**

* Dataset filters: filter by class, tag, image names and task
* Tags can now be exported as a separate csv file

**Bug fixes**

* Duplicating a dataset resulted in some naming conflicts
* Issues with uploading tags from the Python library

---

## v0.4.14 - 24 Jul 20

Another round of small incremental improvements:

* Based on user feedback, we are not allowing to have multiple datasets with the same name (if upgrading remo, existing dataset with duplicated name will be renamed)
* Some UI fixes: improvement to object pop up in annotation tool, better handling of long annotation set names inside a Dataset, more explicit loading behaviour when remo is loading a large set of annotations

---

## v0.4.13 - 20 Jul 20

Two main changes in this release:

* Fixing a bug we introduced in a recent release - some times new annotations were not saved properly if you were quickly drawing annotations and changing images
* Renaming remo-sdk to remo-python

---

## v0.4.12 - 17 Jul 20

In this release we worked on some improvements to the annotation experience and implemented a warning notification when adding duplicate images.

**Improvements**

* Design tweaks on the classes and object menus of Image View and Annotation tool
* Annotation tool: not allowing to create objects without class
* Images uploading: Warning notification when uploading a duplicated image within a dataset
* Increased test coverage on the Front End and Backend

---

## v0.4.9 - 9 Jul 20

We are improving on the search experience from within an image, fixed some issues around PostgreSQL installation and did some minor UX improvements.

We can now search by filename and we have an autocomplete menu to speed up the search.

**Improvements**

* Image View filters: search by filename and autocomplete for faster filtering
* Datasets: made it easier to export annotations, responding to users feedback
* Annotation tool: redesigned the On Hold / To Do button

**Bug fixes**

* Postgres-10 install failed on ubuntu 20.04 as reported by user Marco
* Remo init failed on Mac with different existing version of Postgres installed
* Remo init failed when a previous config file was present and corrupted
* Remo creates new tables in dataset with local user role instead of remo role

---

## v0.4.8 - 28 Jun 20

* Fixed postgres installation issue

---

## v0.4.7 - 26 Jun 20

Most of the work on this release has been around annotations upload and export.
We are adding the ability to upload and export tags, and some nice convenience functions for annotation exporting.

* ability to add and export tags

* export annotations: functionality to include or exclude images with no annotations

* export annotations: option to append paths to filenames

* more clear counting on annotation statistics in Annotations Tab: now displaying annotated as the count of images actual having annotations

* removing truncation for long filename on dataset page

---

## v0.4.5 - 19 Jun 20

We are introducing a check for the latest version on command line, particularly useful given we are iterating quite fast.

We also fixed some small reported bugs:


* installation issues with PostgresSQL on Windows

* installation script to use pip3 instead of pip when python 2 is installed

* sort by TODO in annotation page occasionally not working

---

## v0.4.4 - 09 Jun 20

Cosmetic changes to address links behaviour and formatting in documentation and discuss forum


---
## v0.4.3 - 04 Jun 20

Some small changes:

* Fixed bug with upload folder when using electron
* Added license page

---
## v0.4.2 - 03 Jun 20

Some quick fixes post the bigger release:

* CSS on loading bar
* demo access occasional login fail
* handling of tags: now it's case insensitive

---
## v0.4.1 - 29 May 20

**Main Changes**

Most of the work has been about introducing a notification system to inform on progress for images and annotation uploading and parsing, including a detailed breakdown of any error. Nothing fancy, but a great improvement to reliability of the app.

We also expanded the Command Line Interface, allowing for more options (such as kill remo, delete datasets), and simplified the connection between the sdk and the remo server.

For the rest, we completed a series of smaller UX-driven changes to improve usability (including showing selected annotation sizes) and fixed few reported bugs.

**Breakdown**

Bug fixes:

* Delete all images from dataset causes error
* Delete an image and re-upload it: should be allowed
* Up-to-date count of images after fast deleting
* Fix download latest available electron app

Changes:

* Notification system for data upload. You can now monitor the upload of data and get a breakdown of errors that occur.
* Expanded Command Line Interface suit of options
* SDK: rework the connection with remo app and introduce clear option to connect to a remote remo server. "import remo" in conda now does not launch the server
* Annotation tool, delete object: ask for confirmation
* Image view and Annotation tool - objects height and width information

---
## v0.3.42 - 19 May 20

Quick fix to handle directories with space within their name

* Edited installation scripts to handle folder names containing a space e.g. 'C:/remo ai/script'

---

## v0.3.41 - 8 May 20

**Main Changes**

Switched to PostgresSQL for database management, instead of SQLlite. This makes the whole app more responsive and reliable.
For the rest, we implemented a number of small fixes aimed at making making remo more robust

**Breakdown**

Bug fixes:

* Fixed annotation statistics inconsistencies for image classification
* Fixed sending feedback form
* Fixed autologin in browser, and in electron after user changes password
* Fixed rename annotation set
* Fixed export annotation form - missing annotation set name
* Fixed Windows installation in conda env - pip failed to install package
* Fixed duplicate annotation objects

Changes:

* Added support for PostgresSQL as main database
* Improved duplicate annotation set flow
* After annotations uploaded - images marked as annotated
* Improved create annotation set flow
* Improved save annotations behaviour
* Improved data uploading and parsing - moved it to a separate process, which allows to use remo while long uploads are in progress
* Added ability to bulk delete annotations for an image in annotation tool
* Added ability to mark image as TODO in annotation tool
* Improved description of installation steps. Also we are now asking user for explicit permission to install PostgresSQL and additional packages
