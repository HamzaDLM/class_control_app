# Classroom Control App

## Description

This platform aims to enable teachers to have control over children’s computers and be able to do basic monitoring and control over them like turning off monitors ...etc.
The platform should be accessible either via terminal or web UI localy hosted.
The communication should be secured end-to-end and the app os agnostic.

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

## Contributions

Feel free to submit a pull request!

## Disclaimer

Using this program as a RAT against devices you have no permission on is immoral & illegal!
