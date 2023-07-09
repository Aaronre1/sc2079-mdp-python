# sc2079-mdp-python

# Setup :wrench:
Install the required packages:
```bash
pip install -r requirements.txt
```

## Bluetooth Connection
```bash
sudo rfcomm watch hci0
```

Make rpi detectable
```bash
sudo hciconfig hci0 piscan
```

Open rfcomm channel
```bash
sudo rfcomm listen /dev/rfcomm0 0
```

