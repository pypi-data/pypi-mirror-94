# ProtoDriver
A simple Raspberry Pi web api for driving a MAX7219 dot matrix display

This package is meant to be ran as a REST API and be called from a dedicated frontend.

ProtoDriver has only just been brought to a usable level and is in no way production ready.

## API calls

***

### /ping - GET
* A simple test call to see if the server is reachable
* Returns JSON data with the word "Pong"

### /uploadimage/< filename > - POST
* Used to pass image data in the form of bytes to the server
* filename is passed including the files extension and will be used to write the new file

### /updateimage/< filename > - PUT
* used in the same way as uploadimage but with the intent of overwriting an existing file with new data
* filename is passed including the files extension and will be used to overwrite an existing file with that name

### /deleteimage/< filename > - DELETE
* used to delete a file from the server
* filename is passed including the files extension and will be used to delete an existing file with that name

### /getimage/< filename > - GET
* used to get the contents of an image from the server
* filename is passed including the files extension and will be used to target an existing file with that name

### /getallimages - GET
* returns the contents of all images currently stored on the server paired with their filenames
* [ filename , file data]

###/displayimage/< filename > - GET
* used to display an image on the led matrix
* filename is passed including the files extension and will be used to target an existing file with that name


###/cleardisplay - GET
* clears the led matrix
