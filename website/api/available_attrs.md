* `quest`:
  * `title` - string, **required for creating**
  * `tags` - array of strings
  * `hidden` - bool, **required for creating**
  * `description` - string
  * `password` - string
  * `time_open` - string...?
  * `time_close` ?
  * `lead_time` int ?
* `question`:
  * `type` - `open`, `choice`, `start`, `end`, `movement` string, "**required for creating**
  * `text` - string
  * `pos_x` - int
  * `pos_y` - int
* `hint`:
  * `text` - string, **required for creating**
  * `fine` - float
* `answer_option`:
  * `text` - string, **required for creating**
  * `points` - float
* `movement`:
  * There are no available attributes 
* `file`:
  * `type` - `image`, `video`, `audio` string, **required for creating**
  * `url` - string, **required for creating**
* `place`:
  * `coords` - array of two floats, **required for creating**
  * `radius` - float, **required for creating**
  * `time_open` - ?
  * `time_close` - ?
