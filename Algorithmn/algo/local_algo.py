import heapq
import math
from typing import List
import numpy as np
from Algorithmn.entities.Local_Robot import Robot
from Algorithmn.entities.Local_Entity import Obstacle, CellState, Grid
from Algorithmn.consts import Direction, MOVE_DIRECTION, TURN_FACTOR, ITERATIONS, TURN_RADIUS, SAFE_COST
from python_tsp.exact import solve_tsp_dynamic_programming

turn_wrt_big_turns = [[3 * TURN_RADIUS, TURN_RADIUS],
                  [3 * TURN_RADIUS, TURN_RADIUS]]


class MazeSolver:
    def __init__(
            self,
            size_x: int,
            size_y: int,
            robot_x: int,
            robot_y: int,
            robot_direction: Direction,
            big_turn=None 
    ):
        self.table_grid = Grid(size_x, size_y)
        self.robot = Robot(robot_x, robot_y, robot_direction)
        self.table_path = dict()
        self.table_cost = dict()
        if big_turn is None:
            self.required_turn = 0
        else:
            self.required_turn = int(big_turn)

    def add_obstacle(self, x: int, y: int, direction: Direction, obstacle_id: int):

        obstacle = Obstacle(x, y, direction, obstacle_id)
        self.table_grid.add_obstacle(obstacle)

    def reset_obstacles(self):
        self.table_grid.reset_obstacles()

    @staticmethod
    def compute_coord_distance(x1: int, y1: int, x2: int, y2: int, level=1):
        horizontal_distance = x1 - x2
        vertical_distance = y1 - y2

        # Euclidean distance
        if level == 2:
            return math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2)

        return abs(horizontal_distance) + abs(vertical_distance)

    @staticmethod
    def compute_state_distance(start_state: CellState, end_state: CellState, level=1):
        return MazeSolver.compute_coord_distance(start_state.x, start_state.y, end_state.x, end_state.y, level)

    @staticmethod
    def get_visit_options(n):

        s = []
        l = bin(2 ** n - 1).count('1')

        for i in range(2 ** n):
            s.append(bin(i)[2:].zfill(l))

        s.sort(key=lambda x: x.count('1'), reverse=True)
        return s

    def get_optimal_order_dp(self, retrying) -> List[CellState]:
        distance = 1e9
        optimal_path = []


        all_view_positions = self.table_grid.get_view_obstacle_positions(retrying)
        print(f"all_view_positions: {all_view_positions}")
        print(f"All view position: {all_view_positions}")

        for op in self.get_visit_options(len(all_view_positions)):

            items = [self.robot.get_start_state()]
            # Initialize `cur_view_positions` to be an empty list
            cur_view_positions = []
            
            # print(f"===================\nop = {op}")
            # print("List of obstacle visited: \n")

            for idx in range(len(all_view_positions)):
                if op[idx] == '1':
                    items = items + all_view_positions[idx]
                    cur_view_positions.append(all_view_positions[idx])
                    #print("obstacle: {}\n".format(self.table_grid.obstacles[idx]))

            # Generate the path cost for the items
            self.path_cost_generator(items)
            combination = []
            self.generate_combination(cur_view_positions, 0, [], combination, [ITERATIONS])

            for c in combination: # run the algo some times ->
                visited_candidates = [0] # add the start state of the robot

                cur_index = 1
                fixed_cost = 0 # the cost applying for the position taking obstacle pictures
                for index, view_position in enumerate(cur_view_positions):
                    visited_candidates.append(cur_index + c[index])
                    fixed_cost += view_position[c[index]].penalty
                    cur_index += len(view_position)
                
                cost_np = np.zeros((len(visited_candidates), len(visited_candidates)))

                for s in range(len(visited_candidates) - 1):
                    for e in range(s + 1, len(visited_candidates)):
                        u = items[visited_candidates[s]]
                        v = items[visited_candidates[e]]
                        if (u, v) in self.table_cost.keys():
                            cost_np[s][e] = self.table_cost[(u, v)]
                        else:
                            cost_np[s][e] = 1e9
                        cost_np[e][s] = cost_np[s][e]
                cost_np[:, 0] = 0
                _permutation, _distance = solve_tsp_dynamic_programming(cost_np)

                if _distance + fixed_cost >= distance:
                    continue

                optimal_path = [items[0]]
                distance = _distance + fixed_cost

                for i in range(len(_permutation) - 1):
                    from_item = items[visited_candidates[_permutation[i]]]
                    to_item = items[visited_candidates[_permutation[i + 1]]]

                    cur_path = self.table_path[(from_item, to_item)]
                    for j in range(1, len(cur_path)):
                        optimal_path.append(CellState(cur_path[j][0], cur_path[j][1], cur_path[j][2]))

                    optimal_path[-1].set_screenshot(to_item.screenshot_id)

            if optimal_path:
                break

        return optimal_path, distance


    def get_neighbors(self, x, y, direction):  # TODO: see the behavior of the robot and adjust...
        neighbors = []
        for dx, dy, md in MOVE_DIRECTION:
            if md == direction:  # if the new direction == md
                if self.table_grid.reachable(x + dx, y + dy):  # go forward;
                    safe_cost = self.get_safe_cost(x + dx, y + dy)
                    neighbors.append((x + dx, y + dy, md, safe_cost))
                if self.table_grid.reachable(x - dx, y - dy):  # go back;
                    safe_cost = self.get_safe_cost(x - dx, y - dy)
                    neighbors.append((x - dx, y - dy, md, safe_cost))

            else:
                
                change_in_x = turn_wrt_big_turns[self.required_turn][0]
                change_in_y = turn_wrt_big_turns[self.required_turn][1]

                if direction == Direction.NORTH and md == Direction.EAST:

                    if self.table_grid.reachable(x + change_in_x, y + change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_x, y + change_in_y)
                        neighbors.append((x + change_in_x, y + change_in_y, md, safe_cost + 10))

                    if self.table_grid.reachable(x - change_in_y, y - change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_y, y - change_in_x)
                        neighbors.append((x - change_in_y, y - change_in_x, md, safe_cost + 10))

                if direction == Direction.EAST and md == Direction.NORTH:
                    if self.table_grid.reachable(x + change_in_y, y + change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_y, y + change_in_x)
                        neighbors.append((x + change_in_y, y + change_in_x, md, safe_cost + 10))

                    if self.table_grid.reachable(x - change_in_x, y - change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_x, y - change_in_y)
                        neighbors.append((x - change_in_x, y - change_in_y, md, safe_cost + 10))

                # east <-> south
                if direction == Direction.EAST and md == Direction.SOUTH:
                    
                    if self.table_grid.reachable(x + change_in_y, y - change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_y, y - change_in_x)
                        neighbors.append((x + change_in_y, y - change_in_x, md, safe_cost + 10))

                    if self.table_grid.reachable(x - change_in_x, y + change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_x, y + change_in_y)
                        neighbors.append((x - change_in_x, y + change_in_y, md, safe_cost + 10))

                if direction == Direction.SOUTH and md == Direction.EAST:
                    if self.table_grid.reachable(x + change_in_x, y - change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_x, y - change_in_y)
                        neighbors.append((x + change_in_x, y - change_in_y, md, safe_cost + 10))

                    if self.table_grid.reachable(x - change_in_y, y + change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_y, y + change_in_x)
                        neighbors.append((x - change_in_y, y + change_in_x, md, safe_cost + 10))

                # south <-> west
                if direction == Direction.SOUTH and md == Direction.WEST:
                    if self.table_grid.reachable(x - change_in_x, y - change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_x, y - change_in_y)
                        neighbors.append((x - change_in_x, y - change_in_y, md, safe_cost + 10))

                    if self.table_grid.reachable(x + change_in_y, y + change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_y, y + change_in_x)
                        neighbors.append((x + change_in_y, y + change_in_x, md, safe_cost + 10))

                if direction == Direction.WEST and md == Direction.SOUTH:
                    if self.table_grid.reachable(x - change_in_y, y - change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_y, y - change_in_x)
                        neighbors.append((x - change_in_y, y - change_in_x, md, safe_cost + 10))

                    if self.table_grid.reachable(x + change_in_x, y + change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_x, y + change_in_y)
                        neighbors.append((x + change_in_x, y + change_in_y, md, safe_cost + 10))

                # west <-> north
                if direction == Direction.WEST and md == Direction.NORTH:
                    if self.table_grid.reachable(x - change_in_y, y + change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_y, y + change_in_x)
                        neighbors.append((x - change_in_y, y + change_in_x, md, safe_cost + 10))

                    if self.table_grid.reachable(x + change_in_x, y - change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_x, y - change_in_y)
                        neighbors.append((x + change_in_x, y - change_in_y, md, safe_cost + 10))

                if direction == Direction.NORTH and md == Direction.WEST:
                    if self.table_grid.reachable(x + change_in_y, y - change_in_x, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x + change_in_y, y - change_in_x)
                        neighbors.append((x + change_in_y, y - change_in_x, md, safe_cost + 10))

                    if self.table_grid.reachable(x - change_in_x, y + change_in_y, turn = True) and self.table_grid.reachable(x, y, preTurn = True):
                        safe_cost = self.get_safe_cost(x - change_in_x, y + change_in_y)
                        neighbors.append((x - change_in_x, y + change_in_y, md, safe_cost + 10))

        return neighbors

    def get_safe_cost(self, x, y):
        for ob in self.table_grid.obstacles:
            if abs(ob.x-x) == 1 and abs(ob.y-y) == 2:
                return SAFE_COST
            
            if abs(ob.x-x) == 2 and abs(ob.y-y) == 1:
                return SAFE_COST

            if abs(ob.x-x) == 2 and abs(ob.y-y) == 2:
                return SAFE_COST

        return 0
    
    def path_cost_generator(self, states: List[CellState]):
        # Generate the path cost between the input states and update the tables accordingly

   
        def record_path(start, end, parent: dict, cost: int):

            # Update cost table for the (start,end) and (end,start) edges
            self.table_cost[(start, end)] = cost
            self.table_cost[(end, start)] = cost

            path = []
            cursor = (end.x, end.y, end.direction)

            while cursor in parent:
                path.append(cursor)
                cursor = parent[cursor]

            path.append(cursor)

            self.table_path[(start, end)] = path[::-1]
            self.table_path[(end, start)] = path

        def astar_search(start: CellState, end: CellState):
            # astar search algo with three states: x, y, direction

            # If it is already done before, return
            if (start, end) in self.table_path:
                return

            g_distance = {(start.x, start.y, start.direction): 0}


            heap = [(self.compute_state_distance(start, end), start.x, start.y, start.direction)]
            parent = dict()
            visited = set()

            while heap:
                _, cur_x, cur_y, cur_direction = heapq.heappop(heap)
                
                if (cur_x, cur_y, cur_direction) in visited:
                    continue

                if end.is_eq(cur_x, cur_y, cur_direction):
                    record_path(start, end, parent, g_distance[(cur_x, cur_y, cur_direction)])
                    return

                visited.add((cur_x, cur_y, cur_direction))
                cur_distance = g_distance[(cur_x, cur_y, cur_direction)]

                for next_x, next_y, new_direction, safe_cost in self.get_neighbors(cur_x, cur_y, cur_direction):
                    if (next_x, next_y, new_direction) in visited:
                        continue

                    move_cost = Direction.rotation_cost(new_direction, cur_direction) * TURN_FACTOR + 1 + safe_cost

                    # new cost is calculated by the cost to reach current state + cost to move from
                    # current state to new state + heuristic cost from new state to end state
                    next_cost = cur_distance + move_cost + \
                                self.compute_coord_distance(next_x, next_y, end.x, end.y)

                    if (next_x, next_y, new_direction) not in g_distance or \
                            g_distance[(next_x, next_y, new_direction)] > cur_distance + move_cost:
                        g_distance[(next_x, next_y, new_direction)] = cur_distance + move_cost
                        parent[(next_x, next_y, new_direction)] = (cur_x, cur_y, cur_direction)

                        heapq.heappush(heap, (next_cost, next_x, next_y, new_direction))

        for i in range(len(states) - 1):
            for j in range(i + 1, len(states)):
                astar_search(states[i], states[j])
                
    @staticmethod
    def generate_combination(view_positions, index, current, result, iteration_left):
        if index == len(view_positions):
            result.append(current[:])
            return

        if iteration_left[0] == 0:
            return

        iteration_left[0] -= 1
        for j in range(len(view_positions[index])):
            current.append(j)
            MazeSolver.generate_combination(view_positions, index + 1, current, result, iteration_left)
            current.pop()

if __name__ == "__main__":
    pass
