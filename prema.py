#!python3
# coding: utf8

import serial
import time 

class PremaDMM:
	__port__ = None
	ser = None
	
	def __init__(self, port, timeout=0.2):
		self.__port__ = port
		self.ser = serial.Serial(port, 9600, timeout=timeout) # 9600,8,N,1
		self.ser.reset_input_buffer()
		self.ser.write(0x0D)
		
	def close(self):
		self.ser.close()
		
	def send(self, s, verbose=False, info=""):
		if verbose:
			self.display_text(info)
		s = s + "\n"
		self.ser.write(s.encode("utf-8"))
		if verbose:
			time.sleep(0.35)

	def query(self, s):
		self.send(s)
		result = self.ser.read(size=4096)
		return result

	def display_normal(self):
		self.send("D0")
		
	def display_text(self, s):
		self.send('D1"%s"' % s)
	
	def mode_voltage_dc(self, show_text=False):
		self.send("VD", verbose=show_text, info="Mode: Volt DC")
		
	def mode_voltage_ac(self, show_text=False):
		self.send("VA", verbose=show_text, info="Mode: Volt AC")
		
	def mode_voltage_mixed(self, show_text=False):
		self.send("VC", verbose=show_text, info="Mode: Volt AC+DC")
		
	def mode_resistance_2W(self, show_text=False):
		self.send("O2", verbose=show_text, info="Mode: R 2-wire")
		
	def mode_resistance_4W(self, show_text=False):
		self.send("O4", verbose=show_text, info="Mode: R 4-wire")
		
	def mode_current_dc(self, show_text=False):
		self.send("ID", verbose=show_text, info="Mode: Curr DC")
		
	def mode_current_ac(self, show_text=False):
		self.send("IA", verbose=show_text, info="Mode: Curr AC")

	def mode_temperature_celsius(self, show_text=False):
		self.send("TC", verbose=show_text, info="Mode:TCelsius")
		
	def mode_temperature_fahrenheit(self, show_text=False):
		self.send("TF", verbose=show_text, info="Mode:TFahrenheit")
		
	def mode_temperature_kelvin(self, show_text=False):
		self.send("TK", verbose=show_text, info="Mode:TKelvin")
		
	def set_temp_sensor_PT10(self, show_text=False):
		self.send("SL1", verbose=show_text, info="T-Sens: PT10")
		
	def set_temp_sensor_PT25(self, show_text=False):
		self.send("SL2", verbose=show_text, info="T-Sens: PT25")
		
	def set_temp_sensor_PT100(self, show_text=False):
		self.send("SL3", verbose=show_text, info="T-Sens: PT100")
		
	def set_temp_sensor_PT500(self, show_text=False):
		self.send("SL4", verbose=show_text, info="T-Sens: PT500")
		
	def set_temp_sensor_PT1000(self, show_text=False):
		self.send("SL5", verbose=show_text, info="T-Sens: PT1000")
		
	def set_temp_sensor_user_calib(self, show_text=False):
		self.send("SL6", verbose=show_text, info="T-Sens: user cal")
		
	def get_temp_sensor_type(self):
		return self.query("SL?")
		
	def mode_frequency(self, show_text=False):
		self.send("FQ", verbose=show_text, info="Mode: Freqency")
		
	def mode_continuity(self, show_text=False):
		self.send("CO", verbose=show_text, info="Mode: Cont.")	

	def set_program_offset(self, show_text=False):
		self.send("P01", verbose=show_text, info="Prog: Offset")		

	def set_program_ax_b(self, show_text=False):
		self.send("P02", verbose=show_text, info="Prog: ax + b")		
	
	def set_program_ratio(self, show_text=False):
		self.send("P03", verbose=show_text, info="Prog: ratio")		
	
	def set_program_deviation(self, show_text=False):
		self.send("P04", verbose=show_text, info="Prog: deviatn")		
	
	def set_autorange_off(self, show_text=False):
		self.send("A0", verbose=show_text, info="Autorange: OFF")		

	def set_autorange_on(self, show_text=False):
		self.send("A1", verbose=show_text, info="Autorange: ON")		
	
	def set_range_300mV_300R_200uA(self, show_text=False):
		self.send("R1", verbose=show_text, info="Range: 300 mV")
		
	def set_range_3V_3k_2mA(self, show_text=False):
		self.send("R2", verbose=show_text, info="Range: 3 V")
		
	def set_range_30V_30k_20mA(self, show_text=False):
		self.send("R3", verbose=show_text, info="Range: 30 V")
		
	def set_range_300V_300k_200mA(self, show_text=False):
		self.send("R4", verbose=show_text, info="Range: 300 V")
		
	def set_range_1000V_3M_2A(self, show_text=False):
		self.send("R5", verbose=show_text, info="Range: 1000 V")
		
	def set_range_30Meg(self, show_text=False):
		self.send("R6", verbose=show_text, info="Range: 30 Meg")
		
	def set_integration_20ms(self, show_text=False):
		self.send("T0", verbose=show_text, info="Int.: 20 ms")
	
	def set_integration_40ms(self, show_text=False):
		self.send("T1", verbose=show_text, info="Int.: 40 ms")
	
	def set_integration_100ms(self, show_text=False):
		self.send("T2", verbose=show_text, info="Int.: 100 ms")
	
	def set_integration_200ms(self, show_text=False):
		self.send("T3", verbose=show_text, info="Int.: 200 ms")
	
	def set_integration_400ms(self, show_text=False):
		self.send("T4", verbose=show_text, info="Int.: 400 ms")
	
	def set_integration_1s(self, show_text=False):
		self.send("T5", verbose=show_text, info="Int.: 1 s")
	
	def set_integration_2s(self, show_text=False):
		self.send("T6", verbose=show_text, info="Int.: 2 s")
	
	def set_integration_4s(self, show_text=False):
		self.send("T7", verbose=show_text, info="Int.: 4 s")
	
	def set_integration_10s(self, show_text=False):
		self.send("T8", verbose=show_text, info="Int.: 10 s")
		
	def set_integration_20s(self, show_text=False):
		self.send("T9", verbose=show_text, info="Int.: 20 s")
	
	def set_integration_40s(self, show_text=False):
		self.send("TA", verbose=show_text, info="Int.: 40 s")
	
	def set_integration_100s(self, show_text=False):
		self.send("TB", verbose=show_text, info="Int.: 100 s")
		
	def set_filter_off(self, show_text=False):
		self.send("F0", verbose=show_text, info="Filter: OFF")	
		
	def set_filter_average(self, show_text=False):
		self.send("F1", verbose=show_text, info="Filter: avg")	
		
	def set_filter_auto(self, show_text=False):
		self.send("F2", verbose=show_text, info="Filter: auto")	
		
	def set_filter_auto_fast(self, show_text=False):
		self.send("F3", verbose=show_text, info="Filter: fast")	
		
	def set_srq_off(self, show_text=False):
		self.send("Q0", verbose=show_text, info="SRQ: OFF")	
		
	def set_srq_on(self, show_text=False):
		self.send("Q1", verbose=show_text, info="SRQ: ON")	

	def get_error_queue(self):
		return self.query("EQ?")
		
	def set_sampling_continuous(self, show_text=False):
		self.send("S0", verbose=show_text, info="Trig: cont.")	
		
	def set_sampling_single_and_trigger(self, show_text=False):
		self.send("S1", verbose=show_text, info="Trig: soft")	
		
	def set_sampling_single_ext_man_trigger(self, show_text=False):
		self.send("S2", verbose=show_text, info="Trig: man/ext")			

	def set_output_format_short(self, show_text=False):
		self.send("L0", verbose=show_text, info="Fmt: short")	

	def set_output_format_long(self, show_text=False):
		self.send("L1", verbose=show_text, info="Fmt: long")

	def do_offset_correction(self, show_text=False):
		self.send("ZO", verbose=show_text, info="Offset Corr")
		
	def set_scanner_channel(self, n, show_text=False):
		self.send("M%s" % str(int(n)).zfill(2), verbose=show_text, info="Channel %s" % str(int(n)).zfill(2))

	def set_scanner_mode_1W(self, show_text=False):
		self.send("MP1", verbose=show_text, info="Scan 1W 80CH")	

	def set_scanner_mode_2W(self, show_text=False):
		self.send("MP2", verbose=show_text, info="Scan 2W 40CH")

	def set_scanner_mode_4W(self, show_text=False):
		self.send("MP4", verbose=show_text, info="Scan 4W 20CH")	
		
	def set_calibration_9digit_string(self, s, show_text=False):
		self.send("NV%s" % s.zfill(9), verbose=show_text, info="CAL %s" % s)

	def set_calibration_7digit_key(self, s, show_text=False):
		self.send("NV\"%s\"" % s, verbose=show_text, info="CalKey %s" % s)	
		
	def set_contrast_0to9(self, d, show_text=False):
		self.send("I%d" % d, verbose=show_text, info="Contrast %d" % int(d))

	def set_scanner_mode_4W(self, show_text=False):
		self.send("MP4", verbose=show_text, info="Scan 4W 20CH")	

	def read(self):
		return self.query("RD?")

	def set_streaming_off(self, show_text=False):
		self.send("CN0", verbose=show_text, info="Streaming OFF")	
		
	def set_streaming_on(self, show_text=False):
		self.send("CN1", verbose=show_text, info="Streaming ON")	
		