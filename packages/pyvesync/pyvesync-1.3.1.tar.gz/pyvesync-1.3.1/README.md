# pyvesync [![build status](https://img.shields.io/pypi/v/pyvesync.svg)](https://pypi.python.org/pypi/pyvesync) [![Build Status](https://dev.azure.com/webdjoe/pyvesync/_apis/build/status/webdjoe.pyvesync?branchName=master)](https://dev.azure.com/webdjoe/pyvesync/_build/latest?definitionId=4&branchName=master) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/) [![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) <!-- omit in toc -->

pyvesync is a library to manage VeSync compatible [smart home devices](#supported-devices)

## Table of Contents <!-- omit in toc -->

- [Installation](#installation)
- [Supported Devices](#supported-devices)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example Usage](#example-usage)
  - [Get electricity metrics of outlets](#get-electricity-metrics-of-outlets)
- [API Details](#api-details)
  - [Manager API](#manager-api)
  - [Device API](#device-api)
  - [Outlet Specific Energy Methods and Properties](#outlet-specific-energy-methods-and-properties)
  - [Model ESW15-USA 15A/1800W Methods](#model-esw15-usa-15a1800w-methods)
  - [Air Purifier LV-PUR131S Methods](#air-purifier-lv-pur131s-methods)
  - [Dimmable Smart Light Bulb Method and Properties (ESL100)](#dimmable-smart-light-bulb-method-and-properties)
  - [Tunable Smart Light Bulb Methods and Properties (ESL100CW)](#tunable-smart-light-bulb-methods-and-properties)
  - [Dimmable Switch Methods and Properties](#dimmable-switch-methods-and-properties)
  - [Levoit 300S humidifer](#levoit-humidifier-300s-methods-and-properties)
  - [JSON Output API](#json-output-api)
    - [JSON Output for All Devices](#json-output-for-all-devices)
    - [JSON Output for Outlets](#json-output-for-outlets)
    - [JSON Output for Dimmable Switch](#json-output-for-dimmable-switch)
    - [JSON Output for Bulbs](#json-output-for-bulbs)
    - [JSON Output for Air Purifier](#json-output-for-air-purifier)
    - [JSON Output for 300S Humidifier](#json-output-for-300s-humidifier)
- [Notes](#notes)
- [Feature Requests](#feature-requests)

## Installation

Install the latest version from pip:

```python
pip install pyvesync
```

## Supported Devices

1. Etekcity Voltson Smart WiFi Outlet (7A model ESW01-USA)
2. Etekcity Voltson Smart WiFi Outlet (10A model ESW01-EU)
3. Etekcity Voltson Smart Wifi Outlet (10A model ESW03-USA)
4. Etekcity Voltson Smart WiFi Outlet (15A model ESW15-USA)
5. Etekcity Two Plug Outdoor Outlet (ESO15-TB) (Each plug is a separate object, energy readings are for both plugs combined)
6. Etekcity Smart WiFi Light Switch (model ESWL01)
7. Levoit Smart Wifi Air Purifier (LV-PUR131S)
8. Etekcity Soft White Dimmable Smart Bulb (ESL100)
9. Etekcity Cool to Soft White Tunable Dimmable Bulb (ESL100CW)
10. Etekcity Wifi Dimmer Switch (ESD16)

## Usage

To start with the module:

```python
from pyvesync import VeSync

manager = VeSync("EMAIL", "PASSWORD", "TIME_ZONE")
manager.login()

# Get/Update Devices from server - populate device lists
manager.update()

my_switch = manager.outlets[0]
# Turn on the first switch
my_switch.turn_on()
# Turn off the first switch
my_switch.turn_off()

# Get energy usage data
manager.update_energy()

# Display outlet device information
for device in manager.outlets:
    device.display()
```

## Configuration

The `time_zone` argument is optional but the specified time zone must match time zone in the tz database (IANNA Time Zone Database), see this link for reference:
[tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
The time zone determines how the energy history is generated for the smart outlets, i.e. for the week starts at 12:01AM Sunday morning at the specified time zone.  If no time zone or an invalid time zone is entered the default is America/New_York

```python
#Devices are respectively located in their own lists that can be iterated over
manager.outlets = [VeSyncOutletObjects]
manager.switches = [VeSyncSwitchObjects]
manager.fans = [VeSyncFanObjects]
manger.bulbs = [VeSyncBulbObjects]
```

If outlets are going to be continuously polled, a custom energy update interval can be set - The default is 6 hours (21600 seconds)

```python
manager.energy_update_interval = 360 # time in seconds
```

## Example Usage

### Get electricity metrics of outlets

```python
for s in manager.outlets:
  s.update_energy(check_bypass=False) # Get energy history for each device
```

## API Details

### Manager API

`VeSync.get_devices()` - Returns a list of devices

`VeSync.login()` - Uses class username and password to login to VeSync

`VeSync.update()` - Fetch updated information about devices

`VeSync.update_all_devices()` - Fetch details for all devices (run `VeSyncDevice.update()`)

`VeSync.update_energy(bypass_check=False)` - Get energy history for all outlets - Builds week, month and year nested energy dictionary.  Set `bypass_check=True` to disable the library from checking the update interval

### Device API

`VeSyncDevice.turn_on()` - Turn on the device

`VeSyncDevice.turn_off()` - Turn off the device

`VeSyncDevice.update()` - Fetch updated information about device

`VeSyncDevice.active_time` - Return active time of the device in minutes

`VeSyncDevice.get_config()` - Retrieve Configuration data such as firmware version for device and store in the `VeSyncDevice.config` dictionary

`VeSyncDevice.firmware_update` - Return true if Firmware has update available. `VeSyncDevice.get_config()` must be called first

### Outlet Specific Energy Methods and Properties

`VeSyncOutlet.update_energy(bypass_check=False)` - Get outlet energy history - Builds week, month and year nested energy dictionary. Set `bypass_check=True` to disable the library from checking the update interval

`VeSyncOutlet.energy_today` - Return current energy usage in kWh

`VeSyncOutlet.power` - Return current power in watts of the device

`VeSyncOutlet.voltage` - Return current voltage reading

`VesyncOutlet.weekly_energy_total` - Return total energy reading for the past week in kWh, starts 12:01AM Sunday morning

`VesyncOutlet.monthly_energy_total` - Return total energy reading for the past month in kWh

`VesyncOutlet.yearly_energy_total` - Return total energy reading for the past year in kWh

### Model ESW15-USA 15A/1800W Methods

The rectangular smart switch model supports some additional functionality on top of the regular api call

`VeSyncOutlet.nightlight_status` - Get the status of the nightlight

`VeSyncOutlet.nightlight_brightness` - Get the brightness of the nightlight

`VeSyncOutlet.turn_on_nightlight()` - Turn on the nightlight

`VeSyncOutlet.turn_off_nightlight()` - Turn off the nightlight

### Air Purifier LV-PUR131S Methods

`VeSyncFan.fan_level` - Return the level of the fan (1-3) or 0 for off

`VeSyncFan.filter_life` - Return the percentage of filter life remaining

`VeSyncFan.air_quality` - Return air quality reading

`VeSyncFan.auto_mode()` - Change mode to auto

`VeSyncFan.manual_mode()` - Change fan mode to manual with fan level 1

`VeSyncFan.sleep_mode()` - Change fan mode to sleep

`VeSyncFan.change_fan_speed(speed)` - Change fan speed with level 1, 2 or 3

`VeSyncFan.screen_status` - Get Status of screen on/off

### Dimmable Smart Light Bulb Method and Properties

`VeSyncBulb.brightness` - Return brightness in percentage (1 - 100)

`VeSyncBulb.set_brightness(brightness)` - Set bulb brightness values from 1 - 100

### Tunable Smart Light Bulb Methods and Properties

`VeSyncBulb.color_temp_pct` - Return color temperature in percentage (0 - 100)

`VeSyncBulb.color_temp_kelvin` - Return brightness in Kelvin

`VeSyncBulb.set_color_temp(color_temp)` - Set color temperature in percentage (0 - 100)

### Dimmable Switch Methods and Properties

`VeSyncSwitch.brightness` - Return brightness of switch in percentage (1 - 100)

`VeSyncSwitch.indicator_light_status` - return status of indicator light on switch

`VeSyncSwitch.rgb_light_status` - return status of rgb light on faceplate

`VeSyncSwitch.rgb_light_value` - return dictionary of rgb light color (0 - 255)

`VeSyncSwitch.set_brightness(brightness)` - Set brightness of switch (1 - 100)

`VeSyncSwitch.indicator_light_on()` - Turn indicator light on

`VeSyncSwitch.indicator_light_off()` - Turn indicator light off

`VeSyncSwitch.rgb_color_on()` - Turn rgb light on

`VeSyncSwitch.rgb_color_off()` - Turn rgb light off

`VeSyncSwitch.rgb_color_set(red, green, blue)` - Set color of rgb light (0 - 255)

### Levoit Humidifier 300S Methods and Properties

The details dictionary contains all device status details 

```python
VeSync300S.details = {
    'humidity': 80, # percent humidity in room
    'mist_virtual_level': 0, # Level of mist output 1 - 9
    'mist_level': 0,
    'mode': 'manual', # auto, manual, sleep
    'water_lacks': False,
    'humidity_high': False,
    'water_tank_lifted': False,
    'display': False,
    'automatic_stop_reach_target': False,
    'night_light_brightness': 0
    }
```

The configuration dictionary shows current settings

```python
VeSync300S.config = {
    'auto_target_humidity': 80, # percent humidity in room
    'display': True, # Display on/off
    'automatic_stop': False
    }
```

`VeSync300S.automatic_stop_on()` Set humidifier to stop at set humidity

`VeSync300S.automatic_stop_off` Set humidifier to run continuously 

`VeSync300S.turn_on_display()` Turn display on

`VeSync300S.turn_off_display()` Turn display off

`VeSync300S.set_humidity(30)` Set humidity between 30 and 80 percent

`VeSync300S.set_night_light_brightness(50)` Set nightlight brightness between 1 and 100

`VeSync300S.set_humidity_mode('sleep')` Set humidity mode - sleep/auto

`VeSync300S.set_mist_level(4)` Set mist output 1 - 9


### JSON Output API

The `device.displayJSON()` method outputs properties and status of the device

#### JSON Output for All Devices

```python
device.displayJSON()

#Returns:

{
  'Device Name': 'Device 1',
  'Model': 'Device Model',
  'Subdevice No': '1',
  'Status': 'on',
  'Online': 'online',
  'Type': 'Device Type',
  'CID': 'DEVICE-CID'
}
```

#### JSON Output for Outlets

```python
{
  'Active Time': '1', # in minutes
  'Energy': '2.4', # today's energy in kWh
  'Power': '12', # current power in W
  'Voltage': '120', # current voltage
  'Energy Week': '12', # totaly energy of week in kWh
  'Energy Month': '50', # total energy of month in kWh
  'Energy Year': '89', # total energy of year in kWh
}
```

#### JSON Output for Dimmable Switch

This output only applies to dimmable switch.  The standard switch has the default device JSON output shown [above](#json-output-for-all-devices)

```python
{
  'Indicator Light': 'on', # status of indicator light
  'Brightness': '50', # percent brightness
  'RGB Light': 'on' # status of RGB Light on faceplate
}
```

#### JSON Output for Bulbs

```python
# output for dimmable bulb
{
  'Brightness': '50' # brightness in percent
}

# output for tunable bulb
{
  'Kelvin': '5400' # color temperature in Kelvin
}

```

#### JSON Output for Air Purifier

```python
{
  'Active Time': '50', # minutes
  'Fan Level': '2', # fan level 1-3
  'Air Quality': '95', # air quality in percent
  'Mode': 'auto',
  'Screen Status': 'on',
  'Filter Life': '99' # remaining filter life in percent
}
```
#### JSON Output for 300S Humidifier

```python
{
  'Mode': 'manual', # auto, manual, sleep
  'Humidity': 20, # percent
  'Mist Virtual Level': 6, # Mist level 1 - 9
  'Water Lacks': True, # True/False
  'Water Tank Lifted': True, # True/False
  'Display': True, # True/False
  'Automatic Stop Reach Target': True,
  'Night Light Brightness': 10, # 1 - 100
  'Auto Target Humidity': True, # True/False
  'Automatic Stop': True # True/False
}
```

## Notes

More detailed data is available within the `VesyncOutlet` by inspecting the `VesyncOutlet.energy` dictionary.

The `VesyncOutlet.energy` object includes 3 nested dictionaries `week`, `month`, and `year` that contain detailed weekly, monthly and yearly data

```python
VesyncOutlet.energy['week']['energy_consumption_of_today']
VesyncOutlet.energy['week']['cost_per_kwh']
VesyncOutlet.energy['week']['max_energy']
VesyncOutlet.energy['week']['total_energy']
VesyncOutlet.energy['week']['data'] # which itself is a list of values
```

## Feature Requests

If you would like new devices to be added, you will need to capture the packets from the app. The easiest way to do this is by using [Packet Capture for Android](https://play.google.com/store/apps/details?id=app.greyshirts.sslcapture&hl=en_US&gl=US). This works without rooting the device. If you do not have an android or are concerned with adding an app that uses a custom certificate to read the traffic, you can use an Android emulator such as [Nox](https://www.bignox.com/).

When capturing packets make sure all packets are captured from the device list, along with all functions that the app contains. The captured packets are stored in text files, please do not capture with pcap format.

After you capture the packets, please redact the `accountid` and `token`. If you feel you must redact other keys, please do not delete them entirely. Replace letters with "A" and numbers with "1", leave all punctuation intact and maintain length. 

For example:

Before:
```
{
  'tk': 'abc123abc123==3rf',
  'accountId': '123456789',
  'cid': 'abcdef12-3gh-ij'
}
```
After:
```
{
  'tk': 'AAA111AAA111==1AA',
  'accountId': '111111111',
  'cid': 'AAAAAA11-1AA-AA'
}
``` 

All contributions are welcome, please run `tox` before submitting a PR to ensure code is valid.
