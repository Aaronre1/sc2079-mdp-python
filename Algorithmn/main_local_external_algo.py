
import time
from Algorithmn.algo.local_algo import MazeSolver 
from Algorithmn.local_helper import command_generator



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
                'distance': distance,
                'path': path_results,
                'commands': commands
            },
            
            "error": None
            
            }
    print(final_result)
    return final_result




if __name__ == '__main__':
    
    robot_obstacles_positions = {
                                'obstacles': [
                                    {'x': 5, 'y': 5, 'd': 0, 'id': 3},
                                    {'x': 12, 'y': 5, 'd': 0, 'id': 7}
                                ],
                                'robot_x': 1,
                                'robot_y': 1,
                                'robot_dir': 0,
                                'retrying': False
                               }

    
    local_algo_path_finding(robot_obstacles_positions)
    
    