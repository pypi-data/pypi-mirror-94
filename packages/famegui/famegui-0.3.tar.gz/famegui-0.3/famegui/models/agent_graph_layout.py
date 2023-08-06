import logging

import igraph as ig

def layout_agents(scenario):
    if len(scenario.agents) == 0:
        return

    logging.info("building graph layout for {} agents".format(len(scenario.agents)))
    g = ig.Graph(directed=True)

    # add nodes
    agent_ids = []
    for a in scenario.agents.values():
        g.add_vertex(str(a.id))
        agent_ids.append(a.id)
    # print("Added {} vertices".format(len(g.vs)))

    # add connections
    for a in scenario.agents.values():
        for sender_id in a.inputs:
            g.add_edge(str(sender_id), str(a.id))
        for receiver_id in a.outputs:
            g.add_edge(str(a.id), str(receiver_id))

    layout = g.layout_kamada_kawai()
    assert(len(layout.coords) == len(agent_ids))
    layout.fit_into(ig.BoundingBox(0, 0, 2000, 2000))

    for i, coord in enumerate(layout.coords):
        id = agent_ids[i]
        scenario.agent(id).set_display_xy(coord[0], coord[1])
