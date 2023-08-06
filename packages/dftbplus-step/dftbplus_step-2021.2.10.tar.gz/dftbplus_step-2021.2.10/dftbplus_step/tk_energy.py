# -*- coding: utf-8 -*-

"""The graphical part of a DFTB+ Energy node"""

import logging
import tkinter as tk
import tkinter.ttk as ttk

import dftbplus_step
import seamm
import seamm_widgets as sw

logger = logging.getLogger(__name__)


class TkEnergy(seamm.TkNode):

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=120,
        y=20,
        w=200,
        h=50,
        my_logger=logger,
        keyword_metadata=None
    ):
        """Initialize the graphical Tk DFTB+ Energy step

        Keyword arguments:
        """
        self.results_widgets = []

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h,
            my_logger=my_logger,
            keyword_metadata=keyword_metadata
        )

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def create_dialog(
        self, title='Edit DFTB+ Energy Step', calculation='energy'
    ):
        """Create the dialog!"""
        self.logger.debug('Creating the dialog')
        super().create_dialog(title=title, widget='notebook', results_tab=True)

        # Create all the widgets
        P = self.node.parameters

        # Frame to isolate widgets
        e_frame = self['energy frame'] = ttk.LabelFrame(
            self['frame'],
            borderwidth=4,
            relief='sunken',
            text='Hamiltonian Parameters',
            labelanchor='n',
            padding=10
        )

        for key in dftbplus_step.EnergyParameters.parameters:
            if key not in ('results', 'extra keywords', 'create tables'):
                self[key] = P[key].widget(e_frame)

        # Set the callbacks for changes
        for widget in ('SCC', 'HCorrection'):
            w = self[widget]
            w.combobox.bind("<<ComboboxSelected>>", self.reset_energy_frame)
            w.combobox.bind("<Return>", self.reset_energy_frame)
            w.combobox.bind("<FocusOut>", self.reset_energy_frame)

        self.setup_results(dftbplus_step.properties, calculation=calculation)

        self.logger.debug('Finished creating the dialog')

    def reset_dialog(self, widget=None):
        frame = self['frame']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # Put in the energy frame
        row = 0
        self['energy frame'].grid(row=row, column=0, sticky=tk.N)
        row += 1

        # and the widgets in it
        self.reset_energy_frame()

        return row

    def reset_energy_frame(self, widget=None):
        frame = self['energy frame']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        scc = self['SCC'].get() == 'Yes'

        widgets = []
        widgets1 = []
        widgets2 = []

        row = 0
        self['SCC'].grid(row=row, column=0, columnspan=3, sticky=tk.EW)
        widgets.append(self['SCC'])
        row += 1
        if scc:
            for widget in ('SCCTolerance', 'MaxSCCIterations', 'ThirdOrder'):
                self[widget].grid(
                    row=row, column=1, columnspan=2, sticky=tk.EW
                )
                widgets1.append(self[widget])
                row += 1

            self['HCorrection'].grid(
                row=row, column=1, columnspan=2, sticky=tk.EW
            )
            widgets1.append(self['HCorrection'])
            row += 1

            hcorrection = self['HCorrection'].get()
            if hcorrection == 'Damping':
                self['Damping Exponent'].grid(row=row, column=1, sticky=tk.EW)
                widgets2.append(self['Damping Exponent'])
                row += 1

        sw.align_labels(widgets)
        sw.align_labels(widgets1)
        sw.align_labels(widgets2)

        return row
