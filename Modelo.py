# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 12:56:57 2018

@author: john ochoa
"""
#%%
import numpy as np;
import pydicom as dicom;
import os;
class DICOM(object):
    def __init__(self):
        self.__dcm = None;
        self.__data = None;
        self.__npatient = 0;
        
        self.__slices = 0;
        self.__rows = 0;
        self.__columns = 0;
        
        self.__x_space = 0;
        self.__y_space = 0;
        self.__x_thickness = 0;

        self.__nombre_paciente = ''
        self.__fecha_estudio = ''
        self.__fecha_nacimiento = ''
        self.__sexo_paciente = ''
        self.__id_paciente = ''
        self.__medico_tratante = ''
        
    #%%    
    def loadDICOM(self, PathDicom):               
        lstFilesDCM = []  # create an empty list
        for dirName, subdirList, fileList in os.walk(PathDicom):
            for filename in fileList:
                # check whether the file's DICOM
                if ".dcm" in filename.lower():  
                    lstFilesDCM.append(os.path.join(dirName,filename))        
        if len(lstFilesDCM) == 0:
            return False; 
        self.__dcm = lstFilesDCM
        # Get ref file
      
        print(lstFilesDCM)
        ref = dicom.read_file(lstFilesDCM[0])
        print(ref,'r')
        # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
        self.__rows = int(ref.Rows);
        
        self.__columns = int(ref.Columns);
        self.__slices = len(lstFilesDCM);   
        print(self.__rows,"coronal,",self.__columns,"sagital,",self.__slices,"axial")
    
        # Load spacing values (in mm)
        self.__x_space = float(ref.PixelSpacing[0]);
        self.__y_space = float(ref.PixelSpacing[1]);
        self.__thickness = float(ref.SliceThickness);                
        self.__data = np.zeros((self.__rows, self.__columns, self.__slices), 
                               dtype=ref.pixel_array.dtype);

        self.__nombre_paciente = str(ref[0x0010, 0x0010].value)
        self.__fecha_estudio = str(ref[0x0008, 0x0020].value)
        self.__fecha_nacimiento = str(ref[0x0010, 0x0030].value)
        self.__sexo_paciente = str(ref[0x0010, 0x0040].value)
        self.__id_paciente = str(ref[0x0010, 0x0020].value)
        self.__medico_tratante = str(ref[0x0008, 0x0090].value)

        # loop through all the DICOM files
        counter = 0
        for filenameDCM in lstFilesDCM:
            # read the file
            ds = dicom.read_file(filenameDCM)
            # store the raw imag e data
            self.__data[:, :, counter] = ds.pixel_array;
            counter = counter + 1;       
            print(counter)
        return True;
    #%%  

    def obtenerNombrePaciente(self):
        return self.__nombre_paciente

    def obtenerFechaEstudio(self):
        return self.__fecha_estudio

    def obtenerFechaNacimiento(self):
        return self.__fecha_nacimiento

    def obtenerSexoPaciente(self):
        return self.__sexo_paciente

    def obtenerIDPaciente(self):
        return self.__id_paciente

    def obtenerMedicoTratante(self):
        return self.__medico_tratante
              
    def returnSliceAxial(self,position):
        print(self.__data[:,:,position])
        return self.__data[:,:,position];
    
    def returnSliceCoronal(self,position):
        print(self.__data[position,:,:])
        return self.__data[position,:,:];
    
    def returnSliceSagital(self,position):
        print(self.__data[:,position,:])
        return self.__data[:,position,:];
