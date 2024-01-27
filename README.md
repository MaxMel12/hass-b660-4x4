# hass-b660-4x4
A home assistant integration for the Binary B-660 4x4 HDMI Matrix

# Installation
**1.** 
**(Manual)** Copy the **b660-4x4** folder to your Home Assistant's custom_components directory. If you don't have a **custom_components** directory, create one in the same directory as your **configuration.yaml** file.

**(HACS)** Add this repository to HACS. https://github.com/MaxMel12/hass-b660-4x4

**2.** Add the following lines to your Home Assistant **configuration.yaml** file:

```yaml
b660_4x4:
  ip_address: "10.0.0.185"
  port: 23
  username: "admin"
  password: "password"
```
Replace **YOUR_OPENAI_API_KEY** with your actual OpenAI API key.

**3.** Restart Home Assistant.

