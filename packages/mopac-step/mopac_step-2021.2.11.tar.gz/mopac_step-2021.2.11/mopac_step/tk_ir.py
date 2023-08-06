# -*- coding: utf-8 -*-

"""The graphical part of a MOPAC vibrational node"""

import mopac_step
import seamm_widgets as sw
import tkinter as tk


class TkIR(mopac_step.TkEnergy):

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=120,
        y=20,
        w=200,
        h=50
    ):
        '''Initialize a node

        Keyword arguments:
        '''
        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h
        )

    def create_dialog(
        self,
        title='MOPAC Infrared (Vibrational) Spectrum',
        calculation='vibrations'
    ):
        """Create the dialog!"""
        self.logger.debug('Creating the dialog')
        super().create_dialog(title=title, calculation='vibrations')
        self.logger.debug('Finished creating the dialog')

    def reset_dialog(self, widget=None):
        """Layout the widgets in the main frame

        We'll let 'TkEnergy' layout the initial set of widgets,
        then add the extra widgets for controlling optimization
        """
        row = super().reset_dialog()

        widgets = []
        for key in ('trans', 'let'):
            self[key].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        sw.align_labels(widgets)

        return row
