import EXIF
import sys
import os
import shutil

import time
import datetime

srcdirpath = sys.argv[1]
tgtdirpath = sys.argv[2]
camera_model = sys.argv[3]
shift_hours = sys.argv[4] # 6
shift_minutes = sys.argv[5] # 0
shift_seconds = sys.argv[6] # 0
postfix_tag = sys.argv[7] # "Szwajcaria - Renata"


dfiles = {}

for fname in os.listdir( srcdirpath ):
    fpath = os.path.join( srcdirpath, fname )
    print 'Reading picture data from: %s' % fpath
    
    try:
        fle = open( fpath, 'rb' )
    except:
        print "ERROR: Cannot open for reading: %s" % fpath
        sys.exit()

    # get the tags
    data = EXIF.process_file( fle, details=False, debug=False )
    if not data:
        print 'ERROR: No EXIF data found in: %s' % fpath
        sys.exit()

    #picdate = data['Image DateTime']
    picdate = data['EXIF DateTimeOriginal']
    cameramodel = data['Image Model']

    in_time_format = "%Y:%m:%d %H:%M:%S"
    tstamp = datetime.datetime( *( time.strptime( picdate.values, in_time_format )[0:6] ) ) 

    tstamp = tstamp + datetime.timedelta( hours=int( shift_hours ), minutes=int( shift_minutes ), seconds=int( shift_seconds ) )
    str_tstamp = str( tstamp )
    str_tstamp = str_tstamp.replace( '-', ':' )
    
    if str_tstamp in dfiles.keys():
        print 'Duplicate tstamp in: %s and %s' % ( fpath, dfiles[ str_tstamp ] )
        sys.exit()
    else:
        dfiles[ str_tstamp ] = (fpath, cameramodel.values.strip())

    fle.close()

timestamps = dfiles.keys()
timestamps.sort()

print "Start renaming loop."
for tstamp in timestamps:

    oldpath, cameramodel = dfiles[ tstamp ]
    if cameramodel != camera_model:
        continue
    fpath, fname = os.path.split( oldpath )
    ext = os.path.splitext( fname )[1]

    picdate, pictime = tstamp.split()
    picdate = picdate.replace(':', '-')
    hh, mm, ss = pictime.split(':')
    pictime = '%sh %sm %ss' % (hh, mm, ss)

    new_name = '%s %s %s%s' % (picdate, pictime, postfix_tag, ext)
    newpath = os.path.join( tgtdirpath, new_name )

    try:
        print 'Renaming:', oldpath, tstamp, '->', newpath
        shutil.copy( oldpath, newpath )
        pass
    except:
        print 'ERROR: Cannot rename from: %s to: %s' % (oldpath, newpath)
        if os.path.isfile( newpath ):
            print "The following file already exists: %s" % newpath
        else:
            print "Cause unknown."
        sys.exit()
        
print "SUCCESS. End renaming loop."
    

       