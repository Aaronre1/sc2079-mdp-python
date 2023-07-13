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
