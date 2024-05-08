# Maya Polar Cord Tool
## Introduction:
This is a tool I developed to help with the placing and moving of objects in polar cordinate space

## What this plugin does
<img src = assets\Example2.png width = 550> 

This plugin converts 3D polar cords and creates a cube on cartesian 3D space

<img src = assets/istallDirectory.png width = 600> 

## How to Install
* download and unzip the plugin to the maya script folder, it should look like this:

* Drag the install.mel to maya's viewport





# Instructions:

> [!NOTE]
> This is only a tool meant for maya and the math has been made for maya specificly since the z and x axis are swiched normally when using actuall math.

<img src = assets\Example.png width = 400> 

 What do the values mean?

* The Radial Cordinate is the r Value which is the radius.

* The Polar Value is the vertical angle from the Y axis.

* The Alpha is the horizontal angle from the Z axis.

* The Rotation Radial Value is the r value which is the radius.

* The Rotation Polar Value is the Vertical angle from the Y axis.

* The Rotation Alpha Value is the horizontal angle from the Z axis.

* The Geo Size is the size of the geo when created.

* The Color Change Check Box when checked updates the material with a new color and if unchecked will not do anything with the material at all.

* The Color Button once clicked will open a colorpicker to pick what color you want the mesh to be.

* The Update Polar Cords Button is what updates or cretaes the geo after you have put in your values. If you have nothing selected in the scene it will create a cube by default. If you have a object selected it will move it and not delete or create anything else new it will only move the selected mesh and scale it if you want it bigger.


## How to use the tool

Select an object if you want to move and rotate a object int he scene using polar cords else don't select one.

If you don't want to change the color of the object or just want the default color when a new object is created un chekc the color change check box.

Set the values you want for the polar cords to be converted.

Select a color if you enabled the color change check box.

Finally press the Update Polar Cord Button


# Color Picker

<img src = assets\ColorPickerExample.png width = 500> 

This is what shows up when you press the color picker button. Once you pick your color and press ok the color will update and it's as simple as that. If you just want to update the color on the mesh you can just press the create geo button again to apply the color. The color shown on the button is the color that will be applied on the mesh when created.
