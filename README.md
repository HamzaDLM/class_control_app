# Classroom Control App

## Description

:warning: **Work still in progress**

## Installation

```
git clone https://github.com/hamzadlm/class_control_app
cd ./class_control_app
pip install -r requirements.txt
```

## Commands

|    Command     | Description                                                    |
| :------------: | -------------------------------------------------------------- |
|      help      | List general commands                                          |
|      list      | Display list of connected clients (id, ip, port, mac address). |
| connect `<ID>` | Connect to a client using it's ID.                             |
|      quit      | Terminate the server's session.                                |
|    killall     | Shutdown all connected machines.                               |
| monon / monoff | Turn on/off all monitor.                                       |
| volon / voloff | Turn on/off all volumes.                                       |
|      scrn      | Get screenshot from all clients.                               |
|    history     | Get all browser history as a file.                             |

## Commands (connected to client)

|      Command       | Description                                |
| :----------------: | ------------------------------------------ |
|        help        | List commands specific to a single client. |
|        scrn        | Get screenshot from client's device.       |
|   monon / monoff   | Turn on/off the monitor.                   |
|   volon / voloff   | Turn on/off the volume.                    |
|       killc        | Shutdown client's machine.                 |
| proxyon / proxyoff | Enable proxy to redirect http https proxy. |
|      history       | Get browser history.                       |

### TODO
- [ ] Add end-to-end encryption.
- [ ] Add all necessary exception & error handling.
- [ ] Complete the commands list.
- [ ] Add checks for if connections still maintained.
- [ ] Add Connection via secured tokens.
