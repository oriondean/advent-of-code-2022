from re import compile, Pattern
import networkx as nx


def is_distinct(route_one: str, route_two: str) -> bool:
    return len([node for node in route_one[3:].split(',') if node in route_two[3:]]) == 0


def traverse(position_current: str, key_route: str, time_remaining: int, pressure_released: int,
             results: dict[str, int], paths: dict[str, dict[str, list[str]]]):
    results[key_route] = max(results.get(key_route, 0), pressure_released)

    for position_next in nodes_with_flow:
        time_left_next = time_remaining - (len(paths[position_current][position_next]) - 1) - 1
        if position_current != position_next and position_next not in key_route and time_left_next > 0:
            route_key_next = ','.join(sorted(key_route.split(',') + [position_next]))
            pressure_released_next = pressure_released + time_left_next * nodes_with_flow[position_next]
            traverse(position_next, route_key_next, time_left_next, pressure_released_next, results, paths)
    return results


if __name__ == '__main__':
    regex_valves: Pattern[str] = compile('Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? ([\w,?\s]+)')
    graph: nx.Graph = nx.Graph()
    nodes_with_flow: dict[str, int] = {}  # we only care about nodes with flow rate

    with open('input.txt') as file:
        for line in file:
            (name, flow_rate_raw, neighbours) = regex_valves.match(line.strip()).groups()
            flow_rate = int(flow_rate_raw)
            graph.add_node(name, flow_rate=flow_rate)
            graph.add_edges_from([(name, i) for i in neighbours.split(', ')])

            if flow_rate > 0:
                nodes_with_flow[name] = flow_rate
    file.close()

    paths_shortest: dict[str, dict[str, list[str]]] = nx.shortest_path(graph)
    print('Part one', max(traverse('AA', 'AA', 30, 0, {}, paths_shortest).values()))

    # take max value from combination of routes that are distinct (i.e. don't share any paths)
    results = traverse('AA', 'AA', 26, 0, {}, paths_shortest)
    print('Part two', max([v1 + v2 for k1, v1 in results.items() for k2, v2 in results.items() if is_distinct(k1, k2)]))
