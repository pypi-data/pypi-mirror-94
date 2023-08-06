from PyQt5.QtCore import pyqtSignal
from easydict import EasyDict as edict
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo, DataFromPlugins
from pymodaq.daq_viewer.utility_classes import DAQ_Viewer_base
from collections import OrderedDict
import numpy as np
from enum import IntEnum
from pymodaq.daq_viewer.utility_classes import comon_parameters

class DAQ_0DViewer_Keithley_Pico_type(IntEnum):
    """
        Enum class of Keithley_Pico_type

        =============== =========
        **Attributes**  **Type**
        *Pico_648X*     int
        *Pico_6430*     int
        *Pico_6514*     int
        =============== =========
    """
    Pico_648X=0
    Pico_6430=1
    Pico_6514=2
    @classmethod
    def names(cls):
        return [name for name, member in cls.__members__.items()]


class DAQ_0DViewer_Keithley_Pico(DAQ_Viewer_base):
    """
        ==================== ========================
        **Attributes**        **Type**
        *data_grabed_signal*  instance of pyqtSignal
        *VISA_rm*             ResourceManager
        *com_ports*           
        *params*              dictionnary list
        *keithley*
        *settings*
        ==================== ========================
    """
    data_grabed_signal=pyqtSignal(list)

    ##checking VISA ressources

    from pyvisa import ResourceManager
    VISA_rm=ResourceManager()
    com_ports=list(VISA_rm.list_resources())
#    import serial.tools.list_ports;
#    com_ports=[comport.device for comport in serial.tools.list_ports.comports()]

    params= comon_parameters+[
              {'title': 'VISA:','name': 'VISA_ressources', 'type': 'list', 'values': com_ports },
             {'title': 'Keithley Type:','name': 'keithley_type', 'type': 'list', 'values': DAQ_0DViewer_Keithley_Pico_type.names()},
             {'title': 'Id:', 'name': 'id', 'type': 'text', 'value': "" },
             {'title': 'Timeout (ms):', 'name': 'timeout', 'type': 'int', 'value': 10000, 'default': 10000, 'min': 2000 },
             {'title': 'Configuration:', 'name': 'config', 'type': 'group', 'children':[
                 {'title': 'Meas. type:', 'name': 'meas_type', 'type': 'list', 'value': 'CURR', 'default': 'CURR', 'values': ['CURR','VOLT','RES','CHAR'] },


                 ] },
            ]

    def __init__(self,parent=None,params_state=None):
        super(DAQ_0DViewer_Keithley_Pico,self).__init__(parent,params_state)
        from visa import ResourceManager
        self.VISA_rm=ResourceManager()
        self.controller=None

    def ini_detector(self, controller=None):
        """
            Initialisation procedure of the detector.

            Returns
            -------

                The initialized status.

            See Also
            --------
            daq_utils.ThreadCommand
        """
        self.status.update(edict(initialized=False,info="",x_axis=None,y_axis=None,controller=None))
        try:

            if self.settings.child(('controller_status')).value()=="Slave":
                if controller is None: 
                    raise Exception('no controller has been defined externally while this detector is a slave one')
                else:
                    self.controller=controller
            else:
                self.controller=self.VISA_rm.open_resource(self.settings.child(('VISA_ressources')).value(), read_termination='\r')

            self.controller.timeout=self.settings.child(('timeout')).value()

            self.controller.write("*rst; status:preset; *cls;")
            txt=self.controller.query('*IDN?')
            self.settings.child(('id')).setValue(txt)
            self.controller.write('CONF:'+self.settings.child('config','meas_type').value())
            self.controller.write(':FORM:ELEM READ;DATA ASC;')
            self.controller.write('ARM:SOUR IMM;')
            self.controller.write('ARM:COUNt 1;')
            self.controller.write('TRIG:SOUR IMM;')
            #%%
            data=self.controller.query_ascii_values('READ?')

            self.status.initialized=True
            self.status.controller=self.controller
            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status',[getLineInfo()+ str(e),'log']))
            self.status.info=getLineInfo()+ str(e)
            self.status.initialized=False
            return self.status


    def commit_settings(self, param):
        """
            Activate the parameters changes in the hardware.

            =============== ================================= ============================
            **Parameters**   **Type**                         **Description**
            *param*         instance of pyqtgraph.parameter   The parameter to be checked.
            =============== ================================= ============================

            See Also
            --------
            daq_utils.ThreadCommand
        """
        try:
            if param.name()=='timeout':
                self.controller.timeout=self.settings.child(('timeout')).value()
            elif param.name()=='meas_type':
                self.controller.write('CONF:'+param.value())


        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status',[getLineInfo()+ str(e),'log']))

    def close(self):
        """
            close the current instance of Keithley viewer.
        """
        self.controller.close()

    def grab_data(self, Naverage=1, **kwargs):
        """
            | Start new acquisition.
            | grab the current values with keithley profile procedure.
            | Send the data_grabed_signal once done.

            =============== ======== ===============================================
            **Parameters**  **Type**  **Description**
            *Naverage*      int       Number of values to average
            =============== ======== ===============================================
        """
        data_tot=[]
        self.controller.write('ARM:SOUR IMM;')
        self.controller.write('ARM:COUNt 1;')
        self.controller.write('TRIG:SOUR IMM;')
        self.controller.write('TRIG:COUN {:};'.format(Naverage))
        data_tot=self.controller.query_ascii_values('READ?')
        #for ind in range(Naverage):
        #    data_tot.append(self.controller.query_ascii_values('READ?')[0])
        data_tot=[np.array([np.mean(np.array(data_tot))])]
        self.data_grabed_signal.emit([DataFromPlugins(name='Keithley',data=data_tot, dim='Data0D')])


    def stop(self):
        """
            not implemented?
        """
        return ""
