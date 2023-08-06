import threading
from typing import Callable

import blinker

Record_Signal = blinker.Signal
Callable_Thread_Create = Callable[[], None]
Callable_Thread_Destroy = Callable[[threading.Thread], None]
