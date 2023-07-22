
import time
from algo.algo import MazeSolver 
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import *
from helper import command_generator
import json
#model = load_model()
model = None
def status():
    """
    This is a health check endpoint to check if the server is running
    :return: a json object with a key "result" and value "ok"
    """
    return jsonify({"result": "ok"})


def local_algo_path_finding(robot_obstacles_positions):
    """
    This is the main endpoint for the path finding algorithm
    :return: a json object with a key "data" and value a dictionary with keys "distance", "path", and "commands"
    """
    # Get the json data from the request
    content = robot_obstacles_positions

    # Get the obstacles, big_turn, retrying, robot_x, robot_y, and robot_direction from the json data
    obstacles = content['obstacles']
    # big_turn = int(content['big_turn'])
    retrying = content['retrying']
    robot_x, robot_y = content['robot_x'], content['robot_y']
    robot_direction = int(content['robot_dir'])

    # Initialize MazeSolver object with robot size of 20x20, bottom left corner of robot at (1,1), facing north, and whether to use a big turn or not.
    maze_solver = MazeSolver(20, 20, robot_x, robot_y, robot_direction, big_turn=None)

    # Add each obstacle into the MazeSolver. Each obstacle is defined by its x,y positions, its direction, and its id
    for ob in obstacles:
        maze_solver.add_obstacle(ob['x'], ob['y'], ob['d'], ob['id'])

    start = time.time()
    # Get shortest path
    optimal_path, distance = maze_solver.get_optimal_order_dp(retrying=retrying)
    print(f"Time taken to find shortest path using A* search: {time.time() - start}s")
    print(f"Distance to travel: {distance} units")
    
    # Based on the shortest path, generate commands for the robot
    commands = command_generator(optimal_path, obstacles)

    # Get the starting location and add it to path_results
    path_results = [optimal_path[0].get_dict()]
    # Process each command individually and append the location the robot should be after executing that command to path_results
    i = 0
    for command in commands:
        if command.startswith("SNAP"):
            continue
        if command.startswith("FIN"):
            continue
        elif command.startswith("FW") or command.startswith("FS"):
            i += int(command[2:]) // 10
        elif command.startswith("BW") or command.startswith("BS"):
            i += int(command[2:]) // 10
        else:
            i += 1
        path_results.append(optimal_path[i].get_dict())
    
    
    
    final_result = {
            "data": {
                "distance": distance,
                "path": path_results,
                "commands": commands
            },
            
            "error": None
            
            }
    
    json_final_result = json.dumps(final_result)
    print(json_final_result)
    print(final_result['data']['distance'])
    
    # count_o = 0
    # for o in final_result['data']['path']:
    #     print(o)
        
    #     for i in content['obstacles']:
    #         input_object_id = i['id']
    #         if input_object_id == o['s']:
    #             print(input_object_id)
    #             output_image_id = i['image_id']
    #             print(output_image_id)
    #         else:
    #             output_image_id = '-1'
        
    #     final_result['data']['path'][count_o]['object_id'] = final_result['data']['path'][count_o]['s']
        
        
    #     count_o += 1
    
    # # for o in json_final_result.items():
    # #     print(o)
    # print(json_final_result)

    return final_result


def image_predict():
    """
    This is the main endpoint for the image prediction algorithm
    :return: a json object with a key "result" and value a dictionary with keys "obstacle_id" and "image_id"
    """
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('uploads', filename))
    # filename format: "<timestamp>_<obstacle_id>_<signal>.jpeg"
    constituents = file.filename.split("_")
    obstacle_id = constituents[1]

    ## Week 8 ## 
    #signal = constituents[2].strip(".jpg")
    #image_id = predict_image(filename, model, signal)

    ## Week 9 ## 
    # We don't need to pass in the signal anymore
    image_id = predict_image_week_9(filename,model)

    # Return the obstacle_id and image_id
    result = {
        "obstacle_id": obstacle_id,
        "image_id": image_id
    }
    return jsonify(result)

def stitch():
    """
    This is the main endpoint for the stitching command. Stitches the images using two different functions, in effect creating two stitches, just for redundancy purposes
    """
    img = stitch_image()
    img.show()
    img2 = stitch_image_own()
    img2.show()
    return jsonify({"result": "ok"})



if __name__ == '__main__':
    
    robot_obstacles_positions = {
                                'obstacles': [
                                    {'x': 5, 'y': 5, 'd': 0, 'id': 1},
                                    {'x': 12, 'y': 5, 'd': 0, 'id': 2}
                                ],
                                'robot_x': 1,
                                'robot_y': 1,
                                'robot_dir': 0,
                                'retrying': False
                               }

    
    local_algo_path_finding(robot_obstacles_positions)
    
    