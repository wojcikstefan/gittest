# Test with:
# mkdir test_root
# mkdir test_root/test1
# mkdir test_root/test2
# touch test_root/some_file.wma
# touch test_root/some_file.mp3
# touch test_root/some_other_file.wma
# touch test_root/test1/some_file_deeper.wma
# touch test_root/test2/some_file_deeper.wma
# touch test_root/test2/some_file_deeper.mp3
# Expected to delete:
#   test_root/some_file.wma
#   touch test_root/test2/some_file_deeper.wma

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='Path to the root directory where the WMA/MP3 files are stored')
parser.add_argument('--confirm', action='store_true', help='Confirm that you want to delete the files (otherwise a dry run is performed)')
args = parser.parse_args()

if not os.path.exists(args.path):
    print "Path doesn't exist: %s" % args.path

def delete_or_skip(filepath):
    # skip immediately if it's not a WMA file
    if not filepath.endswith('.wma'):
        return

    if has_duplicate(filepath):
        print 'Deleted: %s has an equivalent MP3 file.' % filepath
        if args.confirm:
            os.remove(filepath)
    else:
        print 'Skipped: %s has no equivalent MP3 file.' % filepath

def has_duplicate(filepath):
    mp3_filepath = filepath[:-4] + '.mp3'
    return os.path.exists(mp3_filepath)


print "Traversing through %s..." % args.path

for dirpath, dirnames, filenames in os.walk(args.path):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        delete_or_skip(filepath)

