"""
Creado como taller del manejo de imagenes médicas para la materia
de procesamiento de imagenes de la universidad de Antioquia,
semestre 2020-2

Vista de la arquitectura MVC

Proyecto Visor DICOM

@authors: John Ochoa, Juan David Cruz y Esteban Gutiérrez
"""

# %% Librerias
from Modelo import DICOM
# Qfiledialog es una ventana para abrir y guardar archivos
# Qvbox es un organizador de widget en la ventana, este en particular los apila en vertical
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog, QDialog
from PyQt5.uic import loadUi

# contenido para graficos de matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# clase con el lienzo (canvas=lienzo) para mostrar en la interfaz los graficos matplotlib, el canvas mete la grafica dentro de la interfaz
class MyGraphCanvas(FigureCanvas):
    # constructor
    def __init__(self, parent=None, width=10, height=8, dpi=300):
        # se crea un objeto figura
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # el axes en donde va a estar mi grafico debe estar en mi figura
        self.axial = self.fig.add_subplot(131)
        self.coronal = self.fig.add_subplot(132)
        self.sagital = self.fig.add_subplot(133)

        # se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init__(self, self.fig)

    # hay que crear un metodo para graficar un corte
    def graficar_axial(self, datos, indice):
        # primero se necesita limpiar la grafica anterior
        self.axial.clear()
        # ingresamos los datos a graficar
        self.axial.imshow(datos, cmap='gray')
        self.axial.set_title("Axial")
        self.axial.set_ylabel("indice" + str(indice))
        # ordenamos que dibuje
        self.axial.figure.canvas.draw()

    def graficar_coronal(self, datos):
        # primero se necesita limpiar la grafica anterior
        self.coronal.clear()
        # ingresamos los datos a graficar
        self.coronal.imshow(datos, cmap='gray')
        self.coronal.set_title("Coronal")
        # ordenamos que dibuje
        self.coronal.figure.canvas.draw()

    def graficar_sagital(self, datos):
        # primero se necesita limpiar la grafica anterior
        self.sagital.clear()
        # ingresamos los datos a graficar
        self.sagital.imshow(datos, cmap='gray')
        self.sagital.set_title("Sagital")
        # ordenamos que dibuje
        self.sagital.figure.canvas.draw()


# %%
class InterfazGrafico(QMainWindow):
    # constructor
    def __init__(self, ppal=None):
        # siempre va
        super(InterfazGrafico, self).__init__(ppal)
        # se carga el diseno
        loadUi('anadir_grafico.ui', self)
        # se llama la rutina donde configuramos la interfaz
        self.setup()
        # se muestra la interfaz
        self.show()
        # voy a crear un atributo que sea el indice
        self.__indice = 0

    def setup(self):
        # los layout permiten organizar widgets en un contenedor
        # esta clase permite añadir widget uno encima del otro (vertical)
        layout = QVBoxLayout()
        # se añade el organizador al campo grafico
        self.campo_grafico.setLayout(layout)
        # se crea un objeto para manejo de graficos
        self.__sc = MyGraphCanvas(self.campo_grafico, width=5, height=4, dpi=100)
        # se añade el campo de graficos
        layout.addWidget(self.__sc)
        # se organizan las senales
        self.boton_cargar.clicked.connect(self.cargar_dicom)
        self.boton_atras.clicked.connect(self.atras)
        self.boton_adelante.clicked.connect(self.adelante)
        self.boton_conv_jpeg_to_dicom.clicked.connect(self.convertir_a_dcm)

    # Se asigna instancia del controlador a esta vista
    def asignar_Controlador(self, controlador):
        self.__coordinador = controlador

    # Metodos de la vista encargados del manejo de botones
    def atras(self):
        # disminuyo el indice
        self.__indice = self.__indice - 1
        # le digo al controlador que le diga al modelo que me devuelva
        # el corte en esa posicion
        self.__sc.graficar_axial(self.__coordinador.returnSliceAxial(self.__indice), self.__indice)
        self.__sc.graficar_coronal(self.__coordinador.returnSliceCoronal(self.__indice))
        self.__sc.graficar_sagital(self.__coordinador.returnSliceSagital(self.__indice))

    def adelante(self):
        # Aumento el indice
        self.__indice = self.__indice + 1
        # le digo al controlador que le diga al modelo que me devuelva
        # el corte en esa posicion
        self.__sc.graficar_axial(self.__coordinador.returnSliceAxial(self.__indice), self.__indice)
        self.__sc.graficar_coronal(self.__coordinador.returnSliceCoronal(self.__indice))
        self.__sc.graficar_sagital(self.__coordinador.returnSliceSagital(self.__indice))

    def cargar_dicom(self):
        # se abre el cuadro de dialogo para cargar un directorio
        directorio = QFileDialog.getExistingDirectory(
            self,
            "Seleccione un directorio",
            ".",
            QFileDialog.ShowDirsOnly)

        # Se verifica que el directorio no sea nulo
        if directorio != "":
            print(directorio)

            # Se verifica el ingreso de una carpeta con archivos DICOM
            resultado = self.__coordinador.recibirCarpetaDICOM(directorio)
            if resultado:
                # actualizo el indice
                self.__indice = 0

                # Cargo vistas del respectivo corte
                self.__sc.graficar_axial(
                    self.__coordinador.returnSliceAxial(self.__indice), self.__indice)
                self.__sc.graficar_coronal(
                    self.__coordinador.returnSliceCoronal(self.__indice))
                self.__sc.graficar_sagital(
                    self.__coordinador.returnSliceSagital(self.__indice))

                # Cargo información del paciente
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

    # Metodo encargado de recibir interucción al click del boton convertir a DCM
    def convertir_a_dcm(self):
        # Se lanza la vista del formulario
        self.ventanaformulario = formulario_window(self)
        self.ventanaformulario.asignar_Controlador(self.__coordinador)
        self.ventanaformulario.show()


# Clase encargada de la ventana de dialogo del formulario
class formulario_window(QDialog):
    # Constructor
    def __init__(self, ppal=None):
        # siempre va
        super(formulario_window, self).__init__(ppal)
        # se carga el diseno
        loadUi('formulario.ui', self)
        # se llama la rutina donde configuramos la interfaz
        self.setup()

    def setup(self):
        self.Aceptarinf.accepted.connect(self.guardar_datos)

    def asignar_Controlador(self, controlador):
        self.__coordinador = controlador

    # Se crea la rutina de vista del botón guardar
    def guardar_datos(self):
        # Se crea una lista con la información del formulario
        Np = self.Nombrepaciente.text()
        IDp = self.IDpaciente.text()
        Birth = self.Birth.text()
        Sex = self.Sex.text()
        Med = self.Medico.text()
        fecha = self.Fecha.text()
        hora = self.Hora.text()
        study = self.studyID.text()
        info = [Np, IDp, Birth, Sex, Med, fecha, hora, study]
        self.envio_datos(info)

        # se abre el cuadro de dialogo para cargar un archivo
        archivo_jpeg, _ = QFileDialog.getOpenFileName(self,
                                                      "Seleccione el archivo jpeg a convertir",
                                                      ".", "Images (*.jpg *.jpeg)")

        # se abre el cuadro de dialogo para cargar el directorio de guardado
        directorio = QFileDialog.getExistingDirectory(self,
                                                      "Seleccione un directorio para guardar imagen dcm",
                                                      ".",
                                                      QFileDialog.ShowDirsOnly)

        # Se verifica que tanto el directorio como el archivo no sean nulos
        if (directorio != "") & (archivo_jpeg != ""):
            # Se llama la rutina del controlador encargada de convertir y guardar archivo
            self.__coordinador.convertir_a_dicom(archivo_jpeg, directorio)
        else:
            print('No seleccionó o el directorio o una imagen jpeg correctamente')

        # Se oculta la vista
        self.hide()

    def envio_datos(self, info):
        self.__coordinador.recibirinfo(info)

    # Se crea la rutina de vista del botón cancelar
    def cancel(self):
        self.Aceptarinf.rejected.connect(self.guardar_datos)
        self.hide()
