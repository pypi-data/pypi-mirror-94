# -*- coding: utf-8 -*-

"""Helper class needed for the stevedore integration.

This must provide a description() method that returns a dict containing a
description of this node, and create_node() and create_tk_node() methods for
creating the graphical and non-graphical nodes.

"""

import read_structure_step


class ReadStructureStep(object):
    my_description = {
        'description': ('An interface for Read Structure'),
        'group': 'Simulations',
        'name': 'Read Structure'
    }
    """The description needs three fields:

    description:
        A human-readable description of this step. It can be
        several lines long, and needs to be clear to non-expert users.
    group:
        Which group in the menus to put this step. If the group does
        not exist it will be created. Common groups are 'Building',
        'Calculations', 'Control' and 'Data'.
    name:
        The name of this step, to be displayed in the menus.

    """

    def __init__(self, flowchart=None, gui=None):
        """Initialize this helper class, which is used by
        the application via stevedore to get information about
        and create node objects for the flowchart
        """
        pass

    def description(self):
        """Return a description of what this extension does
        """
        return ReadStructureStep.my_description

    def create_node(self, flowchart=None, **kwargs):
        """Create and return the new node object.
        """
        return read_structure_step.ReadStructure(flowchart=flowchart, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Create and return the graphical Tk node object.
        """
        return read_structure_step.TkReadStructure(canvas=canvas, **kwargs)
