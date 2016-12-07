from time import time, sleep
from threading import Lock
import copy


from sensors import Pressure, IMU


class ROV(object):

    def __init__(self):
        self._data = {}
        self.last_update = time()

        self.simple_sensors = {
            "imu": IMU(),
            "pressure": Pressure()
        }

        self._data_lock = Lock()

    @property
    def data(self):
        self._data_lock.acquire()

        self._data['last_update'] = self.last_update
        ret = copy.deepcopy(self._data)

        self._data_lock.release()

        return ret

    def update(self):
        self._data_lock.acquire()

        print "Update! %.5f" % (time() - self.last_update)

        # Update all simple sensor data and stuff it in data
        for sensor in self.simple_sensors.keys():
            self.simple_sensors[sensor].read()
            self._data[sensor] = self.simple_sensors[sensor].data

        # Our last update
        self.last_update = time()

        self._data_lock.release()

    def run(self):
        while True:
            while time() - self.last_update < 0.01:
                sleep(0.001)

            self.update()


if __name__ == "__main__":
    r = ROV()
    r.run()