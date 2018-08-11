#!python3
# coding: utf8

import sys
import os
import time 

import serial
import argparse

import prema


DMM  = None
args = None

tc_channels    = []
pt100_channels = []
lv_channels    = []
r_channels     = []


def parse_arguments():
	global args, tc_channels, pt100_channels, lv_channels, r_channels
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument("--port", "-p", required=True, 
		help="define a COM port, e.g. --port COM1")
#	parser.add_argument("--interval", "-i", default=1.0, type=float, 
#		help="acquisition delay (seconds)")
	parser.add_argument("--output", "-o",  
		help="output file")
	parser.add_argument("--thermocouple-channels", "-tc", type=int, nargs='+', 
		help="list voltage channels from the scanner to be read (300 mV range).")
	parser.add_argument("--pt100-channels", "-pt", type=int, nargs='+', 
		help="list PT100 channels from the scanner to be read.")
	parser.add_argument("--low-voltage-channels", "-lv", type=int, nargs='+', 
		help="list voltage channels from the scanner to be read (30 V range)")
	parser.add_argument("--resistance-channels", "-r", type=int, nargs='+', 
		help="list 4-wire resistance channels to be read (autorange).")
	parser.add_argument('--verbose', '-v', action='count',
		help="verbose output")
	
	args = parser.parse_args()
	tc_channels    = args.thermocouple_channels
	pt100_channels = args.pt100_channels
	lv_channels    = args.low_voltage_channels
	r_channels     = args.resistance_channels
	
	
def setup_dmm():
	global args, DMM
	DMM = prema.PremaDMM(port=args.port) # PREMA5017SC

	print("#", DMM.query("*IDN?").decode().replace("\n",""))
	DMM.send("*RST")
	time.sleep(0.5)
	DMM.display_text(" [ Remote ON ]")
	time.sleep(0.5)

	# begin init
	DMM.set_sampling_continuous(True)	
	DMM.set_scanner_mode_4W(True)

	# check thermocouple
	if tc_channels:
		for n in tc_channels:
			DMM.set_scanner_channel(n, True)
			DMM.mode_continuity(True)
			DMM.display_normal()
			time.sleep(1.2)

	# continue init
	col_labels = ["#[time]"]

	if lv_channels:	
		for n in lv_channels:
			DMM.set_scanner_channel(n, True)
			DMM.mode_voltage_dc(True)
			DMM.set_range_30V_30k_20mA(True)
			DMM.set_integration_200ms(True)
			DMM.set_autorange_off(True)
			DMM.set_filter_auto(True)
			col_labels.append("[%d:V]" % n)
	
	if tc_channels:
		for n in tc_channels:
			DMM.set_scanner_channel(n, True)
			DMM.mode_voltage_dc(True)
			DMM.set_range_300mV_300R_200uA(True)
			DMM.set_integration_200ms(True)
			DMM.set_autorange_off(True)
			DMM.set_filter_auto(True)
			col_labels.append("[%d:TC]" % n)
	
	if pt100_channels:	
		for n in pt100_channels:
			DMM.set_scanner_channel(n, True)
			DMM.mode_temperature_celsius(True)
			DMM.set_temp_sensor_PT100(True)
			DMM.set_integration_40ms(True)
			DMM.set_filter_auto(True)
			col_labels.append("[%d:PT100]" % n)
			
	if r_channels:
		for n in r_channels:
			DMM.set_scanner_channel(n, True)
			DMM.mode_resistance_4W(True)
			DMM.set_range_30V_30k_20mA(True)
			DMM.set_integration_40ms(True)
			DMM.set_filter_auto(True)
			col_labels.append("[%d:R]" % n)
			
	print("\t".join(col_labels))
	if args.output:
		if not os.path.isfile(args.output):	
			f = open(args.output, "w")
			f.write("\t".join(col_labels)+"\n")
			f.close()
		else:
			print("Warning: '%s' already exists and will be appended. Columns are not guaranteed to match." % args.output)
			f = open(args.output, "a")
			f.write("\t".join(col_labels)+"\n")
			f.close()
		
	# finalize init
	DMM.ser.reset_input_buffer()
	DMM.set_output_format_long(True)
	DMM.display_normal()	

	
def process_value():
	global args
	cells  = [str(time.time())]
	
	if lv_channels:
		for n in lv_channels:
			if args.verbose:
				print("read voltage channel %d" % n)
				print("%s\t%s\t%s" % (time.time(), v[35:37], v[0:13]))
			DMM.set_scanner_channel(n)
			time.sleep(2.0)
			v = DMM.read().decode()
			cells.append(v[0:13])
			
	if tc_channels:
		for n in tc_channels:
			if args.verbose:
				print("read TC channel %d" % n)
				print("%s\t%s\t%s" % (time.time(), v[35:37], v[0:13]))
			DMM.set_scanner_channel(n)
			time.sleep(2.0)
			v = DMM.read().decode()
			cells.append(v[0:13])
			
	if pt100_channels:
		for n in pt100_channels:
			if args.verbose:
				print("read PT channel %d" % n)
				print("%s\t%s\t%s" % (time.time(), v[35:37], v[0:13]))
			DMM.set_scanner_channel(n)
			time.sleep(2.5)
			v = DMM.read().decode()	
			cells.append(v[0:13])
			
	if r_channels:
		for n in r_channels:
			if args.verbose:
				print("read 4-wire R channel %d" % n)
				print("%s\t%s\t%s" % (time.time(), v[35:37], v[0:13]))
			DMM.set_scanner_channel(n)
			time.sleep(2.0)
			v = DMM.read().decode()	
			cells.append(v[0:13])

	print("\t".join(cells))
	if args.output:
		f = open(args.output, "a")
		f.write("\t".join(cells)+"\n")
		f.close()
	
	
def main():
	global args, DMM
	parse_arguments()
	setup_dmm()
	try:
		while True:
			process_value()
	except KeyboardInterrupt:
		pass
	DMM.close()
	print("end.")

	
if __name__ == "__main__":
	main()

