# sc2079-mdp-python

# Setup :wrench:
Install the required packages:
```bash
pip install -r requirements.txt
```

## Bluetooth Connection
```
sudo rfcomm watch hci0
```

Make rpi detectable
```
sudo hciconfig hci0 piscan
```

Open rfcomm channel 1
```
sudo rfcomm listen /dev/rfcomm0 1
```

### Should only need the following
Receive message
```
cat dev/rfcomm0
```
Send message
```
echo "Message" > /dev/rfcomm0
```


### Sample Algo Response
```JSON
{
  "data": {
    "commands": [
      "FW90",
      "FW10",
      "BR00",
      "BR00",
      "SNAP3_C",
      "FR00",
      "BW70",
      "BR00",
      "SNAP7_C",
      "FIN"
    ],
    "distance": 69.0,
    "path": [
      {
        "d": 0,
        "s": -1,
        "x": 1,
        "y": 1
      },
      {
        "d": 0,
        "s": -1,
        "x": 1,
        "y": 10
      },
      {
        "d": 0,
        "s": -1,
        "x": 1,
        "y": 11
      },
      {
        "d": 6,
        "s": -1,
        "x": 2,
        "y": 8
      },
      {
        "d": 4,
        "s": 3,
        "x": 5,
        "y": 9
      },
      {
        "d": 6,
        "s": -1,
        "x": 2,
        "y": 8
      },
      {
        "d": 6,
        "s": -1,
        "x": 9,
        "y": 8
      },
      {
        "d": 4,
        "s": 7,
        "x": 12,
        "y": 9
      }
    ]
  },
  "error": null
}
```

# TODO
- [ ] Rpi package
    - [ ] Movement module 
        - [x] Decimal to Hex convertor
        - [ ] Forward
            - [ ] forward
            - [ ] half_forward
            - [ ] full_forward
    - [ ] Path planner module
        - [ ] Command queue to movement convertor
    - [ ] Arena receiver module
    - [ ] Arena transimitter module
    - [ ] Camera module
    - [ ] ImageID receiver module
    
- [ ] Image Recognition
    - [ ] 6 & 9 inaccurate (upside down)
    - [ ] bullseye inaccurate
