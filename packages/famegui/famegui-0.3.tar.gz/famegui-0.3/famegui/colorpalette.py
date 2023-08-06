import logging

_mapped_colors = {}
_remaining_colors = ["#66b54b", "#a65ecb", "#a5b13f", "#6976d6", "#cf9834",
                            "#c5522e", "#c8489b", "#91b99d", "#d44368", "#63b8cc",
                            "#56bc84", "#5a8dc5", "#db8566", "#605690", "#b09e65",
                            "#823570", "#48786d", "#d28cd7", "#cbd6ad", "#d596be",
                            "#866a92", "#d883a0", "#afa6ce", "#7d5229", "#caa59a",
                            "#a1607b", "#5e77da", "#97b942", "#caa43f", "#d8917e"]

def color_for_agent_type(agent_type):
    """ Utility function that map a color to an agent types """
    # return color already mapped to that type
    if agent_type in _mapped_colors:
        return _mapped_colors[agent_type]

    # map a color to that new type
    if len(_remaining_colors) > 0:
        color = _remaining_colors.pop(0)
    else:
        # use default color
        color = "#aca69f"
        logging.warning("not enough colors in palette for new agent type, using default one")

    _mapped_colors[agent_type] = color
    return color
