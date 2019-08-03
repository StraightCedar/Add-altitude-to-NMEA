#!/usr/bin/python
# coding: UTF-8

import sys
from sys import argv
import os
import urllib.request
import json
from tqdm import tqdm

# Show usage.
def ShowUsage():
    #print("Usage: python " + os.path.basename(__file__) + " input-nmea-file-name <output-nmea-file-name>")
    print("Usage: (python) " + os.path.basename(sys.argv[0]) + " input-nmea-file-name <output-nmea-file-name>")

# Get input & output file names.
def GetInputFileName():
    # Get input file name.
    if len(sys.argv) < 2:
        ShowUsage()
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = ''
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        name_body, name_ext = os.path.splitext(input_file)
        output_file = '.'.join([name_body+'_with_alt', 'nmea'])
    print('in = %s, out = %s' % (input_file, output_file) )
    return(input_file, output_file)

# Get altitude from latitude and longitude
def GetAltitude(dd_lat, dd_lon):
    url = 'http://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php?lon=' + str(dd_lon) + '&lat=' + str(dd_lat) + '&outtype=JSON'
    read_obj = urllib.request.urlopen(url)
    response = read_obj.read()
    #dec_str = response.decode('unicode-escape')
    data = json.loads(response.decode())
    return(data['elevation'])

# Index of NMEA GPGGA
IDX_UTC         = 1    # hhmmss.ss
IDX_LATITUDE    = 2    # 緯度 dddmm.mmmm
IDX_LONGITUDE   = 4    # 経度 dddmm.mmmm
IDX_ANTENA_ALT  = 9

# Get latitude and longitude in ddd.dddd
def GetLatAndLon(gpgga_arr):
    lat = float(gpgga_arr[IDX_LATITUDE])
    lon = float(gpgga_arr[IDX_LONGITUDE])
    lat_q, lat_mod = divmod(lat, 100)
    lon_q, lon_mod = divmod(lon, 100)
#    print('lat = %5.4f, lat_q = %d, lat_mod = %2.4f' % (lat, lat_q, lat_mod))
#    print('lon = %5.4f, lon_q = %d, lon_mod = %2.4f' % (lon, lon_q, lon_mod))
    dd_lat = lat_q + lat_mod / 60
    dd_lon = lon_q + lon_mod / 60
#    print('dd_lat = %f, dd_lon = %f' % (dd_lat, dd_lon))
    return(dd_lat, dd_lon)

# Get altitude added GPGGA string.
def GetUpdatedGpgga(gpgga_arr, altitude):
    gpgga_arr[IDX_ANTENA_ALT] = str(altitude)
    gpgga_byte = ','.join(gpgga_arr).encode()
#    print(gpgga_byte)
    # Make updated check sum
    ch_sum = 0
    for b_char in gpgga_byte:
        if b_char == b'$':
            continue
        ch_sum = ch_sum ^ b_char
#    print(format(ch_sum, '02x'))
    new_gpgga_str = ','.join(gpgga_arr) + '*%02x' % ch_sum
#    print('new_gpgga_str = %s' % new_gpgga_str)
    return(new_gpgga_str)

# Get splited GPGGA gfactors as an array.
# Check sum is removed.
def GetGpggaArray(gpgga_str):
    gpgga_arr = gpgga_str.split(',')
    gpgga_arr[-1] = gpgga_arr[-1].split('*')[0]
    return(gpgga_arr)

# Output altitude added NMEA file.
def OutputAltitude(input_file, output_file):
    # Prepare Progress bar
    total_line = sum([1 for _ in open(input_file)])
    pbar = tqdm(total = total_line)
    # Prepare Output file
    of = open(output_file, "w")
    # Scan input file.
    with open(input_file, "r") as f:
        for line in f:
            nmea_str = line.strip()
            if '$GPGGA' == nmea_str[0:6]:
                gpgga_arr = GetGpggaArray(nmea_str)
#                print(gpgga_arr)
                dd_lat, dd_lon = GetLatAndLon(gpgga_arr)
                altitude = GetAltitude(dd_lat, dd_lon)
#                print(altitude)
                nmea_str = GetUpdatedGpgga(gpgga_arr, altitude)
            of.write(nmea_str + '\n')
            pbar.update(1)
    of.close()
    pbar.close()
            
# Main
if __name__ == "__main__":
    input_file, output_file = GetInputFileName()
    OutputAltitude(input_file, output_file)


                

