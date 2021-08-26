'''
PBS job test run, import a module
'''

#import eqt
import obspy
from datetime import datetime

run_end_time=datetime.now()
print('Obspy module imported successfully')
print('Finished '+str(run_end_time))
