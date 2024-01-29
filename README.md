# hass-b660-4x4
A home assistant integration for the Binary B-660 4x4 HDMI Matrix

# Installation
**1.** 
**(Manual)** Copy the **b660-4x4** folder to your Home Assistant's custom_components directory. If you don't have a **custom_components** directory, create one in the same directory as your **configuration.yaml** file.

**(HACS)** Add this repository to HACS. https://github.com/MaxMel12/hass-b660-4x4, click on the repo and click download

**2.** Add the following lines to your Home Assistant **configuration.yaml** file:

```yaml
b660_4x4:
  ip_address: "ip"
  port: 23
  username: "username"
  password: "password"
```

**3.** Restart Home Assistant.

# Usage
Navigate to developer tools > services

Search for the b660_4x4 service, and call the service

