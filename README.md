# RubiksCube-TwophaseSolver
## Overview 
This project implements the two-phase-algorithm in its fully developed form to solve Rubik's cube in Python. Though Python is much slower than for example C++ or even Java the implementation is sufficiently fast to solve random cubes in less than 20 moves on average on slow hardware like the Raspberry Pi3 within a few seconds.

If you just want to solve Rubik's cube and play around with its patterns [Cube Explorer](http://kociemba.org/cube.htm) may be the better choice. But if you want to get a better understanding of the two-phase-algorithm details or you work on a project to build a cube solving robot which solves the cube almost optimal this this may be the right place to look.
## Usage

The package is published on PyPI and can be installed with

```$ pip install RubikTwophase``` 

```$ pip install numpy``` is necessary too if the numpy package is not installed in your environment.

Once installed, you can import the module twophase.solver into your code:
```python
>>> import twophase.solver  as sv
```
There are several tables which must be created, but only on the first run. These need about 80 MB disk space and it takes from about 1/2 to 6 hours to create them, depending on the hardware.

A cube is defined by its cube definition string. A solved cube has the string 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'.   
```python
>>> cubestring = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'
```
See https://github.com/hkociemba/RubiksCube-TwophaseSolver/blob/master/enums.py for the exact  format.
```python
>>> sv.solve(cubestring,19,2)
```
This solves the cube described by the definition string with a desired maximum length of 19 moves and  a timeout of 2 seconds. If the timeout is reached, the shortest solution computed so far is returned even if it is longer than the desired maximum length.
```python
'L3 U1 B1 R2 F3 L1 F3 U2 L1 U3 B3 U2 B1 L2 F1 U2 R2 L2 B2 (19f)'
```
U, R, F, D, L and B denote the Up, Right, Front, Down, Left and Back face of the cube. 1, 2, and 3 denote a 90°, 180° and 270° clockwise rotation of the corresponding face. 


Another possibility is to locally start a server which listens on a port of your choice and which accepts the cube definition string and returns the solution.
```python
>>> import twophase.server as srv
>>> srv.start(8080,20,2)
```
If you get a  
```Server socket created```  
```Server now listening...```
message everything seems to work fine.
In this example the server listens on port 8080, the desired maximum length is 20 moves and the timeout is 2 seconds.

You can access the server - which may run also on a remote machine - by several methods.

```http://localhost:8080/DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL```  
 with a webbrowser if the server runs on the same machine on port 8080.  

```http://myserver.com:8081/DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL```  
with a webbrowser if the server runs on the remote machine myserver.com, port 8081.  

```echo DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL | nc localhost 8080```  
with netcat, if the server runs on the same machine on port 8080.  

You also can communicate with the server with a little GUI program which allows to enter the cube definition string interactively.
```python
import twophase.client_gui
```

![](gui_client.jpg "")


The following module is experimental. It uses the OpenCV package which eventually has be installed with ```$ pip install opencv-python```.
```python
import twophase.computer_vision
```

You have the possibility to enter the facelet colors with a webcam. There are several parameters which have an influence on the facelet detection quality.  If you use a Raspberry Pi with the Raspberry Pi Camera Module  and not an USB-webcam make sure you do "sudo modprobe bcm2835-v4l2" first. 

You can find some more information how to set the parameters here:
[Computer vision and Rubik's cube](http://kociemba.org/computervision.html)
