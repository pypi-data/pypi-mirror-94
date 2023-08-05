[![Build Status](https://jenkins.cognicept.systems/buildStatus/icon?job=cognicept-shell-pipeline)](https://jenkins.cognicept.systems/job/cognicept-shell-pipeline/)


# COGNICEPT SHELL #

This is a shell utility to manage Cognicept tools.

  * [Installation](#installation)
    + [Dependencies](#dependencies)
    + [Package installation](#package-installation)
  * [Usage](#usage)
    + [Commands](#commands)
  * [Building](#building)
    + [Tests](#tests)
    + [Build](#build)
    + [Upload](#upload)
  * [Contribution](#contribution)
  * [Version history](#version-history)

## Installation

### Dependencies

You need:

* Python 3
* Python 3 PIP

Install:

```
sudo apt-get install python3 python3-pip
```

### Package installation

To install the package locally, run:

```
pip3 install -e <path-to-the-repo>
```

To install from Python Package Index (PyPI), run:

```
pip3 install cognicept-shell
```

To verify installation, try to run

```
cognicept -h
```

If you get `cognicept: command not found` error, make sure that `~/.local/bin/` is in your `$PATH`. You could run this:

```
export PATH=$PATH:/home/$USER/.local/bin/
```
and add it to your `.bashrc` file.

## Usage

For details on usage, use

```
cognicept -h
```

### Commands

#### `config`: Configure Cognicept tools

`cognicept-shell` and Cognicept agents are configured in `runtime.env` file typically placed in `~/.cognicept/runtime.env`. The file defines the docker environment used by the Cognicept agents. 

This command allows to inspect and modify the configuration file. You can use parameter `--path` to modify the path to the Cognicept config directory.

To print full configuration, run:

```
cognicept config --read
```

To add new configuration parameter (or modify single value), run:

```
cognicept config --add
```

Variables used by `cognicept-shell`:

* `COGNICEPT_ACCESS_KEY`
* `COGNICEPT_API_URI`
* `COG_AGENT_CONTAINERS`
* `COG_AGENT_IMAGES`
* `COG_EXTRA_IMAGES` : images to pull from Cognicept and general docker image repositories
* `COG_ORBITTY_ENABLED`
* `COG_ORBITTY_IMAGE`
* `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`: temporary AWS credentials modified by `keyrotate` and needed for `update`
* `COG_ENABLE_SSH`
* `COG_ENABLE_SSH_KEY_AUTH`
* `COG_ENABLE_AUTOMATIC_SSH`
* `COG_SSH_DEFAULT_USER`

To setup `ssh` access from `remote_intervention_agent` to the host machine, run:

```
cognicept config --ssh
```

It will generate ssh keys in `~/.cognicept/ssh/` and configures `COG_ENABLE_SSH`, `COG_ENABLE_SSH_KEY_AUTH`, `COG_ENABLE_AUTOMATIC_SSH`, `COG_SSH_DEFAULT_USER` according to the user preferences. If `COG_ENABLE_AUTOMATIC_SSH` is enabled, public key is copied into `~/.ssh/authorized_hosts`; `sudo` access is requested to perform this action.

#### `status`: Get status of Cognicept agents

```
cognicept status
```
Prints status of agents and other containers managed by `cognicept-shell`. Possible values:

* "ONLINE": Everything fine
* "CONTAINER NOT FOUND": Agent/container is not initiated
* "OFFLINE": Container stopped
* "Error": Error accessing API
* "ERROR": Detected error, needs inspection
* "NOT INITIALIZED": Agent is in init state
* "STALE": Agent didn't update within last minute   

#### `update`: Update Cognicept tools

Updates images for agents and tools specified in `COG_AGENT_IMAGES` and `COG_EXTRA_IMAGES` config variables. It requires temporary credentials to be valid. For updates to take effect, containers need to be restarted with `restart` command.

#### `lastevent`: Display last event log reported by Cognicept agent

Displays last event saved by `cgs_diagnostics_agent` from `~/.cognicept/logs`.

#### `start`/`stop`/`restart`: start/stop/restart cognicept agents

These commands are used to start/stop/restart containers and datadog specified in `COG_AGENT_CONTAINERS`/`COG_AGENT_IMAGES`. Certain container names are reserved for Cognicept agents and are preconfigured:

* `cgs_diagnostics_agent`
* `remote_intervention_agent`
* `cgs_diagnostics_ecs_api`
* `cgs_diagnostics_streamer_api`
* `cgs_bagger_server`

Any agent name or image type can be put in the list as long as default command for the image is specified. All containers are started in `host` network mode.

Following are examples for using `start`. `stop` follows same API as `start`. `restart` first calls `stop` and then `stop` .

To start all listed agents `COG_AGENT_CONTAINERS` and datadog, don't specify any argument:

```
cognicept start
```

To start all agents:

```
cognicept start --agents
```

To start datadog:

```
cognicept start --datadog
```


To start specific agents:

```
cognicept start remote_intervention_agent cgs_diagnostics_agent
```

#### `keyrotate`: Rotate Cognicept cloud keys

Updates temporary AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`) using `COGNICEPT_ACCESS_KEY` from `COGNICEPT_API_URI`. The validity of the credentials is 12 hours. Internet access with HTTPS allowed is needed.

#### `orbitty`: Run Orbitty

TODO

#### `record`: Manage rosbag recording

To be done in future release.

#### `push`: Push data to Cognicept cloud

To be done in future release

## Building


### Tests

`cognicept-shell` is using `pytest` as the test framework. Make sure you install manually:

```
pip3 install pytest pytest-cov cli_test_helpers mock
```

To run tests, execute:

```
pytest --cov=cogniceptshell tests
```

Output will look like this:

```
user@computer:~/cognicept-shell$ pytest --cov=cogniceptshell tests
============================= test session starts ==============================
platform linux -- Python 3.8.5, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
rootdir: /home/jakub/code/cognicept-shell
plugins: cov-2.10.0
collected 50 items                                                             

tests/functional/test_config.py ........s                                [ 18%]
tests/functional/test_push.py ..........                                 [ 38%]
tests/functional/test_record.py ..........                               [ 58%]
tests/unit/test_config.py ....                                           [ 66%]
tests/unit/test_keyrotate.py ...                                         [ 72%]
tests/unit/test_lifecycle.py ..............                              [100%]

----------- coverage: platform linux, python 3.8.5-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
cogniceptshell/__init__.py               2      0   100%
cogniceptshell/agent_life_cycle.py     319    117    63%
cogniceptshell/common.py                15      5    67%
cogniceptshell/configuration.py        189     53    72%
cogniceptshell/interface.py             79      2    97%
cogniceptshell/pusher.py               104     11    89%
cogniceptshell/rosbag_record.py         90     13    86%
--------------------------------------------------------
TOTAL                                  798    201    75%


======================== 49 passed, 1 skipped in 28.59s ========================
```

### Build

To build the PyPI package, run:

```
python3 setup.py sdist bdist_wheel
```

This will generate the build files. 

### Upload

To upload the dev package, run:

```
python3 -m twine upload --repository testpypi dist/* --verbose
```

To upload the prod package, run:

```
python3 -m twine upload dist/* --verbose
```

## Contribution

Please follow [the successful branching model](https://nvie.com/posts/a-successful-git-branching-model/). The naming of branches follows:

* Feature branch: /feature/name-of-the-feature
* Bug fix branch: /fix/name-of-the-bug
* Release branch: /release/name-of-the-release


## Version history

* 1.1 []
    * Limit agent logs to 5MB

* 1.0 [15/12/2020]
    * Added `start` command
    * Start/Stop/Restart agents separately as parameter of command
    * Migrated to new credential management using `COGNICEPT_ACCESS_KEY` 
    * Added `keyrotate` command
    * Added unit and functional tests
    * Added `record` and `push` commands for management of rosbags
    * Added support for Python 3.5
    * Added `lastevent` command to read last event 
    * Added ssh configuration for `remote_intervention_agent`

* 0.1 [10/6/2020]
    * First version of the CLI utility able to configure, restart, and update agents 

