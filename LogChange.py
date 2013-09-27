#!/usr/bin/env python

import re
import time

AUTHOR = r'Gui Chen'
EMAIL = r'<gui.chen@intel.com>'

def _get_info(head):
    ''' to dealwith the headline and get release info '''
    head = head.strip()
    p =re.compile(r'-')
    p_list = p.split(head)
    rels_version = p_list[0].strip()[-4:].strip()   #get release version from input head_line
    rels_time = p_list[1].strip()   #get release time from input head_line
    head_dict = {'version':rels_version, 'time': rels_time}
    return head_dict

def ToPackaging(in_file, out_file):
    ''' this function used to make mic.changes for directory packaging '''
    for line in in_file.readlines():
        if line.startswith('Release'):
            head = _get_info(line)
            head_str = '* %s %s %s - %s\n' % (head['time'], AUTHOR, EMAIL, head['version'])  #output head_line
            out_file.write(head_str)
        elif line.startswith(r'==='):
            pass
        elif line.startswith(r' *'):
            out_str = line.replace('*','-')
            out_file.write(out_str)
        else:
            out_file.write(line)
    out_file.write('  Please read README.rst for more details.')    #add the end line
            
def ToDebain(in_file, out_file):
    ''' this function used to make changelog for directory debain '''
    for line in in_file.readlines():
        if line.startswith('Release'):
            head = _get_info(line)
            head_str = 'mic (%s-1) unstable; urgency=low\n' % head['version']     #output head_line
            out_file.write(head_str)
        elif line.startswith(r'==='):
            out_file.write('\n')
        elif line.startswith('\n'):
            cur_time = '%s %s +0800' % (head['time'], time.strftime("%H:%M:%S"))
            end_line = ' -- %s %s  %s\n' % (AUTHOR, EMAIL, cur_time)     #end_line
            str_list = [line, end_line, line]
            out_file.writelines(str_list) 
        else:
            out_str = ' %s' % line
            out_file.write(out_str)

if __name__ == "__main__":
    input_log = r'./ChangeLog'
    output1 = r'./packaging/mic.changes'
    output2 = r'./debain/changelog'
    with open(input_log, 'r') as in_file, open(output1, 'w+') as out_file1:
            ToPackaging(in_file, out_file1)
    with open(input_log, 'r') as in_file, open(output2, 'w+') as out_file2:
            ToDebain(in_file, out_file2)
