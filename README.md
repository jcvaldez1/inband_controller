# inband_controller
Network traffic rerouter for connectivity issue resiliency

## SDN controller classes
Class used for initializing an SDN controller
### learning_switch
Base class for the SDN controller, contains basic network routing capabilities with volatile network address tables.
### main_controller
Class extending learning_switch, contains packet header rewriting capabilities for rerouting network traffic to configurable paths.
### docker_host_handler
Class extending main_controller, contains a simple container management structure for CRUD, configuration, etc. Communicates to the host running containers via docker daemon API.

## Wrappers
Pythonic class declarations for wrapping data structures
### container_wrapper
Wrapper class for docker containers. (Currently a redundant implementation)
### alias_object
Wrapper class for SDN flows that are used for rerouting network traffic.
## Configuration
### constants
Contains declaration of constants used for configuration.

## Miscellaneous
### dockerstuff
Contains a sample docker environment for use of the host running the docker daemon
### container_testers
Sample scripts for diagnosing docker container functionalities such as stop, pause, create, etc.
### config_generators
Sample scripts for generating configurations for the sample application used by the containers defined in dockerstuff
### cold_mode_files
Files for the implementation of the cold_mode feature. (currently unfinished and discontinued)

# iot_objects
Experimentation environment used for the methodology shown in the official documentation.
## updated_samsung
Experimentation scripts for use in the original Samsung sensor and Lifx lightbulb environment. (currently discontinued)

## equal_step_mn
Experimentation scripts for testing the IoT subnetwork emulation environment via mininet as discussed in the official documentation.
### Implementation
#### actuator
Sends periodic requests to its respective cloud service. For execution on an actuator device.
#### receiver
Opens a persistent websocket connection to its respective cloud service. For execution on a receiver device.
#### custom_topo
Custom mininet topology for emulating the IoT devices.
#### ghost_reg
Used for registering the IoT devices and their respective cloud services to the SDN controller
#### makedir
Python implementation for creating a directory
#### post_sender
Python implementation for sending HTTP POST requets
#### constants
Contains declaration of constants used for configuration.

### Automation scripts
#### start_experiment.sh
Used for executing the currently configured experiment setup.
#### results_movers.sh
Used for automatically moving finished experiment results to the experiments directory. Called by custom_topo
#### ovs_starter
Diagnostic script for checking ovs installation on host machine

### Result Directories
#### experiments
Used to store results from experiments runs. Contains sample data from experiments used in the official documentation. Contains parsing and graphing scripts for quick visualization.

#### resource_usage
Used to store resource usage results from the container host during experiment runs. Contains sample data from experiments used in the official documentation. Contains parsing and graphing scripts for quick visualization. No automatic generation, present only due to convention.




