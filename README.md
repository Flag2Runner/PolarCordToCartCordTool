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

<img src = assets\Example.png width = 300> 

 What do the values mean?

* The Radial Cordinate is the r Value which is the distance from the origin of the world or radius.

* The Polar Value is the vertical angle from the Y axis

* The Alpha is the horizontal angle from the Z axis

* The Geo Size is the size of the geo when created

* The Color Button once clicked will open a colorpicker to pick what color you want the mesh to be

* The Create Geo Button is what creates the geo after you have put in your values.
It will delete the old mesh when pressed or anything called 'cube' before creating the new cube.

# Color Picker

<img src = assets\ColorPickerExample.png width = 500> 

This is what shows up when you press the color picker button. Once you pick your color and press ok the color will update and it's as simple as that if you just want to update the color on the mesh you can just press the create geo button again to apply the color. The color shown on the button is the color that will be applied on the mesh when created.
