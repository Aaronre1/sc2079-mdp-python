from Algorithmn.main_local_external_algo import local_algo_path_finding

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
