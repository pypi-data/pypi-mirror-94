# Picovoice Shepherd

Made in Vancouver, Canada by [Picovoice](https://picovoice.ai)

Picovoice Shepherd is the first no-code platform for building voice interfaces on microcontrollers.
It enables creating voice experiences similar to Alexa that run entirely on microcontrollers. 
Picovoice Shepherd accelerates prototyping, mitigates technical risks, and shortens time to market. 
Paired with [Picovoice Console](https://console.picovoice.ai/) users can deploy custom voice models into microcontrollers instantly.

## Compatibility

- Linux (x86_64)
- macOS (x86_64)
- Windows (x86_64)

## Installation

Install the Picovoice Shepherd:

```shell
pip3 install pvshepherd
```

### Note for macOS

Install Python using either the [official installer](https://www.python.org/downloads/mac-osx/) or [Homebrew](https://brew.sh). Shepherd cannot run using the Python shipped with macOS. If using the Homebrew Python, make sure that `/usr/local/bin` is in the `PATH` variable before installing Shepherd.

### Note for Windows

The default Python installation options do not add it to the Windows `PATH` variable. To fix the issue, refer to this [link](https://docs.python.org/3/using/windows.html#setting-envvars).

## Usage

Run the following command from the terminal:

```shell
pvshepherd
```

> On Linux, Shepherd will ask for the root password only on the first launch.

For more information, please refer to [Picovoice Shepherd Documentation](https://picovoice.ai/docs/picovoice-shepherd/)