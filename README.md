PCLite
======

Alternate Package Control for Sublime Text 3

Installing
----------

Clone the repository in your Sublime Text "Packages" directory:

    git clone https://github.com/PCLite/PCLite.git


The "Packages" directory is located at:

* OS X: `~/Library/Application Support/Sublime Text 3/Packages/`

* Linux: `~/.config/sublime-text-3/Packages/`

    * Note: SSL is currently not enabled in ST3 for Linux. In this case PCLite uses `wget` to download instead. Make sure it's installed. For Ubuntu that's: `sudo apt-get install wget`

* Windows: `%APPDATA%/Sublime Text 3/Packages/`

Functions
---------
* Install: Installs packages from the main Package Control repository. Some packages may not work because there is currently no way to filter out ST2 only packages.
* Remove: Removes packages previously installed by PCLite.

Why?!
-----
The original Package Control works well. Why make another? The goal is to mimic Package Control's specification, but with a fresh look at its architecture. Also, by using only Python 3 I'm hoping to leverage the new features to make a more readable and maintainable code base. Here are some of the enhancements I've made:

* Tests: PCLite has a built-in test suite that is automatically run if debug mode is enabled. Tests are essential for any large program. Without them the code can break in unexpected ways which makes it hard to maintain.
* Threading with futures: PCLite uses a more modern threading model. Package Control uses raw threads to do HTTP requests and disk IO. While this works for a small program, threads can get messy quickly. PCLite uses the notion of Executors or Thread Pools to manage long running tasks. There's even a handy @async decorator that will turn any function into an asynchronous function. It will return a result to a supplied callback. Concurrency is hard, we need to make it as easy as we can.
* Libraries: PCLite embraces the use of libraries. The main downloader uses Requests which reduces all the complicated HTTP/HTTPS logic to a simple get() method. On platforms that do not support Requests other methods are used (like `wget`).
* Logging: By using Python's built in Logging library PCLite gets flexible, semantic logging for free. When in debug mode all logs show what file and line they came from, turn off debug and messages are clean and user friendly.
* Statuses: With the status module PCLite can set the status text from anywhere in the program. Status messages are also linked with the logging system so the user has a history of what was said. A status message can be a regular message, an error, or displayed with an animated 'loading' display. Regular and error messages go away after a set time. Loading statuses are stopped by calling stop() on the returned object.
* Settings: PCLite has a global settings module. This reduces code since the settings object does not have to be passed around everywhere. For instance every module has access to settings.isDebug() to execute special debug only functions.
* Exceptions: A lot can go wrong with network and disk IO. PCLite tries to fail fast and give as much error information as possible.
