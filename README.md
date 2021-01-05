#### Threading Example KivyMD App

> Is a basic [KivyMD](https://kivymd.readthedocs.io/en/latest/) app to test threading on Android using python [threading.Thread](https://docs.python.org/3.6/library/threading.html) library. The thread also works using [Kivy](https://kivy.org/doc/stable/) widgets.
> The app Apk is built using [buildozer](https://buildozer.readthedocs.io/en/latest/) command *buildozer android debug deploy*.
> The purpose of the app is to create a thread that updates the connection status of Android's bluetooth `RfcommSocket`.

No issues has been observed as the UI thread is updating while thread runs.

###### Tested with following versions:
* Python 3.6.9
* Kivy 1.11.1
* KivyMD 0.1.4
* Android 7.1.2 on Zebra TC25