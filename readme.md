<div align="center">
    <img src="./assets/pentagram.png" alt="Devil ghost" width="200" height="200"/>
    <h1>Demon Connection</h1>
</div>

# Requirements

- Unix
- Docker
- Python 3.11
- Pip (Package manager from Python)
- Make

# Installation

To install the base: `make install`

To install the dev requirements: `make install-dev`

# Running

To run: `make dev`

To run all specs: `make test`

# Pendency

- Authentication to server;
- Show client's online;
- Show all client's with your last connection datetime;

# Flow

## Models

Starting with models, the model of task are dynamic, doesn't have a specify validation, required just a name and optional array of string to args.

Now, to host model, have just one field that is required (`ip_address`), and he is filled when call the route of health-check.

## Client routes

In X time of loop in your client, keeps calling the route of "/client/health-check" to put your presence.

In Y time of loop in your client, also keeps calling the route of "/client/current-task" to get some task if there is.

* "X time" is the var `CLIENT_HEALTH_CHECK_LOOP_TIME` in `.en` file.
* "Y time" is not required to configure, because this case stay just in your client.

## Server routes

Actually, you can add and remove a task from a specified client and doesn't have a authentication (yet).
