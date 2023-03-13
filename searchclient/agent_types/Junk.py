for i in range(num_agents):
    agent_postion, agent_char = initial_state.agent_positions[i]
    agent_color = level.colors[agent_char]
    monochrome_problem = initial_state.color_filter(agent_color)
    planning_success, pi_i = graph_search(monochrome_problem, action_set, goal_description, frontier)
    pi[i] = pi_i

    while any(pi):
        if len(pi[i]) == 0:
            actions[i] = "NoOp"
        else:
            actions[i] = pi[0]
        for joint_action in actions:

            print("joint_action: ", file=sys.stderr)
            print(joint_action, file=sys.stderr)

            # Uncomment the below line to print the executed actions to the command line for debugging purposes
            print(joint_action_to_string(joint_action), file=sys.stderr, flush=True)
            # Send the joint action to the server
            print(joint_action_to_string(joint_action), flush=True)

            # Read back whether the agents succeeded in performing the joint action
            execution_successes = parse_response(read_line())
            if False in execution_successes:
                print("Execution failed! Stopping...", file=sys.stderr)
                # One of the agents failed to execute their action.
                # This should not occur in classical planning and we therefore just abort immediately
                return

print("Pi: ", file=sys.stderr)
print(pi, file=sys.stderr)
print(len(pi), file=sys.stderr)
#### Pi is an array of n elements, where n is num_agents.
#### Each element has a number of tuples where each tuple has
#### n actions. However, this is a problem.

while any(pi):

    actions = [""] * num_agents

    for i in range(num_agents):
        if len(pi[i]) == 0:
            actions[i] = "NoOp"
        else:
            actions[i] = pi[0]

    for i in range(num_agents):
        print(joint_action_to_string(actions[i]), flush=True)
        execution_successes = parse_response(read_line())
        print(execution_successes)

    '''
    __return = False

    for i in range(len(pi)):
        for joint_action in pi[i]:
            print("joint_action: ", file=sys.stderr)

            # Send the joint action to the server
            print(joint_action, file=sys.stderr)
            print(joint_action_to_string(joint_action), flush=True)
            # Uncomment the below line to print the executed actions to the command line for debugging purposes
            print(joint_action_to_string(joint_action), file=sys.stderr, flush=True)

            # Read back whether the agents succeeded in performing the joint action
            execution_successes = parse_response(read_line())
            print("execution_successes: ", file=sys.stderr)
            print(execution_successes, file=sys.stderr)
            if False in execution_successes:
                # print("Number of actions that fail: {}".format(sum(execution_successes)))
                print("Execution failed! Stopping...", file=sys.stderr)
                # One of the agents failed to execute their action.
                # This should not occur in classical planning and we therefore just abort immediately
                __return = True
                return
            if execution_successes[i] and pi[i]:
                pi[i] = pi[i][1:]

        if __return:
            return
    '''

    for i in range(num_agents):
        if execution_successes[i] and len(pi[i]) == 0:
            pi[i] = pi[i].pop(0)