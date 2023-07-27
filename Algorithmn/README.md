<br />
<p align="center">
  <img src="/images/Map.png" alt="Logo" height=150 >
  <h1 align="center">
    CZ3004/SC2079 Multidisciplinary Project - Algorithm API
  </h1>
</p>

# Overview

This repository contains the code for the algorithm and image recognition inference component of the CZ3004/SC2079 Multidisciplinary Project. The repository is responsible for the following:

- Finding the shortest path from the starting point to all the obstacles.
- Performing inference on the images captured by the robot to identify the symbols.
- Stitching the images together to form a summary of the results.

## Setup

```bash
pip install -r requirements.txt
python main_cloud_algo.py


The server will be running at localhost:5000.

Miscellaneous
Raw images from Raspberry Pi are stored in the uploads folder.
After calling the image/ endpoint, the annotated image (with bounding box and label) is stored in the runs and own_results folder.
After calling the stitch/ endpoint, two stitched images using two different functions (for redundancy) are saved at runs/stitched.jpg and in the own_results folder.
Primers - Constants and Parameters
Direction of the robot (d)
NORTH - UP - 0
EAST - RIGHT - 2
SOUTH - DOWN - 4
WEST - LEFT - 6
Parameters
EXPANDED_CELL - Size of an expanded cell, usually set to 1 unit, but expanding it to 1.5 or 2 allows the robot to have more space to move around obstacles at the cost of finding a shortest path becoming harder. Useful to tweak if the robot is encountering obstacles.
WIDTH - Width of the area (in 10cm units).
HEIGHT - Height of the area (in 10cm units).
ITERATIONS - Number of iterations to run the algorithm for. A higher number of iterations will result in a more accurate shortest path but will take longer to run. Useful to tweak if the robot is not finding the shortest path.
TURN_RADIUS - Number of units the robot turns. We set the turns to 3 * TURN_RADIUS, 1 * TURN_RADIUS units. Can be tweaked in the algorithm.
SAFE_COST - Used to penalize the robot for moving too close to obstacles. Currently set to 1000. Check get_safe_cost to tweak.
SCREENSHOT_COST - Used to penalize the robot for taking pictures from a position that is not directly in front of the symbol.
API Endpoints:
1. POST Request to /path:
Sample JSON request body:


{
    "obstacles":
    [
        {
            "x": 0,
            "y": 9,
            "id": 1,
            "d": 2
        },
        ...,
        {
            "x": 19,
            "y": 14,
            "id": 5,
            "d": 6
        }
    ]
}

{
    "data": {
        "commands": [
            "FR00",
            "FW10",
            "SNAP1",
            "FR00",
            "BW50",
            "FL00",
            "FW60",
            "SNAP2",
            ...,
            "FIN"
        ],
        "distance": 46.0,
        "path": [
            {
                "d": 0,
                "s": -1,
                "x": 1,
                "y": 1
            },
            {
                "d": 2,
                "s": -1,
                "x": 5,
                "y": 3
            },
            ...,
            {
                "d": 2,
                "s": -1,
                "x": 6,
                "y": 9
            }
        ]
    },
    "error": null
}


2. POST Request to /image
The image is sent to the API as a file, thus no base64 encoding is required.

Sample Request in Python
response = requests.post(url, files={"file": (filename, image_data)})


image_data: a bytes object
The API will then perform three operations:

Save the received file into the /uploads and /own_results folders.
Use the model to identify the image, save the results into the folders above.
Return the class name as a json response
{
  "image_id": "D",
  "obstacle_id": 1
}

Please note that the inference pipeline is different for Task 1 and Task 2. Be sure to comment/uncomment the appropriate lines in app.py before running the API.

3. POST Request to /stitch
This will trigger the stitch_image and stitch_image_own functions.

Images found in the run/ and own_results directories will be stitched together and saved separately, producing two stitched images. Two functions are used for redundancy purposes, in case one fails, the other can still run.

Disclaimer
The CZ3004/SC2079 Multidisciplinary Project - Algorithm API is provided as-is, and I am not responsible for any errors, mishaps, or damages that may occur from using this code. Use at your own risk. This code is open-source and available under the MIT License, with no warranty of any kind.

Acknowledgements
Past years algorithm used as a reference/baseline but significantly improved it. Edge cases that were previously not covered/handled are now handled.