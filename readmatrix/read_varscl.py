# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 15:54:14 2017

@author: thomas 
"""

import struct

kBytesPerFloat = 4
kBytesPerInt = 4
kBytesPerDouble = 8
kBytesPerChar = 1

class ReadVarscl:
    def  __init__(self,vscl_filename,vscl_type):
        if vscl_type == 'a':
            self.vscl_type = vscl_type
            self.vscl_filename = vscl_filename
        elif vscl_type == 'f':
            self.vscl_type = vscl_type
            self.vscl_filename = vscl_filename
        else:
            print 'Error 10001: the Varscl flie type should be a or f!'
            self.vscl_filename = None
            self.vscl_type = None
    def Varscl2Ascii(self,ascii_file_name):
        """
        Fuction name: 
            Varscl2Ascii           
        Fuction:
            read binary file *.varscl and convert it to ascii file
        Input parameter:
            None
        Return:   
            1
        """
        group_totnum = 0
        e_group = []
        neurton_e_group = []
        gamma_e_group = []
        mesh_bound = []
        mesh_num = []
        start_pos = 0
        end_pos = 4
        try:
            varscl_file = open(self.vscl_filename,'rb')
            ascii_file = open(ascii_file_name,'w')
        except IOError as e:
            print "Error 10004: Varscl file open error: ",e
        else:
            # read the first int
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)
            ascii_file.write('Titel: '+'\n')
            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0]) 
            #start_pos = end_pos
            #end_pos += lists[0]
            #print start_pos, end_pos
            #read first part the title of the file
            lists = self.Bin2Char(varscl_file,start_pos,end_pos)
            for ii in range(len(lists)):
                ascii_file.write('%s' % lists[ii])
            #finished the first part reading
            #start_pos = end_pos + 4
            #end_pos += 8
            (start_pos,end_pos) = self.JumptoNextpart(end_pos)    
            #print start_pos, end_pos
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)
            ascii_file.write('\n')
            # read second part
            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0]) 
            lists = self.Bin2Float(varscl_file,start_pos,end_pos)           
            for ii in range(len(lists)):
                ascii_file.write('%s\n' % lists[ii])
            # read third part    
            (start_pos,end_pos) = self.JumptoNextpart(end_pos)            
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)
            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0])
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)
            for ii in range(len(lists)):
                ascii_file.write('%s\n' % lists[ii])
            group_totnum = lists[0]
            mesh_num = lists[1:4]
            # read fourth part
            (start_pos,end_pos) = self.JumptoNextpart(end_pos)            
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)           
            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0])
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)
            for ii in range(len(lists)):
                ascii_file.write('%s\n' % lists[ii])                
            # read fifth part
            (start_pos,end_pos) = self.JumptoNextpart(end_pos)            
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)           
            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0])
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)
            for ii in range(len(lists)):
                ascii_file.write('%s\n' % lists[ii])
            # read sixth part mesh and energy group
            (start_pos,end_pos) = self.JumptoNextpart(end_pos)            
            lists = self.Bin2Int(varscl_file,start_pos,end_pos)           
            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0])
            lists = self.Bin2Float(varscl_file,start_pos,end_pos)
            for ii in range(len(lists)):
                ascii_file.write('%s\n' % lists[ii])
            idx = (mesh_num[0]+1)+(mesh_num[1]+1)+(mesh_num[2]+1)
            mesh_bound = [lists[:mesh_num[0]+1],lists[(mesh_num[0]+1):(mesh_num[0]+mesh_num[1]+2)]\
            ,lists[(mesh_num[0]+mesh_num[1]+2):idx]]
            e_group = lists[idx:idx+group_totnum]
            #print mesh_bound
            # read seventh part material mesh 
            for jj in range(mesh_num[2]):
                ascii_file.write('material num for zplane'+ str(jj+1) + '\n')
                (start_pos,end_pos) = self.JumptoNextpart(end_pos)            
                lists = self.Bin2Int(varscl_file,start_pos,end_pos)           
                (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0])
                lists = self.Bin2Int(varscl_file,start_pos,end_pos)
                for ii in range(len(lists)):
                    ascii_file.write('%s\n' % lists[ii])
            #read eighth part flux
            if group_totnum == 46:
                if self.vscl_type == 'a':
                    gamma_e_group = e_group[:19]
                    neurton_e_group = e_group[19:]
                    for kk in range(group_totnum):
                        if kk == 0:
                            ascii_file.write('#' *20 +'flux for group: ('+ '0-' \
                            + str(e_group[kk]) + ')' + '#' *20 +  '\n')
                        elif kk == 19:
                            ascii_file.write('#' *20 +'flux for group: ('+ '0-' \
                            + str(e_group[kk]) +  ')' + '#' *20 +  '\n')
                        else:
                            ascii_file.write('#' *20 +'flux for group: ('+str(e_group[kk-1]) \
                            + '-' + str(e_group[kk]) + ')' + '#' *20 +  '\n')
                        for jj in range(mesh_num[2]):
                            (start_pos,end_pos) = self.JumptoNextpart(end_pos)            
                            lists = self.Bin2Int(varscl_file,start_pos,end_pos)           
                            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0])
                            lists = self.Bin2Float(varscl_file,start_pos,end_pos)
                            ascii_file.write('-' *20 +'flux for zplane: (' \
                            + str(mesh_bound[2][jj]) + str(mesh_bound[2][jj+1]) \
                            + ')' + '-' *20 +  '\n')
                            for ii in range(len(lists)):
                                ascii_file.write('%s\n' % lists[ii])     
                else:
                    neutron_e_group = e_group[:27]
                    gamma_e_group = e_group[27:]
            else:
                if self.vscl_type == 'a':
                    gamma_e_group = e_group[:47]
                    neurton_e_group = e_group[47:]                   
                    for kk in range(group_totnum):
                        if kk == 0:
                            ascii_file.write('#' *20 +'flux for group: ('+ '0-' \
                            + str(e_group[kk]) + ')' + '#' *20 +  '\n')
                        elif kk == 47:
                            ascii_file.write('#' *20 +'flux for group: ('+ '0-' \
                            + str(e_group[kk]) +  ')' + '#' *20 +  '\n')
                        else:
                            ascii_file.write('#' *20 +'flux for group: ('+str(e_group[kk-1]) \
                            + '-' + str(e_group[kk]) + ')' + '#' *20 +  '\n')
                        for jj in range(mesh_num[2]):
                            (start_pos,end_pos) = self.JumptoNextpart(end_pos)            
                            lists = self.Bin2Int(varscl_file,start_pos,end_pos)           
                            (start_pos,end_pos) = self.ConfinePart(end_pos,lists[0])
                            lists = self.Bin2Float(varscl_file,start_pos,end_pos)
                            ascii_file.write('-' *20 +'flux for zplane: (' \
                            + str(mesh_bound[2][jj]) + str(mesh_bound[2][jj+1]) \
                            + ')' + '-' *20 +  '\n')
                            for ii in range(len(lists)):
                                ascii_file.write('%s\n' % lists[ii])     
                else:
                    neutron_e_group = e_group[:200]
                    gamma_e_group = e_group[200:]
            varscl_file.close()
            ascii_file.close()
            
    def JumptoNextpart(self,pos):
        start_pos = pos + 4
        end_pos = pos + 8
        return start_pos,end_pos
        
    def ConfinePart(self,end_pos,pos2):
        start_pos = end_pos
        end_pos =  end_pos + pos2
        return start_pos,end_pos
        
    def Bin2Int(self,fileid,start_pos,end_pos):
        lists = []
        for ii in range(start_pos,end_pos,kBytesPerInt):
            fileid.seek(ii)
            (num,) = struct.unpack('i',fileid.read(kBytesPerInt))
            lists.append(num)
        return lists
        
    def Bin2Float(self,fileid,start_pos,end_pos):
        lists = []
        #print start_pos
        for ii in range(start_pos,end_pos,kBytesPerFloat):
            fileid.seek(ii)
            (num,) = struct.unpack('f',fileid.read(kBytesPerFloat))
            lists.append(num)
        return lists
        
    def Bin2Char(self,fileid,start_pos,end_pos):
        lists = []
        for ii in range(start_pos,end_pos,kBytesPerChar):
            fileid.seek(ii)
            (num,) = struct.unpack('c',fileid.read(kBytesPerChar))
            lists.append(num)
        return lists
    
    def Bin2Double(self,fileid,start_pos,end_pos):
        lists = []
        for ii in range(start_pos,end_pos,kBytesPerDouble):
            fileid.seek(ii)
            (num,) = struct.unpack('d',fileid.read(kBytesPerDouble))
            lists.append(num)
        return lists
        
        
if __name__ == '__main__':
    rv = ReadVarscl('200.adjoint.varscl','a')
    rv.Varscl2Ascii('outtest.txt')
        