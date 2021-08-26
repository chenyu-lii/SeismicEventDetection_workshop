#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from obspy import read, Stream
from os.path import join
import os
import glob
import time

time1 = time.time()

inputdir = "/home/eos_data/SEISMIC_DATA_TECTONICS/2018/MM/"
outputdir = "./MM_mseed_day/"
sta_file = './station.dat'
with open(sta_file, 'r') as f_sta:
	stas = [line.split()[0] for line in f_sta]

days = range(11, 12)

for sta in stas:
	inputdir_sta = join(inputdir, sta)
	if os.path.exists(inputdir_sta):
		outputdir_sta = join(outputdir, sta)
		if not os.path.exists(outputdir_sta):
			os.makedirs(outputdir_sta)
		
		time3 = time.time()
		
		comp_dir = glob.glob(inputdir_sta+'/*Z.D')
		if comp_dir != []:
			inputdir_comp = comp_dir[0]

			for day in days:

				files = glob.glob(inputdir_comp + '/{:03d}'.format(day) + '/*Z.D*.mseed')
				#print(files)
				files.sort()
				st_all = Stream()
				st_z = Stream()
				st_e = Stream()
				st_n = Stream()
				for ifile in range(len(files)):
					
					st = read(files[ifile])
					if  not os.path.exists(files[ifile]):
						print(files[ifile])

					for tr in st:
						tr.stats.location = '--'
					if len(st) < 10:
						st.sort(['starttime'])
						st.merge(method=1,fill_value=0)
						st_z += st
						#st[-1].stats.location = '--'
					file_E = files[ifile].replace('Z.D', 'E.D')
					#print(file_E)
					if not os.path.exists(file_E):
						print(file_E)
					
					if os.path.exists(file_E):
						st = read(file_E)
						for tr in st:
							tr.stats.location = '--'
						if len(st) < 10:
							st.sort(['starttime'])
							st.merge(method=1,fill_value=0)
							st_e += st
					file_N = files[ifile].replace('Z.D', 'N.D')
					if not os.path.exists(file_N):
						print(file_N)
					if os.path.exists(file_N):
						st = read(file_N)
						for tr in st:
							tr.stats.location = '--'
						if len(st) < 10:
							st.sort(['starttime'])
							st.merge(method=1,fill_value=0)
							st_n += st
				st_e.sort(['starttime'])
				st_e.merge(method=1,fill_value=0)
				st_n.sort(['starttime'])
				st_n.merge(method=1,fill_value=0)
				st_z.sort(['starttime'])
				st_z.merge(method=1,fill_value=0)
				st_all += st_e 
				st_all += st_n
				st_all += st_z 
				#st_all.sort(['starttime'])
				#st_all.merge(method=1,fill_value=0)

				if len(st_all) > 0:
					print('station = {}, day = {:03d}, nfile= {:2d}'.format(sta, day, len(st_all)))

				if len(st_all) > 0:
					st_all.trim(min([tr.stats.starttime for tr in st_all]),
							max([tr.stats.endtime for tr in st_all]),
							pad=True, fill_value=0)
					min_starttime = min([tr.stats.starttime for tr in st_all])
					max_endtime = max([tr.stats.endtime for tr in st_all])

					for ifile in range(len(st_all)):
						#os.remove(filenames[ifile])
						network = st_all[ifile].stats.network
						station = st_all[ifile].stats.station
						#starttime1 = st_all[ifile].stats.starttime
						starttime1 = min_starttime
						starttime = starttime1.strftime("%Y%m%dT%H%M%SZ")
						#endtime1 = st_all[ifile].stats.endtime #+ st[0].stats.delta
						endtime1 = max_endtime
						endtime = endtime1.strftime("%Y%m%dT%H%M%SZ")
						channel = st_all[ifile].stats.channel
						location = st_all[ifile].stats.location
						newfile = network + "." + station + "." + location + "." + channel + "__" + starttime + "__" + endtime + ".mseed"

						newfile1 = outputdir_sta + '/' +  newfile
						st_all[ifile].write(newfile1, format='MSEED')
	
		time4 = time.time()
		print("time elasped: %#.2fs"%(time4-time3))


time2 = time.time()
print("time elasped: %#.2fs"%(time2-time1))
