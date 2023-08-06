fews-3di
==========================================

Program to start `3Di <https://3diwatermanagement.com/>`_ simulations from FEWS.


Installation and usage
----------------------

We can be installed using python 3.6+ with::

  $ pip install fews-3di

The script is called ``run-fews-3di``, you can pass ``--help`` to get usage
instructions and ``--verbose`` to get more verbose output in case of
problems.

``run-fews-3di`` looks for a ``run_info.xml`` in the current directory by
default, but you can pass a different file in a different location with
``--settings``::

  $ run-fews-3di
  $ run-fews-3di --help
  $ run-fews-3di --settings /some/directory/run_info.xml


Configuration and input/output files
------------------------------------

The expected information in run_info.xml is::

  <?xml version="1.0" encoding="UTF-8"?>
  <Run xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns="http://www.wldelft.nl/fews/PI"
       xsi:schemaLocation="http://www.wldelft.nl/fews/PI
			   http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_run.xsd"
			   version="1.5">
      <startDateTime date="2020-01-26" time="10:00:00"/>
      <endDateTime date="2020-01-30" time="12:00:00"/>
      <properties>
	  <string key="username" value="pietje"/>
	  <string key="password" value="onder-de-deurmat"/>
	  <string key="organisation" value="12345678abcd"/>
	  <string key="modelrevision" value="abcd123456787"/>
	  <string key="simulationname" value="Simulation name"/>
	  <string key="save_state" value="True"/>
	  <string key="saved_state_expiry_days" value="5"/>
	  <string key="rain_type" value="radar"/>
	  <string key="rain_input" value="730d6675-35dd-4a35-aa9b-bfb8155f9ca7"/>
	  <string key="fews_pre_processing" value="True"/>
	  <string key="lizard_results_scenario_name" value="Testsimulatie"/>
	  <string key="lizard_results_scenario_uuid" value=""/>
      </properties>
  </Run>
  
  

**Note:** ``saved_state_expiry_days`` used to be spelled as
``save_state_expiry_days``, without a "d". The example radar uuid
is the Dutch rainfall radar (NRR).

**Using saved states:** To use a warm state provide a text file with 
id in the states folder using the name ``states/3di-saved-state-id.txt``.
A cold state is supplied in a similar way with the name: 
``states/3di-cold-state-id.txt``. 

**Rain_type:** multipe rain-types can be used in the configuration: 

- ``constant``

- ``radar``

- ``custom``


**Rain_input:** according to the chosen rain-type, a rain input must be given in the configuration:

- ``constant`` --> ``integer [m/s]``

- ``radar`` --> ``lizard uuid``

- ``custom`` --> two options: ``rain_csv`` or ``rain_netcdf``. These files must be stored in the input directory as ``input/rain.csv`` and ``input/precipitation.nc`` 


**fews_pre_processing:** can be ``True`` or ``False``. Must be True if the results are needed in fews: additional pre_processing of the results is needed.


Several input files are needed, they should be in the ``input`` directory
**relative** to the ``run_info.xml``:

- ``run_info.xml``

- ``input/lateral.csv``

- ``input/precipitation.nc``

- ``input/evaporation.nc``

- ``input/ow.nc``

- ``model/gridadmin.h5``

Output is stored in the ``output`` directory relative to the
``run_info.xml``:

- ``output/simulation.log`` (unavailable, but included in the zip)

- ``output/flow_summary.log`` (idem)

- ``output/log_files_sim_ID.zip``

- ``output/results_3di.nc``

- ``output/dischages.csv``

- ``output/ow.nc``


Development
-----------

Development happens on github. See ``DEVELOPMENT.rst`` for more information.
