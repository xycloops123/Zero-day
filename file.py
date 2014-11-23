# File Deduplication
# Given a Directory (i.e. /dropbox/), traverse through it and all of it's sub-directories and detect any file duplications.
# The file names may be different but the contents may be identical.
# Output could be a nested list output of identical files - i.e. [[/dropbox/r2, /dropbox/a1/db], ...]
# 


import os
import sys
import stat
import md5

filesize1 = {}

def directory(args, dirname, fnames):
    ds = os.getcwd();
    os.chdir(dirname);
    
    for f in fnames:
        if not os.path.isfile(f):
            continue
        size = os.stat(f)[stat.ST_SIZE]
        if size < 100:
            continue
        if filesize1.has_key(size):
            
            a = filesize1[size]
        else:
            a = []
            filesize1[size] = a
        a.append(os.path.join(dirname, f))
        
        os.chdir(d)
        
for x in sys.argv[1:]:
    print 'Scan for directory "%s"....' %x
    os.path.walk(x, directory, filesize1)
    
print 'Find potential duplicates....'
potentialdupe = []
potentialcount = 0
filetrue = type(True)


sizes = filesize1.keys()
sizes.sort()
for k in sizes:
    inFiles = filesize1[k]
    outfiles = []
    hashes = {}
    if len(inFiles) is 1:
        continue
    print 'testing %d files of size %d' % (len(inFiles), k)
    
    for filename in inFiles:
        if not os.path.isFile(filename):
            continue
        afile = file(filename, 'r')
        hasher = md5.new(afile.read(1024))
        hashvalue = hasher.digest()
        if hashes.has_key(hashvalue):
            x = hashes[hashvalue]
            if type(x) is not filetrue:
                outfiles.append(hashes[hashvalue])
                hashes[hashvalue] = True
                outfiles.append(filename)
                
            else:
                hashes[hashvalue] = filename
                afile.close()
        if len(outfiles):
            potentialdupe.append(outfiles)
            potentialcount = potentialcount + len(outfiles)
            
del filesize1

print 'found %d set of potential duplicates' % potentialcount

print 'found potential dupes' % potentialdupe


                
    
    
    
    
        
        
       

