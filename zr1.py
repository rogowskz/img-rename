import EXIF
import sys

for filename in sys.argv[1:]:
 try:
  file=open(filename, 'rb')
 except:
  print "'%s': Cannot open for reading.\n" % filename
  continue

 # get the tags
 data = EXIF.process_file(file, details=False, debug=False)
 if not data:
  print '%s: No EXIF data found' % filename
  continue

 date = data['Image DateTime']
 model = data['Image Model']
 res = data['Image XResolution']
 unit = data['Image ResolutionUnit']
 speed = data['EXIF ExposureTime']
 fstop = data['EXIF FNumber']

 assert(type(fstop.values[0] is EXIF.Ratio))
 fstop = float(fstop.values[0].num) / float(fstop.values[0].den)

 print "%s: %s, %s, %s %s, F%s %s sec" % (filename, date, model, res, unit, fstop, speed)

 file.close()
 