import time
from threading import Lock, Thread
from sense_hat import SenseHat
import os

r = (255, 0, 0)
o = (255, 127, 0)

class BalanceChecker:
    def __init__(self):
        self.sense = SenseHat()

        # Reset the LED array.
        self.sense.clear()

        # Use all sensors to get a more accurate reading - note this means we need a
        # quick and constant poll time so that the estimation algorithm works well.
        self.sense.set_imu_config(
            compass_enabled=True, gyro_enabled=True, accel_enabled=True
        )

        # When we use threads, we have to be very careful about multiple threads
        # accessing a variable at the same time. This special object only lets at
        # most one thread hold a 'lock' on it at a time. We use this to block
        # access to threads so only one at a time can update or read pitch and roll.
        self.lockObject = Lock()

        # Make an initial update to the positions.
        update = self._get_sensor_update()
        self.pitch = update["pitch"]
        self.roll = update["roll"]

    def _get_sensor_update(self):
        return self.sense.get_orientation()

    def poll_gyroscope_data(self):
        while True:
            update = self._get_sensor_update()

            # It will wait to enter this block of code until the other thread is not
            # looking at the pitch and roll.
            with self.lockObject:
                self.pitch = update["pitch"]
                self.roll = update["roll"]

            # The ideal value could be shorter or slightly longer than this.
            time.sleep(0.05)

    def check_balance(self):
        while True:
            # Let the gyroscope reading stabilise.
            # Adjust to however often a check needs to take place.
            time.sleep(0.5)

            # It will wait to enter this block of code until the other thread is not
            # looking at the pitch and roll.
            with self.lockObject:
                pitch = self.pitch
                roll = self.roll

            is_unbalanced = False
            if 12 < pitch < 170:
                print("left:    ", str(pitch))
                is_unbalanced = True
            elif 348 > pitch > 170:
                print("right:   ", str(pitch))
                is_unbalanced = True

            #    270 is vertical
            #    Therefore ignore 7 degrees forwards and backwards
            if 280 < roll:
                print("backwards:   ", str(roll))
                is_unbalanced = True
            elif 256 > roll:
                print("forwards:    ", str(roll))
                is_unbalanced = True

            if is_unbalanced:
                self.warn_user(pitch, roll)
            else:
                self.sense.clear()
                print("Balance looks good.")

    def warn_user(self, pitch, roll):
        print("Oh no! You are falling over.")
        warning = [
        r,r,r,r,r,r,r,r,
        r,o,o,o,o,o,o,r,
        r,o,r,r,r,r,o,r,
        r,o,r,o,o,r,o,r,
        r,o,r,o,o,r,o,r,    
        r,o,r,r,r,r,o,r,
        r,o,o,o,o,o,o,r,
        r,r,r,r,r,r,r,r
        ]
        self.sense.set_pixels(warning)
        if 12 < pitch < 170:
            os.system("mpg123 right.mp3")
        elif 348 > pitch > 170:
            os.system("mpg123 left.mp3")

        if 280 < roll:
            os.system("mpg123 forwards.mp3")
        elif 256 > roll:
            os.system("mpg123 backwards.mp3")
    

    def run(self):
        poll_thread = Thread(target=self.poll_gyroscope_data)
        balance_checker_thread = Thread(target=self.check_balance)
        poll_thread.start()
        balance_checker_thread.start()

        # Wait until the balance checker thread completes (which is never,
        # so this will run forever).
        balance_checker_thread.join()


# This loop runs when you run `python unbalanced.py` in a terminal, or run from an IDE.
if __name__ == "__main__":
    SenseHat().clear
    print("[console] Welcome to Benficium Moderna, A product by inteligent health.")
    os.system("mpg123 intro.mp3")
    BalanceChecker = BalanceChecker()
    BalanceChecker.run()
