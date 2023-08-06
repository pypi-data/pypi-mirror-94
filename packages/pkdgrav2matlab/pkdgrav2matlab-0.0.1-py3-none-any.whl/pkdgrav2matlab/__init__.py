# -*- coding: utf-8 -*-


import numpy as np
import sys
from scipy.io import savemat
import argparse


au = 149597870700.
sm = 1.98847e30
t = 31556952./2./np.pi
d = 0.001


# According to: http://www.star.bris.ac.uk/jackdob/pkdgrav_data.html
# one 8 byte double for mass
# one 8 byte double for radius
# three 8 byte doubles for x,y,z (maybe other co-ords) components of position
# three 8 byte doubles for x,y,z (maybe other co-ords) components of velocity
# three 8 byte doubles for x,y,z (maybe other co-ords) components of spin
# one 4 byte integer for the colour
# one 4 byte integer for the obj identifyer (i think this is what it's for)


def read_ss(filename, to_si=True, endianess='>'):

    header_t = np.dtype([('time', endianess + 'f8'), ('npoints', endianess + 'i4'), ('padding', endianess + 'i4')]) 
    record_t = np.dtype([('mass', endianess + 'f8'),('radius', endianess + 'f8'),('position',( endianess + 'f8', 3)),
        ('velocity',(endianess + 'f8', 3)),('spin',(endianess + 'f8', 3)),('colour', endianess + 'i4'),('id', endianess + 'i4')])

    if not to_si:
        au = 1.
        sm = 1.
        t = 1.
        d = 1.

    f = open(filename, 'rb')
    header = np.frombuffer(f.read(16), dtype=header_t)
    data = np.frombuffer(f.read(96*header['npoints'][0]),dtype=(record_t, header['npoints'][0]))

    ss = dict()
    ss['mass'] = data['mass'][0] * sm  # sm -> kg
    ss['radius'] = data['radius'][0] * au  # au -> m
    ss['position'] = data['position'] * au  # au -> m 
    ss['velocity'] = data['velocity'] * au/t  # 2*pi*au/yr -> m/s
    ss['spin'] = data['spin'] * t  # 2*pi / yr -> 1/s
    ss['group_id'] = data['id'][0]
    ss['colour'] = data['colour'][0]
    ss['derived_density'] = 3./(4. * np.pi) * ss['mass'] / ss['radius']**3 * d
    ss['simulation_time'] = header['time'][0] * t
    ss['number_of_data_points'] = header['npoints'][0]

    return ss


def write_ss_to_mat(filename, ss):
    savemat(filename, ss)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Binary pkdgrav output file (ss).")
    parser.add_argument('-c', '--si', action='store_true', help="Convert to SI-units (au->m, yr/2pi->s, sm->kg, sm/au^3->g/cm^3).")
    parser.add_argument('-e', '--endianess', type=str, default='>', help="Select the endianess of the results file (this might vary depending on platform): > (big), < (littel), = (native). Default is big endian")

    args = parser.parse_args()
    write_ss_to_mat(args.filename + '.mat', read_ss(args.filename, args.si, args.endianess))


if __name__ == '__main__':
    main()


