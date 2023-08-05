import pathlib

import cffi

ext_dir = pathlib.Path(__file__).parent.joinpath('ext')
sources = [ext_dir.joinpath(s).as_posix() for s in ['Bra.c', 'Bra86.c', 'BraIA64.c']]

ffibuilder = cffi.FFI()


# 7zTypes.h
ffibuilder.cdef(r'''
typedef unsigned char Byte;
typedef unsigned short UInt16;
typedef unsigned int UInt32;
typedef unsigned long long UInt64;
typedef size_t SizeT;
''')

# Bra.h
ffibuilder.cdef(r'''
SizeT x86_Convert(Byte *data, SizeT size, UInt32 ip, UInt32 *state, int encoding);
SizeT ARM_Convert(Byte *data, SizeT size, UInt32 ip, int encoding);
SizeT ARMT_Convert(Byte *data, SizeT size, UInt32 ip, int encoding);
SizeT PPC_Convert(Byte *data, SizeT size, UInt32 ip, int encoding);
SizeT SPARC_Convert(Byte *data, SizeT size, UInt32 ip, int encoding);
SizeT IA64_Convert(Byte *data, SizeT size, UInt32 ip, int encoding);
''')

ffibuilder.set_source('_bcj', r'''
#include "Bra.h"
''', sources=sources, include_dirs=[ext_dir])


if __name__ == "__main__":    # not when running with setuptools
    ffibuilder.compile(verbose=True)
