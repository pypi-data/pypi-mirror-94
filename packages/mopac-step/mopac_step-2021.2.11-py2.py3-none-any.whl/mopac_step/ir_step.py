# -*- coding: utf-8 -*-

"""Main module."""

import mopac_step


class IRStep(object):
    my_description = {
        'description': 'Infrared (vibrational) spectrum',
        'group': 'Calculations',
        'name': 'IR Spectrum'
    }

    def __init__(self, flowchart=None, gui=None):
        """Initialize this helper class, which is used by
        the application via sevedore to get information about
        and create node objects for the flowchart
        """
        pass

    def description(self):
        """Return a description of what this extension does
        """
        return IRStep.my_description

    def create_node(self, flowchart=None, **kwargs):
        """Return the new node object"""
        return mopac_step.IR(flowchart=flowchart, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Return the graphical Tk node object"""
        return mopac_step.TkIR(canvas=canvas, **kwargs)
