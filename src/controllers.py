
import time

# temperature sensor library
from w1thermsensor import W1ThermSensor

# power switch
from gpiozero import Energenie


# TO DO: tidy sensor group code
sensor_group_a = ["800000268a96", "80000026ab3b", "80000026cc1c"]
sensor_group_b = ["8000002703c7", "800000268eda", "80000026cb5b"]

sensors = {}

sensor_id = 0

for sensor in sensor_group_a:
   sensors.setdefault(sensor, sensor_id)
   sensor_id += 1

for sensor in sensor_group_b:
   sensors.setdefault(sensor, sensor_id)
   sensor_id += 1


"""
    Controls brew temperature and pushes data to REST api
"""
class TemperatureController(object):

    """
        Initialise communications and sensors
    """
    def __init__(self, web_comms):
        
        # initialise web communications
        self._web_comms = web_comms
        
        # try to initialise the temperature sensor
        self._temp_sensor = None
        try:
            self._temp_sensor = W1ThermSensor()
        except Exception as e:
            print(e)
            
    """   
        Abiding to the sample rate:
            - sample temperature
            - push reading to REST api 
            - turn heater on / off in response to temperature    
    """
    def run(self, sample_rate, max_heater_thresh):    

        # assure that the temperature sensor has been initialised
        assert self._temp_sensor != None

        while True:

            print("reading temp ...")

            a_temp_celsius = 0
            b_temp_celsius = 0

            # collect temperature readings from sensors and set the maximum
            # temperature as the current temperature
            temp_readings = []
            for sensor in W1ThermSensor.get_available_sensors():
                temp = sensor.get_temperature()
                id = sensors[sensor.id]
                temp_readings.append((id, temp))
                if id <= 2:
                   a_temp_celsius = max(a_temp_celsius, temp)
                else:
                   b_temp_celsius = max(b_temp_celsius, temp)
            
            # push readings to REST api
            try:
                self._web_comms.postSensorReading(temp_readings)
            except Exception as e:
                # catch all exceptions from web communications so 
                # that the temperature controller is not interrupted
                print(e)
                
            # control heater a
            if a_temp_celsius > max_heater_thresh:
                # turn heater off
                Energenie(1, initial_value=False)
            else:
                # turn heater on
                Energenie(1, initial_value=True)

            # control heater b
            if b_temp_celsius > max_heater_thresh:
                # turn heater off
                Energenie(2, initial_value=False)
            else:
                # turn heater on
                Energenie(2, initial_value=True)

            print("readings:")
            for reading in temp_readings:
                print("\t" + str(reading))
            print("sleeping...")

            # sleep 
            time.sleep(sample_rate)
            
