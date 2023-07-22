from Algorithmn.main_local_external_algo import local_algo_path_finding
import requests

robot_obstacles_positions = {
                                'obstacles': [
                                    {'x': 9, 'y': 9, 'd': 4, 'id': 1},
                                    {'x': 10, 'y': 4, 'd': 6, 'id': 2},
                                ],
                                'robot_x': 1,
                                'robot_y': 1,
                                'robot_dir': 0,
                                'retrying': False
                            }




# local_algo_path_finding(robot_obstacles_positions)


url = 'http://192.168.50.214:5000/path'
# url = "http://192.168.1.14:5000/path"
x = requests.post(url, json = robot_obstacles_positions)
print(x.text)


