# SpeedLib
A python library to operate Speed devices.

Currently the API has an unique backend allowing to control miniature devices like the Faller (c) Crane or DCC trains. 

Examples
--------
Controlling a Faller (c) crane model
```python
from speedlib.cranes import faller
from speedlib.cranes.faller import Crane
ip_1 = "172.17.217.217"
ip_2 = "172.17.217.217"
crane_1 = Crane()
crane_2 = Crane()
crane_1.init(ip_1)
crane_2.init(ip_2)
crane_2.start_for(20*faller.ureg.millisecond,faller.MotorChassis,faller.MotorDirectionForward)
crane_1.change_speed(faller.MotorCrab, -40)
```

Controlling a DCC train model
```python
from speedlib.trains import dcc
from speedlib.trains.dcc import Train
dcc.start()
train1.l.speed = 14
train1.faster()
train1.slower()
train1.l.fl = True 
dcc.stop()
```
You can find more examples in the *examples* directory.

Install
-------
git clone https://github.com/CRIStAL-PADR/Speed.git

The library is in speedlib/__init__.py

Tests
-----
To starts the unit tests you can do:
```console
cd tests/
PYTHONPATH=../ python3 -m unittest
```

