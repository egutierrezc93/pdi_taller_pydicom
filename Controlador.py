#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 10:37:41 2018

@author: john ochoa
"""
from Modelo import DICOM
from Vista import InterfazGrafico
import sys
from PyQt5.QtWidgets import QApplication
#%% INICIALIZACION CLASES
class Principal(object):
    def __init__(self):        
        self.__app = QApplication(sys.argv);
        
        self.__mi_vista = InterfazGrafico();
        self.__mi_dicom = DICOM()
        
        self.__mi_controlador=Coordinador(self.__mi_vista,self.__mi_dicom)
        self.__mi_vista.asignar_Controlador(self.__mi_controlador)
    
    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())

#%% ENLACE ENTRE CLASES    
class Coordinador(object):
    def __init__(self, vista, dicom):
        self.__mi_vista = vista;
        self.__mi_dicom = dicom;
        
    def recibirCarpetaDICOM(self, path):
        return self.__mi_dicom.loadDICOM(path);
    
    def returnSliceAxial(self,position):
        return self.__mi_dicom.returnSliceAxial(position);
    
    def returnSliceSagital(self,position):
        return self.__mi_dicom.returnSliceSagital(position);    
    
    def returnSliceCoronal(self,position):
        return self.__mi_dicom.returnSliceCoronal(position);

    def obtenerNombrePaciente(self):
        return self.__mi_dicom.obtenerNombrePaciente()

    def obtenerFechaEstudio(self):
        return self.__mi_dicom.obtenerFechaEstudio()

    def obtenerFechaNacimiento(self):
        return self.__mi_dicom.obtenerFechaNacimiento()

    def obtenerSexoPaciente(self):
        return self.__mi_dicom.obtenerSexoPaciente()

    def obtenerIDPaciente(self):
        return self.__mi_dicom.obtenerIDPaciente()

    def obtenerMedicoTratante(self):
        return self.__mi_dicom.obtenerMedicoTratante()

    def convertir_a_dicom(self, imagen, ruta_guardado):
        return self.__mi_dicom.convertir_a_dicom(imagen, ruta_guardado)
    

p = Principal()
p.main()
