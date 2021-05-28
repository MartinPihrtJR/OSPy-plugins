# -*- coding: utf-8 -*-
__author__ = 'Martin Pihrt'

import json
import time
import datetime
import traceback
import os
from threading import Thread, Event

import web

from ospy.options import options
from ospy.log import log
from plugins import PluginOptions, plugin_url, plugin_data_dir
from ospy.webpages import ProtectedPage
from ospy.helpers import get_rpi_revision
from ospy.helpers import datetime_string
from ospy import helpers
from ospy.stations import stations
from ospy.sensors import sensors

from ospy.webpages import showInFooter # Enable plugin to display readings in UI footer
#from ospy.webpages import showOnTimeline # Enable plugin to display station data on timeline


NAME = 'Pool Heating'
MENU =  _(u'Package: Pool Heating')
LINK = 'settings_page'


plugin_options = PluginOptions(
    NAME,
    {'enabled_a': False,   # enable or disable regulation A
     'probe_A_on': 0,      # for selector temperature probe A ON (0-5)
     'probe_A_off': 0,     # for selector temperature probe A OFF (0-5)
     'temp_a_on': 6,       # temperature for output A ON
     'temp_a_off': 3,      # temperature for output A OFF
     'control_output_A': 0,# selector for output A (0 to station count)
     'ds_name_0': '',      # name for DS probe 1 from air temp humi plugin
     'ds_name_1': '',      # name for DS probe 2 from air temp humi plugin
     'ds_name_2': '',      # name for DS probe 3 from air temp humi plugin
     'ds_name_3': '',      # name for DS probe 4 from air temp humi plugin
     'ds_name_4': '',      # name for DS probe 5 from air temp humi plugin
     'ds_name_5': '',      # name for DS probe 6 from air temp humi plugin
     'ds_count': 0,        # DS probe count from air temp humi plugin
     'reg_mm': 60,         # min for maximal runtime
     'reg_ss': 0,          # sec for maximal runtime
     'probe_A_on_sens': 0, # for selector from sensors xx - temperature ON
     'probe_A_off_sens': 0,# for selector from sensors xx - temperature OFF
     'sensor_probe': 0,    # selector for type probes: 0=none, 1=sensors, 2=air temp plugin
     'use_footer': True    # show data from plugin in footer on home page
     }
)


################################################################################
# Main function loop:                                                          #
################################################################################


class Sender(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self._stop = Event()

        self._sleep_time = 0
        self.start()

    def stop(self):
        self._stop.set()

    def update(self):
        self._sleep_time = 0

    def _sleep(self, secs):
        self._sleep_time = secs
        while self._sleep_time > 0 and not self._stop.is_set():
            time.sleep(1)
            self._sleep_time -= 1

    def _try_read(self, val):
        try:
            return val
        except:
            pass
            return -127.0            

    def run(self):
        temperature_ds = [-127,-127,-127,-127,-127,-127]
        msg_a_on = True
        msg_a_off = True              
 
        if plugin_options['use_footer']:
            temp_sw = showInFooter() #  instantiate class to enable data in footer
            temp_sw.button = "pool_heating/settings"   # button redirect on footer
            temp_sw.label =  _(u'Pool Heating')        # label on footer

        ds_a_on  = -127.0
        ds_a_off = -127.0

        millis = 0                                 # timer for clearing status on the web pages after 5 sec
        last_millis = int(round(time.time() * 1000))

        a_state = -3                               # for state in footer "Waiting."
        regulation_text = _(u'Waiting to turned on or off.')
        
        if not plugin_options['enabled_a']:
            a_state = -1                           # for state in footer "Waiting (not enabled regulation in options)."

        log.info(NAME, datetime_string() + ' ' + _(u'Waiting.'))
        end = datetime.datetime.now()

        while not self._stop.is_set():
            try:
                if plugin_options["sensor_probe"] == 2:                                        # loading probe name from plugin air_temp_humi
                    try:
                        from plugins.air_temp_humi import plugin_options as air_temp_data
                        plugin_options['ds_name_0'] = air_temp_data['label_ds0']
                        plugin_options['ds_name_1'] = air_temp_data['label_ds1']
                        plugin_options['ds_name_2'] = air_temp_data['label_ds2']
                        plugin_options['ds_name_3'] = air_temp_data['label_ds3']
                        plugin_options['ds_name_4'] = air_temp_data['label_ds4']
                        plugin_options['ds_name_5'] = air_temp_data['label_ds5']
                        plugin_options['ds_count'] = air_temp_data['ds_used']

                        from plugins.air_temp_humi import DS18B20_read_probe                    # value with temperature from probe DS1-DS6
                        temperature_ds = [DS18B20_read_probe(0), DS18B20_read_probe(1), DS18B20_read_probe(2), DS18B20_read_probe(3), DS18B20_read_probe(4), DS18B20_read_probe(5)]
                    
                    except:
                        log.error(NAME, _(u'Unable to load settings from Air Temperature and Humidity Monitor plugin! Is the plugin Air Temperature and Humidity Monitor installed and set up?'))
                        pass

                # regulation
                if plugin_options['enabled_a'] and plugin_options["sensor_probe"] != 0:# enabled regulation and selected input for probes sensor/airtemp plugin
                    if plugin_options["sensor_probe"] == 1 and sensors.count()>0:
                        sensor_on = sensors.get(int(plugin_options['probe_A_on_sens']))#  pool
                        if sensor_on.sens_type == 5:                                   # temperature sensor
                            ds_a_on = self._try_read(sensor_on.last_read_value)
                        elif sensor_on.sens_type == 6 and sensor_on.multi_type == 0:   # multitemperature sensor DS1
                            ds_a_on = self._try_read(sensor_on.last_read_value[0])
                        elif sensor_on.sens_type == 6 and sensor_on.multi_type == 1:   # multitemperature sensor DS2
                            ds_a_on = self._try_read(sensor_on.last_read_value[1])
                        elif sensor_on.sens_type == 6 and sensor_on.multi_type == 2:   # multitemperature sensor DS3
                            ds_a_on = self._try_read(sensor_on.last_read_value[2])
                        elif sensor_on.sens_type == 6 and sensor_on.multi_type == 3:   # multitemperature sensor DS4
                            ds_a_on = self._try_read(sensor_on.last_read_value[3])
                        else:
                            ds_a_on = -127.0

                        sensor_off = sensors.get(int(plugin_options['probe_A_off_sens']))#  solar
                        if sensor_off.sens_type == 5:                                    # temperature sensor
                            ds_a_off = self._try_read(sensor_off.last_read_value)
                        elif sensor_off.sens_type == 6 and sensor_off.multi_type == 0:   # multitemperature sensor DS1
                            ds_a_off = self._try_read(sensor_off.last_read_value[0])
                        elif sensor_off.sens_type == 6 and sensor_off.multi_type == 1:   # multitemperature sensor DS2
                            ds_a_off = self._try_read(sensor_off.last_read_value[1])
                        elif sensor_off.sens_type == 6 and sensor_off.multi_type == 2:   # multitemperature sensor DS3
                            ds_a_off = self._try_read(sensor_off.last_read_value[2])
                        elif sensor_off.sens_type == 6 and sensor_off.multi_type == 3:   # multitemperature sensor DS4
                            ds_a_off = self._try_read(sensor_off.last_read_value[3])
                        else:
                            ds_a_off = -127.0

                    elif plugin_options["sensor_probe"] == 2:
                        ds_a_on = temperature_ds[plugin_options['probe_A_on']]           #  pool  
                        ds_a_off = temperature_ds[plugin_options['probe_A_off']]         #  solar
                        
                    station_a = stations.get(plugin_options['control_output_A'])

                    probes_ok = True
                    if ds_a_on == -127.0 or ds_a_off == -127.0:
                        probes_ok = False
                        a_state = -2   

                    if (ds_a_off - ds_a_on) > plugin_options['temp_a_on'] and probes_ok: # ON
                        a_state = 1
                        if msg_a_on:
                            msg_a_on = False
                            msg_a_off = True
                            regulation_text = datetime_string() + ' ' + _(u'Regulation set ON.') + ' ' + ' (' + _(u'Output') + ' ' +  str(station_a.index+1) + ').'
                            log.clear(NAME) 
                            log.info(NAME, regulation_text)
                            start = datetime.datetime.now()
                            sid = station_a.index
                            end = datetime.datetime.now() + datetime.timedelta(seconds=plugin_options['reg_ss'], minutes=plugin_options['reg_mm'])
                            new_schedule = {
                                'active': True,
                                'program': -1,
                                'station': sid,
                                'program_name': _(u'Pool Heating'),
                                'fixed': True,
                                'cut_off': 0,
                                'manual': True,
                                'blocked': False,
                                'start': start,
                                'original_start': start,
                                'end': end,
                                'uid': '%s-%s-%d' % (str(start), "Manual", sid),
                                'usage': stations.get(sid).usage
                            }

                            log.start_run(new_schedule)
                            stations.activate(new_schedule['station'])

                    if (ds_a_off - ds_a_on) < plugin_options['temp_a_off'] and probes_ok: # OFF
                        a_state = 0
                        if msg_a_off:
                            msg_a_off = False
                            msg_a_on = True
                            regulation_text = datetime_string() + ' ' + _(u'Regulation set OFF.') + ' ' + ' (' + _(u'Output') + ' ' +  str(station_a.index+1) + ').'
                            log.clear(NAME)
                            log.info(NAME, regulation_text)
                            sid = station_a.index
                            stations.deactivate(sid)
                            active = log.active_runs()
                            for interval in active:
                                if interval['station'] == sid:
                                    log.finish_run(interval)

                    ### if "pool" end in schedule release msg_a_on to true in regulation for next scheduling ###
                    now = datetime.datetime.now()
                    if now > end:
                        msg_a_off = False
                        msg_a_on = True
                        if probes_ok:
                            a_state = -3

                else:
                    a_state = -1

                # footer text
                tempText = ' '

                if a_state == 0:
                    tempText += regulation_text
                if a_state == 1:
                    tempText += regulation_text
                if a_state == -1:
                    tempText = _(u'Waiting (not enabled regulation in options, or not selected input).')
                if a_state == -2:
                    tempText = _(u'Some probe shows a fault, regulation is blocked!')
                if a_state == -3:
                    tempText = _(u'Waiting.')

                if plugin_options['use_footer']:
                    temp_sw.val = tempText.encode('utf8')    # value on footer

                self._sleep(2)

                millis = int(round(time.time() * 1000))
                if (millis - last_millis) > 5000:        # 5 second to clearing status on the webpage
                    last_millis = millis
                    log.clear(NAME)
                    if plugin_options["sensor_probe"] == 1:
                        try:
                            if options.temp_unit == 'C':
                                log.info(NAME, datetime_string() + '\n' + sensor_on.name + ' (' + _(u'Pool') + u') %.1f \u2103 \n' % ds_a_on + sensor_off.name + ' ('+ _(u'Solar') + u') %.1f \u2103' % ds_a_off)
                            else:
                                log.info(NAME, datetime_string() + '\n' + sensor_on.name + ' (' + _(u'Pool') + u') %.1f \u2109 \n' % ds_a_on + sensor_off.name + ' ('+ _(u'Solar') + u') %.1f \u2103' % ds_a_off)
                        except:
                            pass
                    elif plugin_options["sensor_probe"] == 2:
                        log.info(NAME, datetime_string() + '\n' + _(u'Pool') + u' %.1f \u2103 \n' % ds_a_on + _(u'Solar') + u' %.1f \u2103' % ds_a_off)
                        
                    log.info(NAME, tempText)
 
            except Exception:
                log.error(NAME, _(u'Pool Heating plug-in') + ':\n' + traceback.format_exc())
                self._sleep(60)
          
sender = None

################################################################################
# Helper functions:                                                            #
################################################################################
def start():
    global sender
    if sender is None:
        sender = Sender()
       

def stop():
    global sender
    if sender is not None:
       sender.stop()
       sender.join()
       sender = None 


################################################################################
# Web pages:                                                                   #
################################################################################

class settings_page(ProtectedPage):
    """Load an html page for entering adjustments and deleting logs"""

    def GET(self):
    	global sender
    	
        if sender is not None:
            sender.update()           

        return self.plugin_render.pool_heating(plugin_options, log.events(NAME))

    def POST(self):
    	global sender
        plugin_options.web_update(web.input())

        if sender is not None:
            sender.update()
            log.clear(NAME)

        raise web.seeother(plugin_url(settings_page), True)
        #return self.plugin_render.pool_heating(plugin_options, log.events(NAME))  


class help_page(ProtectedPage):
    """Load an html page for help"""

    def GET(self):                
        return self.plugin_render.pool_heating_help()


class settings_json(ProtectedPage):
    """Returns plugin settings in JSON format."""

    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return json.dumps(plugin_options)