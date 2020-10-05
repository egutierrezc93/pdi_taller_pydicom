# -*- coding: utf-8 -*-
"""
Creado como taller del manejo de imagenes médicas para la materia
de procesamiento de imagenes de la universidad de Antioquia,
semestre 2020-2

Modelo de la arquitectura MVC

Proyecto Visor DICOM

@authors: john ochoa, Juan David Cruz y Esteban Gutiérrez
"""

from PIL import Image
import numpy as np
import pydicom as dicom
import os


# Clase encargada de manejar la logica de procesamiento de imagenes del Visor DICOM
class DICOM(object):
    # Constructor
    def __init__(self):
        # Inicialización de las variables de la clase
        self.__dcm = None
        self.__data = None
        self.__npatient = 0

        self.__slices = 0
        self.__rows = 0
        self.__columns = 0

        self.__x_space = 0
        self.__y_space = 0
        self.__x_thickness = 0

        self.__nombre_paciente = ''
        self.__fecha_estudio = ''
        self.__fecha_nacimiento = ''
        self.__sexo_paciente = ''
        self.__id_paciente = ''
        self.__medico_tratante = ''
        self.__hora_estudio = ''
        self.__estudio_id = ''

    # Metodo encargado de cargar las imagenes DICOM
    def loadDICOM(self, PathDicom):
        lstFilesDCM = []  # crear una lista vacia
        for dirName, subdirList, fileList in os.walk(PathDicom):
            for filename in fileList:
                # Hacer un chequeo de el formato del archivo
                if ".dcm" in filename.lower():
                    lstFilesDCM.append(os.path.join(dirName, filename))
        if len(lstFilesDCM) == 0:
            return False;

        # Se obtiene la lista de archivos dcm en la carpeta
        self.__dcm = lstFilesDCM

        # Se lee el primer archivo .dcm del directorio
        ref = dicom.read_file(lstFilesDCM[0])

        # Se cargan las dimensiones basados en el número de filas, columnas y cortes (a lo largo del eje Z)
        self.__rows = int(ref.Rows)
        self.__columns = int(ref.Columns)
        self.__slices = len(lstFilesDCM)
        #print(self.__rows, "coronal,", self.__columns, "sagital,", self.__slices, "axial")

        # Se cargan los valores de espaciado (en mm)
        self.__x_space = float(ref.PixelSpacing[0]);
        self.__y_space = float(ref.PixelSpacing[1]);
        self.__thickness = float(ref.SliceThickness);
        self.__data = np.zeros((self.__rows, self.__columns, self.__slices),
                               dtype=ref.pixel_array.dtype)

        # Se cargan los valores de los atributos principales de la imagen
        self.__nombre_paciente = str(ref[0x0010, 0x0010].value)
        self.__fecha_estudio = str(ref[0x0008, 0x0020].value)
        self.__fecha_nacimiento = str(ref[0x0010, 0x0030].value)
        self.__sexo_paciente = str(ref[0x0010, 0x0040].value)
        self.__id_paciente = str(ref[0x0010, 0x0020].value)
        self.__medico_tratante = str(ref[0x0008, 0x0090].value)

        # Se itera sobre todos los archivos del direcorio
        counter = 0
        for filenameDCM in lstFilesDCM:
            # se lee el archivo
            ds = dicom.read_file(filenameDCM)
            # se guarda la imagen en crudo
            self.__data[:, :, counter] = ds.pixel_array;
            counter = counter + 1;
            print(counter)
        return True

    # Serie de metodos dirigidos a obtener información del paciente y el estudio
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

    # Serie de metodos que devuelven las diferentes tomas de la imagen Axial, Sagital y Coronal
    def returnSliceAxial(self, position):
        return self.__data[:, :, position]

    def returnSliceCoronal(self, position):
        return self.__data[position, :, :]

    def returnSliceSagital(self, position):
        return self.__data[:, position, :]

    # Metodo encargado de actualizar información generada por el usuario para convertir imagen jpeg a DICOM
    def asignarinfo(self, info):
        self.__nombre_paciente = info[0]
        self.__fecha_estudio = info[5]
        self.__fecha_nacimiento = info[2]
        self.__sexo_paciente = info[3]
        self.__id_paciente = info[1]
        self.__medico_tratante = info[4]
        self.__hora_estudio = info[6]
        self.__estudio_id = info[7]

    # Metodo encargado de convertir imagen en un archivo DICOM y guardarla en una ruta especificada
    def convertir_a_dicom(self, imagen, ruta_guardado):
        archivo_entrada = imagen
        archivo_salida = ruta_guardado + "/dicom_img.dcm"

        # Este formato se encarga de gaurdar información requerida para cargar la imagen en el Visor DICOM
        formato = ' -k 0028,0030=1,1 -k 0018,0050=1'

        # Se convierte la imagen JPEG o JPG a escala de grises para mejor manejo de la imagen
        img = Image.open(archivo_entrada).convert('L')
        img.save('temp.jpeg')
        archivo_entrada = 'temp.jpeg'

        # Se ejecuta comando del sistema operativo para convertir imagen a .dcm
        cmd = "/usr/bin/img2dcm " + archivo_entrada + " " + archivo_salida + formato
        os.system(cmd)  # returns the exit code in unix

        # Se actualiza información básica del archivo
        dset = dicom.dcmread(archivo_salida)
        dset.StudyDate = self.__fecha_estudio
        dset.StudyTime = self.__hora_estudio
        dset.PatientName = self.__nombre_paciente
        dset.PatientID = self.__id_paciente
        dset.PatientBirthDate = self.__fecha_nacimiento
        dset.PatientSex = self.__sexo_paciente
        dset.StudyID = self.__estudio_id
        dset.ReferringPhysicianName = self.__medico_tratante
        dset[0x0028, 0x0030].value = [1, 1]
        dset.save_as(archivo_salida)

        return True
