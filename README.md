# RubiksCube-TwophaseSolver
## Overview 
This project implements the two-phase-algorithm in its fully developed form to solve Rubik's cube in Python. Though Python is much slower than for example C++ or even Java the implementation is sufficiently fast to solve random cubes in less than 20 moves on average on slow hardware like the Raspberry Pi3 within a few seconds.

If you just want to solve Rubik's cube and play around with its patterns [Cube Explorer](http://kociemba.org/cube.htm) may be the better choice. But if you want to get a better understanding of the two-phase-algorithm details or you work on a project to build a cube solving robot which solves the cube almost optimal this this may be the right place to look.
## Usage

The package is published on PyPI and can be installed with

```$ pip install RubikTwoPhase```

Once installed, you can import the module twophase.solver into your code:
```python
>>> import twophase.solver  as sv
```
There are several tables which must be created, but only on the first run. These need about 80 MB of disk space and it takes about 1/2 hour or even longer to create them, depending on the hardware.
But only with these computational relative expensive tables the algorithm works highly effective and usually will find near optimal solutions.

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

If you want to spend a constant of time t for each solve and just return the shortest maneuver found in this time t, do
```python
>>> sv.solve(cubestring,0,t)
```
You can test the performance of the algorithm on your machine with something similar to
```python
>>> import twophase.performance as pf
>>> pf.test(100,0.3)
```
This will for example generate 100 random cubes, solves each in 0.3 s and displays a statistics about the solving lengths.   

You also have the possibility to solve a cube not to the solved position but to some favorite pattern represented by goalstring.

```python
>>> sv.solveto(cubestring,goalstring,20,0.1)
```
will grant for example 0.1 s to find a solution with <= 20 moves.   

***

Another feature is to locally start a server which listens on a port of your choice. It accepts the cube definition string and returns the solution.
```python
>>> import twophase.server as srv
>>> srv.start(8080, 20, 2)
```
Alternatively start the server in background:
```python
>>> import twophase.start_server as ss
>>> from threading import Thread
>>> bg = Thread(target=ss.start, args=(8080, 20, 2))
>>> bg.start()
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
>>> import twophase.client_gui
```
![](gui_client.jpg "")
***


The following module is experimental. It uses the OpenCV package which eventually has to be installed with   
```$ pip install opencv-python```  
You also need the numpy package which can be installed with   
```$ pip install numpy```   

The webserver has to run and a webcam must be connected to the client.
```python
>>> import twophase.computer_vision
```

You have the possibility to enter the facelet colors with a webcam. There are several parameters which have an influence on the facelet detection quality.  If you use a Raspberry Pi with the Raspberry Pi Camera Module  and not an USB-webcam make sure you do "sudo modprobe bcm2835-v4l2" first. 

You can find some more information how to set the parameters here:
[Computer vision and Rubik's cube](http://kociemba.org/computervision.html)

***

## Performance

We solved 1000 random cubes in different scenarios. All computations were done on a Windows 10 machine with an
AMD Ryzen 7 3700X 3.59 GHz.   
We distinguish between computations with the standard CPython interpreter and computation with PyPy (pypy3) which
includes a Just-in-Time compiler which gives a speedup by a factor of about 10.

test(1000, t) generates 1000 random cubes, the computing time for each cube is t seconds. The distribution of the
solving lengths also is given.

#### Standard CPython
test(1000,30): {14: 0, 15: 2, 16: 12, 17: 74, 18: 279, 19: 534, 20: 99, 21: 0}, average 18.63 moves  
test(1000,10): {14: 0, 15: 1, 16: 8, 17: 51, 18: 242, 19: 532, 20: 166, 21: 0}, average 18.79 moves  
test(1000,1): {14: 0, 15: 2, 16: 4, 17: 28, 18: 127, 19: 401, 20: 405, 21: 33, 22: 0}, average 19.27 moves  
test(1000,0.1): {15: 0, 16: 2, 17: 6, 18: 46, 19: 186, 20: 451, 21: 293, 22: 16, 23: 0}, average 20.02 moves  

#### PyPy (pypy3) with Just-in-Time compiler
test(1000,10): {14: 0, 15: 1, 16: 11, 17: 100, 18: 423, 19: 433, 20: 32, 21: 0}, average 18.37 moves  
test(1000,1): {14: 0, 15: 1, 16: 10, 17: 49, 18: 259, 19: 535, 20: 145, 21: 1, 22: 0}, average 18.76 moves  
test(1000,0.1): {15: 0, 16: 4, 17: 23, 18: 100, 19: 429, 20: 401, 21: 43, 22: 0}, average 19.33 moves  
test(1000,0.01): {16: 0, 17: 1, 18: 25, 19: 95, 20: 349, 21: 461, 22: 69, 23: 0}, average 20.45 moves  


To achieve an average of less than 19 moves a computing time of 10 s in case of CPython or 1 s in case of PyPy is
sufficient. If you are satisfied with an average of 0.5 moves more a computation time of 1 s with CPython and 0.1 s
with PyPy is sufficient.   