import glob
import os

# import time

# These  lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_folder1 = glob.glob(base_dir + '28*')[1]

device_file = device_folder + '/w1_slave'
device_file1 = device_folder1 + '/w1_slave'


def read_rom():
    name_file = device_folder+'/name'
    f = open(name_file, 'r')
    # print('f:',f)
    return f.readline()


def read_rom1():
    name_file1 = device_folder1+'/name'
    g = open(name_file1, 'r')
    # print('g:',g)
    return g.readline()


# reading temperature from folder

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    # print('raw_f',lines)
    f.close()
    return lines


def read_temp_raw1():
    g = open(device_file1, 'r')
    lines1 = g.readlines()
    # print('raw_g',lines1)
    g.close()
    return lines1


# converting the temperature data to human readable form

def read_temp_sens1():
    lines = read_temp_raw()
    while lines[1].strip()[-3:] != 'YES':
        lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


def read_temp_sens2():
    lines1 = read_temp_raw1()
    while lines1[1].strip()[-3:] != 'YES':
        lines1 = read_temp_raw1()
        equals_pos1 = lines1[1].find('t=')
        temp_string1 = lines1[1][equals_pos1 + 2:]
        temp_c1 = float(temp_string1) / 1000.0
        # temp_f1 = temp_c1 * 9.0 / 5.0 + 32.0
        return temp_c1


'''while True:
    # READING TEMPERATURE DATA AND PRINTINTING THE VALUES OF INDIVIDUAL SENSOR
    # print(' C1=%3.3f  F1=%3.3f'% read_temp())
    temp = float(read_temp())
    print(temp, type(temp))
    # print(' C2=%3.3f  F2=%3.3f'% read_temp1())
    time.sleep(1)
'''
