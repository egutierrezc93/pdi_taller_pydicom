#%% Librerias
from Modelo import DICOM
#Qfiledialog es una ventana para abrir y guardar archivos
#Qvbox es un organizador de widget en la ventana, este en particular los apila en vertical
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#contenido para graficos de matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# clase con el lienzo (canvas=lienzo) para mostrar en la interfaz los graficos matplotlib, el canvas mete la grafica dentro de la interfaz
class MyGraphCanvas(FigureCanvas):
    #constructor
    def __init__(self, parent= None,width=10, height=8, dpi=300):
        
        #se crea un objeto figura
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #el axes en donde va a estar mi grafico debe estar en mi figura
        self.axial = self.fig.add_subplot(131)
        self.coronal = self.fig.add_subplot(132)
        self.sagital = self.fig.add_subplot(133)
        
        #se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init__(self,self.fig)
        
    #hay que crear un metodo para graficar un corte
    def graficar_axial(self,datos,indice):
        #primero se necesita limpiar la grafica anterior
        self.axial.clear();
        #ingresamos los datos a graficar
        self.axial.imshow(datos,cmap='gray');
        self.axial.set_title("Axial")
        self.axial.set_ylabel("indice"+str(indice))
        #ordenamos que dibuje
        self.axial.figure.canvas.draw();

    def graficar_coronal(self,datos):
        #primero se necesita limpiar la grafica anterior
        self.coronal.clear();
        #ingresamos los datos a graficar
        self.coronal.imshow(datos,cmap='gray');
        self.coronal.set_title("Coronal")
        #ordenamos que dibuje
        self.coronal.figure.canvas.draw();

    def graficar_sagital(self,datos):
        #primero se necesita limpiar la grafica anterior
        self.sagital.clear();
        #ingresamos los datos a graficar
        self.sagital.imshow(datos,cmap='gray');
        self.sagital.set_title("Sagital")
        #ordenamos que dibuje
        self.sagital.figure.canvas.draw();
#%%
class InterfazGrafico(QMainWindow):
    #condtructor
    def __init__(self):
        #siempre va
        super(InterfazGrafico,self).__init__()
        #se carga el diseno
        loadUi ('anadir_grafico.ui',self)
        #se llama la rutina donde configuramos la interfaz
        self.setup()
        #se muestra la interfaz
        self.show()
        #voy a crear un atributo que sea el indice
        self.__indice = 0;
    
    def setup(self):
        #los layout permiten organizar widgets en un contenedor
        #esta clase permite añadir widget uno encima del otro (vertical)
        layout = QVBoxLayout()
        #se añade el organizador al campo grafico
        self.campo_grafico.setLayout(layout)
        #se crea un objeto para manejo de graficos
        self.__sc = MyGraphCanvas(self.campo_grafico, width=5, height=4, dpi=100)
        #se añade el campo de graficos
        layout.addWidget(self.__sc)
        #se organizan las senales 
        self.boton_cargar.clicked.connect(self.cargar_dicom);
        self.boton_atras.clicked.connect(self.atras);
        self.boton_adelante.clicked.connect(self.adelante);
        self.boton_conv_jpeg_to_dicom.clicked.connect(self.convertir_a_dcm);
        
    def asignar_Controlador(self,controlador):
        self.__coordinador=controlador
    
    def atras(self):
        #disminuyo el indice
        self.__indice = self.__indice - 1;
        #le digo al controlador que le diga al modelo que me devuelva
        #el corte en esa posicion
        self.__sc.graficar_axial(self.__coordinador.returnSliceAxial(self.__indice),self.__indice);
        self.__sc.graficar_coronal(self.__coordinador.returnSliceCoronal(self.__indice));
        self.__sc.graficar_sagital(self.__coordinador.returnSliceSagital(self.__indice));
    
    def adelante(self):
        self.__indice = self.__indice+1;
        self.__sc.graficar_axial(self.__coordinador.returnSliceAxial(self.__indice),self.__indice);
        self.__sc.graficar_coronal(self.__coordinador.returnSliceCoronal(self.__indice));
        self.__sc.graficar_sagital(self.__coordinador.returnSliceSagital(self.__indice));
    
        
    def cargar_dicom(self):
        #se abre el cuadro de dialogo para cargar un directorio
        directorio = QFileDialog.getExistingDirectory(
                self,
                "Seleccione un directorio",
                ".",
                QFileDialog.ShowDirsOnly);
        if directorio != "":
            print(directorio)
            
            resultado = self.__coordinador.recibirCarpetaDICOM(directorio);
            if resultado == True:
                #actualizo el indice
                self.__indice = 0;
                self.__sc.graficar_axial(
                        self.__coordinador.returnSliceAxial(self.__indice),self.__indice);
                self.__sc.graficar_coronal(
                        self.__coordinador.returnSliceCoronal(self.__indice));
                self.__sc.graficar_sagital(
                        self.__coordinador.returnSliceSagital(self.__indice));
                self.nombre_paciente.setText(
                    str(self.__coordinador.obtenerNombrePaciente()))
                self.id_paciente.setText(
                    str(self.__coordinador.obtenerIDPaciente()))
                self.fecha_examen.setText(
                    str(self.__coordinador.obtenerFechaEstudio()))
                self.fecha_nacimiento.setText(
                    str(self.__coordinador.obtenerFechaNacimiento()))
                self.sexo_paciente.setText(
                    str(self.__coordinador.obtenerSexoPaciente()))
                self.medico_tratante.setText(
                    str(self.__coordinador.obtenerMedicoTratante()))

    def convertir_a_dcm(self):
        archivo_jpeg, _ = QFileDialog.getOpenFileName(self,
                                                   "Seleccione el archivo jpeg a convertir",
                                                   ".", "Images (*.jpg *.jpeg)")

        directorio = QFileDialog.getExistingDirectory(self,
                                                      "Seleccione un directorio para guardar imagen dcm",
                                                      ".",
                                                      QFileDialog.ShowDirsOnly)

        if (directorio != "") & (archivo_jpeg != ""):
            print('archivo JPEG: ', archivo_jpeg)
            print('directorio: ', directorio)
            self.__coordinador.convertir_a_dicom(archivo_jpeg, directorio)
        else:
            print('No seleccionó o el directorio o una imagen jpeg correctamente')
