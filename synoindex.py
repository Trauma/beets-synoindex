from beets.plugins import BeetsPlugin
from beets import config

import subprocess
import os

# Global variables with default values
#  These values can be overwrite by beets config file
debug = False

cmd_synoindex_add_item   = ['dummycommand', '-a']
cmd_synoindex_add_album  = ['dummycommand', '-A']
cmd_synoindex_del_item   = ['dummycommand', '-d']
cmd_synoindex_move_item  = ['dummycommand', '-n']

# SynoIndex class
class SynoIndex(BeetsPlugin):
    def __init__(self):
        super(SynoIndex, self).__init__()
        self.register_listener('pluginload', self.loaded)
        self.register_listener('item_imported', self.item_imported)
        self.register_listener('album_imported', self.album_imported)
        self.register_listener('item_removed', self.item_removed)
        self.register_listener('item_moved', self.item_moved)
        self.config.add({
            u'debug': False,
            u'command': '/usr/syno/bin/synoindex'
        })

    def loaded(self):
        self._log.info('Plugin loaded!')
        global debug
        debug = config['synoindex']['debug'].get(bool)
        synoindex_command = config['synoindex']['command'].get()
        if debug: print 'SynoIndex plugin will use: ' + synoindex_command
        cmd_synoindex_add_item[0] = synoindex_command
        cmd_synoindex_add_album[0] = synoindex_command
        cmd_synoindex_del_item[0] = synoindex_command
        cmd_synoindex_move_item[0] = synoindex_command

    def item_imported(self, lib, item):
        if debug: print 'item_imported: lib: ' + str(lib) + ' item: ' + str(item)
        synoindex_add_item(item['path'])

    def album_imported(self, lib, album):
        if debug: print 'album_imported: lib: ' + str(lib) + ' album: ' + str(album)
        synoindex_add_album(album['path'])

    def item_removed(self, item):
        if debug: print 'item_removed: item: ' + str(item)
        synoindex_del_item(item['path'])

    def item_moved(self, item, source, destination):
        if debug: print 'item_moved: destination: ' + destination
        if source == destination:
            if debug: print 'item_moved: same source and destination'
            """ This occurs when 'beet modify QUERY field=newvalue' """
            """ There is no dedicated function with 'synoindex' command to update metadatas for a file but a move with same destination and source works. """
            """ Unfortunatly, this also occurs when running 'beet move' or 'beet move -a', I think this case is a bug... """
            """ So, you will need to comment this line to speedup the process if you do a 'beet move' on whole music library but only some need to be updated... """
            synonindex_move_item(source, destination)
        else:
            if debug: print 'item_moved: item:' + str(item)
            #print 'item_moved: item: ' + str(item) + ' source: ' + source + ' destination: ' + destination
            synonindex_move_item(source, destination)

# Helper fcts
def quote(s):
    return '"'+s+'"'

def execute(cmd):
    if debug:
        print cmd
    subprocess.call(cmd)

# Helpers: construct full command, then execute it
def synoindex_add_album(filename):
    if os.path.isdir(filename):
        cmd = list(cmd_synoindex_add_album)
        cmd.append(quote(filename))
        execute(cmd)
    else:
        print 'Error: ' + quote(filename) + ' does not exist.'

def synoindex_add_item(filename):
    if os.path.isfile(filename):
        cmd = list(cmd_synoindex_add_item)
        cmd.append(quote(filename))
        execute(cmd)
    else:
        print 'Error: ' + quote(filename) + ' does not exist.'

def synoindex_del_item(filename):
    if os.path.isfile(filename):
        cmd = list(cmd_synoindex_del_item)
        cmd.append(quote(filename))
        execute(cmd)
    else:
        print 'Error: ' + quote(filename) + ' does not exist.'

def synonindex_move_item(source, destination):
    if os.path.isfile(destination):
        cmd = list(cmd_synoindex_move_item)
        cmd.append(quote(destination))
        cmd.append(quote(source))
        execute(cmd)
    else:
        print 'Error: ' + quote(destination) + ' does not exist.'
