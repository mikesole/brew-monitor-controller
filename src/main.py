
import sys

from comms import SensorWebComms
from controllers import TemperatureController

# TODO(mikesole1989@gmail.com): Use argparse for cli arguments
# TODO(mikesole1989@gmail.com): Extract REST api parameters and convert to cli arguments

if __name__ == "__main__":

    # for now, assure that the correct number of arguments have been provided
    assert len(sys.argv) == 5
    
    api_username = sys.argv[1]
    api_password = sys.argv[2]
    sample_rate = int(sys.argv[3])
    max_heater_thresh = int(sys.argv[4])
    
    target_api_url = "https://www.brew.mikesole.co.uk/api/"
    
    login_decl = "Users/login"
    post_data_decl = "SensorReadings"
    
    # initialise REST api comms
    web_comms = SensorWebComms(api_username, api_password, target_api_url, login_decl, post_data_decl)
    
    # initialise the temperature controller
    controller = TemperatureController(web_comms)
    
    # run the controller
    controller.run(sample_rate, max_heater_thresh)
