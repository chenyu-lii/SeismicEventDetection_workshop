#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

station_list = dict()
#channel_list = ["EHZ", "EHN", "EHE"]

sta_file = 'station.dat'

channel_list = ["HLE", "HLN", "HLZ"]

with open(sta_file, 'r') as f_sta:
	for line in f_sta:
		sta, network, lat, lon, ele = line.split()
		station_list[sta] = {"network": network,
							"channels": channel_list,
							"coords": [float(lat), float(lon), float(ele)]}

with open('station_list.json','w') as fp:
	json.dump(station_list, fp)

