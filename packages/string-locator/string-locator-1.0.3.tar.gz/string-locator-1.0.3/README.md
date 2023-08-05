# String Locator

A simple code to find the file containing a given string inside a given path.

At times in the programming world, we might need to change a certain code but don't know which file it is in and might have to go through a huge list of files. The string locator helps the user find the desired file by entering the text and the path to the folder containing all the documents.



## Code

```
from string_locator import locator

text='import tensorflow'
path='C:/Users/admin/Desktop/test_folder

location=locator.locate(text,path)

```

## License

Copyright (c) Srirag Jayakumar

This repository is licensed under the MIT license. See LICENSE for details.