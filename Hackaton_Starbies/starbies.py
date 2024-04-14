from interfaz import *
import csv
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

csv_usuarios = "usuarios_contraseñas.csv"

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.users = []
        self.passwords = []
        self.valid_passwords = []
        self.leer_user_password()
        self.datos_usuario = {}
        self.stackedWidget.setCurrentIndex(0) # PÁGINA DE INICIO
        self.pushButton_registrarse.clicked.connect(self.registro)
        self.pushButton_iniciosesion.clicked.connect(self.inicio_sesion)
        self.pushButton_cancelar_reg.clicked.connect(self.cancelar)
        self.pushButton_cancelar_inicio.clicked.connect(self.cancelar)
        self.pushButton_cancelar_datos.clicked.connect(self.cancelar_datos)
        self.pushButton_aceptar_reg.clicked.connect(self.registro_sesion)
        self.pushButton_aceptar_inicio.clicked.connect(self.bienvenida)
        self.pushButton_Registrate.clicked.connect(self.registro)
        self.pushButton_cargar_imagen.clicked.connect(self.cargar_imagen)
        self.pushButton_guardar_datos.clicked.connect(self.insertar_datos)
        self.pushButton_barra_imc.clicked.connect(self.pagina_imc)
        self.pushButton_barra_imc_2.clicked.connect(self.pagina_imc)
        self.pushButton_barra_imc_3.clicked.connect(self.pagina_imc)
        self.pushButton_barra_imc_4.clicked.connect(self.pagina_imc)
        self.pushButton_barra_imc_6.clicked.connect(self.pagina_imc)
        self.pushButton_imc_menu.clicked.connect(self.pagina_imc)
        self.pushButton_barra_info.clicked.connect(self.pagina_info)
        self.pushButton_barra_info_2.clicked.connect(self.pagina_info)
        self.pushButton_barra_info_3.clicked.connect(self.pagina_info)
        self.pushButton_barra_info_4.clicked.connect(self.pagina_info)
        self.pushButton_barra_info_6.clicked.connect(self.pagina_info)
        self.pushButton_info_menu.clicked.connect(self.pagina_info)
        self.pushButton_barra_macros.clicked.connect(self.pagina_macros)
        self.pushButton_barra_macros_2.clicked.connect(self.pagina_macros)
        self.pushButton_barra_macros_3.clicked.connect(self.pagina_macros)
        self.pushButton_barra_macros_4.clicked.connect(self.pagina_macros)
        self.pushButton_barra_macros_6.clicked.connect(self.pagina_macros)
        self.pushButton_macro_menu.clicked.connect(self.pagina_macros)
        self.pushButton_home.clicked.connect(self.principal)
        self.pushButton_home_2.clicked.connect(self.principal)
        self.pushButton_home_3.clicked.connect(self.principal)
        self.pushButton_home_5.clicked.connect(self.principal)
        self.pushButton_home_6.clicked.connect(self.principal)
        self.pushButton_perfil.clicked.connect(self.perfil)
        self.pushButton_perfil_2.clicked.connect(self.perfil)
        self.pushButton_perfil_3.clicked.connect(self.perfil)
        self.pushButton_perfil_4.clicked.connect(self.perfil)
        self.pushButton_perfil_7.clicked.connect(self.perfil)
        self.pushButton_logout.clicked.connect(self.cancelar)
        self.pushButton_logout_2.clicked.connect(self.cancelar)
        self.pushButton_logout_3.clicked.connect(self.cancelar)
        self.pushButton_logout_4.clicked.connect(self.cancelar)
        self.pushButton_logout_6.clicked.connect(self.cancelar)
        self.pushButton_logout_7.clicked.connect(self.cancelar)
        self.pushButton_info_ger.clicked.connect(self.info_ger)
        self.pushButton_link.clicked.connect(self.info_link)
        self.pushButton_conocenos.clicked.connect(self.equipo)

    def leer_user_password(self):
        with open (csv_usuarios, "r", encoding="utf-8-sig") as archivo:
            archivo.seek(0)
            lector_csv = csv.DictReader(archivo)
            for row in lector_csv:
                user = row["user"]
                password = row["password"]
                valid_password = row["valid_password"]
                self.users.append(user)
                self.passwords.append(password)
                self.valid_passwords.append(valid_password)

    def bienvenida(self):
        self.write_user = self.lineEdit_user_inicio.text()
        write_password = self.lineEdit_password_inicio.text()
        if self.write_user and write_password: # si hay algo escrito
            if self.write_user in self.users:
                indice = self.users.index(self.write_user)
                if write_password == self.passwords[indice]:
                    nombre, apellidop = self.write_user.split("_")
                    self.label_saludo.setText(f"Hola {nombre}, ¿en qué podemos ayudarte hoy?")
                    self.stackedWidget.setCurrentIndex(7) # PÁGINA PRINCIPAL
                    archivo_persona = f"{self.write_user}.csv"
                    if os.path.exists(archivo_persona):
                        self.obtener_datos(archivo_persona)
                        foto_path = self.datos_usuario.get("foto", "")
                        if foto_path:
                            foto = QPixmap(foto_path)
                            self.label_imagen.setPixmap(foto)
            else:
                message_box = QMessageBox()
                message_box.setWindowTitle("ERROR")
                message_box.setText("Usuario o contraseña incorrectos")
                message_box.exec()
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText("Favor de llenar todos los campos")
            message_box.exec()
        if not self.validar_existencia_datos():
            self.lineEdit_user_inicio.clear()
            self.lineEdit_password_inicio.clear()
            self.lineEdit_apellidom.clear()
            self.comboBox_edad.clearEditText()
            self.comboBox_sexo.clearEditText()
            self.lineEdit_estatura.clear()
            self.lineEdit_peso.clear()
            self.comboBox_actividad.clearEditText()

    def registro_sesion(self):
        username = f"{self.lineEdit_nombre_registro.text()}_{self.lineEdit_apellido_registro.text()}"
        if self.lineEdit_nombre_registro.text() and self.lineEdit_apellido_registro.text() and self.lineEdit_password.text() and self.lineEdit_confirmpassword.text(): # verificar que esté todo escrito
            if self.lineEdit_password.text() != self.lineEdit_confirmpassword.text(): # contraseñas iguales
                message_box = QMessageBox()
                message_box.setWindowTitle("ERROR")
                message_box.setText("Las contraseñas no son iguales")
                message_box.exec()
            if username in self.users:
                message_box = QMessageBox()
                message_box.setWindowTitle("ERROR")
                message_box.setText("Este usuario ya está registrado")
                message_box.exec()
                self.stackedWidget.setCurrentIndex(1) # PÁGINA DE REGISTRO
            else:
                message_box = QMessageBox()
                message_box.setWindowTitle("FELICIDADES")
                message_box.setText(f"Registro exitoso\nSu usuario es {username}")
                message_box.exec()
                nuevo_user = username
                nueva_password = self.lineEdit_password.text()
                nueva_valid_password = self.lineEdit_confirmpassword.text()
                self.agregar_usuario_registrado(nuevo_user, nueva_password, nueva_valid_password)
                self.stackedWidget.setCurrentIndex(3) # PÁGINA DE INICIO DE SESIÓN
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText("Llena todos los campos")
            message_box.exec()
    
    def agregar_usuario_registrado(self, nuevo_user, nueva_password, nueva_valid_password):
        self.users.append(nuevo_user)
        self.passwords.append(nueva_password)
        self.valid_passwords.append(nueva_valid_password)
        with open(csv_usuarios, "a", newline="", encoding="utf-8") as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow([nuevo_user, nueva_password, nueva_valid_password])

    def insertar_datos(self):
        usuario = self.write_user
        nombre, apellidop = usuario.split("_")
        apellidom = self.lineEdit_apellidom.text()
        edad = self.comboBox_edad.currentText()
        sexo = self.comboBox_sexo.currentText()
        estatura = self.lineEdit_estatura.text()
        peso = self.lineEdit_peso.text()
        actividad = self.comboBox_actividad.currentText()
        foto = self.guardar_imagen() or "imagen.png"
        if foto:
            datos = [usuario, nombre, apellidop, apellidom, edad, sexo, estatura, peso, actividad, foto]
            self.crear_csv_usuario(datos)
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText("Favor de cargar una imagen")
            message_box.exec()

    def crear_csv_usuario(self, datos):
        csv_persona = f"{datos[0]}.csv"
        with open(csv_persona, "w", newline="", encoding="utf-8") as archivo:
            escritor_csv = csv.DictWriter(archivo, fieldnames=["usuario", "nombre", "apellido paterno", "apellido materno", "edad", "sexo", "estatura", "peso", "actividad", "foto"])
            escritor_csv.writeheader()
            datos_dict = {
                "usuario": datos[0],
                "nombre": datos[1],
                "apellido paterno": datos[2],
                "apellido materno": datos[3],
                "edad": datos[4],
                "sexo": datos[5],
                "estatura": datos[6],
                "peso": datos[7],
                "actividad": datos[8],
                "foto": datos[9]
            }
            escritor_csv.writerow(datos_dict)
            message_box = QMessageBox()
            message_box.setWindowTitle("FELICIDADES")
            message_box.setText("Datos guardados con éxito")
            message_box.exec()
            self.obtener_datos(csv_persona)
            self.cancelar()

    def obtener_datos(self, csv_persona):
        self.datos_usuario = {}
        with open(csv_persona, "r", newline="", encoding="utf-8-sig") as archivo:
            lector_csv = csv.DictReader(archivo)
            for row in lector_csv:
                self.datos_usuario = row
                foto_path = self.datos_usuario.get("foto", "")
                if foto_path:
                    foto = QPixmap(foto_path)  # cargar imagen desde la ruta
                    self.label_imagen.setPixmap(foto)  # mostrar imagen

    def validar_existencia_datos(self):
        usuario = self.datos_usuario.get("usuario")
        if usuario is not None:
            csv_persona = f"{usuario}.csv"
            if os.path.exists(csv_persona):
                return True
        else:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText("Primero completa los datos de tu perfil")
            message_box.exec()
            return False

    def registro(self):
        self.stackedWidget.setCurrentIndex(1) # PÁGINA DE REGISTRO
    
    def inicio_sesion(self):
        self.stackedWidget.setCurrentIndex(3) # PÁGINA DE INICIO DE SESIÓN
    
    def cancelar(self):
        self.lineEdit_user_inicio.clear()
        self.lineEdit_password_inicio.clear()
        self.lineEdit_apellidom.clear()
        self.comboBox_edad.clearEditText()
        self.comboBox_sexo.clearEditText()
        self.lineEdit_estatura.clear()
        self.lineEdit_peso.clear()
        self.comboBox_actividad.clearEditText()
        self.lineEdit_nombre_registro.clear()
        self.lineEdit_apellido_registro.clear()
        self.lineEdit_password.clear()
        self.lineEdit_confirmpassword.clear()
        self.datos_usuario = {}
        self.stackedWidget.setCurrentIndex(0) # PÁGINA DE INICIO

    def pagina_imc(self):
        if self.validar_existencia_datos():
            self.stackedWidget.setCurrentIndex(4) # PÁGINA DE IMC
            self.calculo_imc()
        
    def pagina_macros(self):
        if self.validar_existencia_datos():
            self.stackedWidget.setCurrentIndex(5) # PÁGINA DE MACROS
            self.validar_imc()
    
    def validar_imc(self):
        if not self.calculo_imc():
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText("Primero calcula tu IMC")
            message_box.exec()

    def pagina_info(self):
        self.stackedWidget.setCurrentIndex(6) # PÁGINA DE INFORMACIÓN EXTRA

    def principal(self):
        nombre = self.datos_usuario.get("nombre")
        self.label_saludo.setText(f"Hola {nombre}, ¿en qué podemos ayudarte hoy?")
        self.stackedWidget.setCurrentIndex(7) # PÁGINA PRINCIPAL
    
    def cancelar_datos(self):
        self.stackedWidget.setCurrentIndex(7) # PÁGINA PRINCIPAL

    def perfil(self):
        nombre, apellidop = self.write_user.split("_")
        self.label_nombre_datos.setText(nombre)
        self.label_apellidop_datos.setText(apellidop)
        self.stackedWidget.setCurrentIndex(2) # PÁGINA DE DATOS PERSONALES
        if self.validar_existencia_datos():
            apellidom = self.datos_usuario.get("apellido materno", None)
            edad = self.datos_usuario.get("edad", None)
            sexo = self.datos_usuario.get("sexo", None)
            estatura = self.datos_usuario.get("estatura", None)
            peso = self.datos_usuario.get("peso", None)
            actividad = self.datos_usuario.get("actividad", None)
            foto = self.datos_usuario.get("foto", None)
            self.lineEdit_apellidom.setText(apellidom)
            self.comboBox_edad.setCurrentText(edad)
            self.comboBox_sexo.setCurrentText(sexo)
            self.lineEdit_estatura.setText(estatura)
            self.lineEdit_peso.setText(peso)
            self.comboBox_actividad.setCurrentText(actividad)

    def cargar_imagen(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Archivos de imagen (*.png *.jpg *.jpeg *.bmp *.gif)")
        if filename:
            imagen = QPixmap(filename)
            if not imagen.isNull():
                self.label_imagen.setPixmap(imagen)

    def guardar_imagen(self):
        pixmap = self.label_imagen.pixmap()
        if pixmap:
            filename, _ = QFileDialog.getSaveFileName(self, "Guardar imagen", "", "Archivos de imagen (*.png *.jpg *.jpeg *.bmp *.gif)")
            if filename:
                if pixmap.save(filename):
                    QMessageBox.information(self, "Éxito", "La imagen se ha guardado correctamente.")
                    return filename if filename else None
                else:
                    QMessageBox.warning(self, "Error", "No se pudo guardar la imagen.")
        else:
            QMessageBox.warning(self, "Error", "No hay ninguna imagen para guardar.")

    def calculo_imc(self):
        estatura = float(self.datos_usuario.get("estatura", 0))
        peso = float(self.datos_usuario.get("peso", 0))
        imc = float(peso) / ((int(estatura) / 100) ** 2)
        self.label_valor_imc.setText(f"{imc:.2f}")
        self.calculo_rango_imc(imc)
        return True

    def calculo_rango_imc(self, imc):
        if imc < 18.5:
            rango = "bajo peso"
        elif imc > 18.5 and imc < 24.9:
            rango = "peso normal"
        elif imc < 25 and imc > 29.9:
            rango = "sobrepeso"
        elif imc < 30 and imc > 34.5:
            rango = "obesidad grado I"
        elif imc < 35 and imc > 39.9:
            rango = "obesidad grado II"
        else:
            rango = "obesidad grado III"
        self.label_rango_imc.setText(rango)
        self.calculo_formulas(imc)

    def calculo_formulas(self, imc):
        if imc < 26:
            self.henry_benedict()
        else:
            self.milphy()

    def henry_benedict(self): # menos de 26 en imc
        peso = float(self.datos_usuario.get("peso", 0))
        estatura = float(self.datos_usuario.get("estatura", 0))
        edad = float(self.datos_usuario.get("edad", 0))
        sexo = self.datos_usuario.get("sexo", 0)
        if sexo == "H":
            GER = (66.5 + (13.8 * peso) + (5 * estatura) - (6.8 * edad))
        else:
            GER = (665.1 + (9.6 * peso) + (1.9 * estatura) - (4.7 * edad))
        self.calorias_dia(GER)
    
    def milphy(self):
        peso = float(self.datos_usuario.get("peso", 0))
        estatura = float(self.datos_usuario.get("estatura", 0))
        edad = float(self.datos_usuario.get("edad", 0))
        sexo = self.datos_usuario.get("sexo", 0)
        if sexo == "H":
            GER = (5 + (10 * peso) + (6.25 * estatura) - (5 * edad))
        else:
            GER = (-161 + (10 * peso) + (6.25 * estatura) - (5 * edad))
        self.calorias_dia(GER)
    
    def calorias_dia(self, GER):
        actividad = self.datos_usuario.get("actividad", 0)
        if actividad == "Sedentario":
            cal_dia = GER * 1
        elif actividad == "Poco activo":
            cal_dia = GER * 1.4
        elif actividad == "Activo":
            cal_dia = GER * 1.27
        else:
            cal_dia = GER * 1.45
        nombre = self.datos_usuario.get("nombre", 0)
        self.label_cal_dia.setText(f"{nombre}, la cantidad de calorías necesarias a consumir en tu día son:")
        self.label_cal_dia_valor.setText(f"{cal_dia:.2f} Kcal")
        self.label_ger_valor.setText(f"GER: {GER:.2f} Kcal")
        self.proteinas_dia(cal_dia)
        self.lipidos_dia(cal_dia)
    
    def proteinas_dia(self, cal_dia):
        peso = float(self.datos_usuario.get("peso", 0))
        gramos = 1.4 * peso
        calorias = gramos * 4
        porcentaje = (calorias / cal_dia) * 100
        self.label_proteinas_porcentaje.setText(f"{porcentaje:.2f} %")
        self.label_proteinas_gramos.setText(f"{gramos:.2f} g")
        self.label_proteinas_cal.setText(f"{calorias:.2f} Kcal")
        self.carbohidratos_dia(porcentaje, cal_dia)

    def carbohidratos_dia(self, porcentaje_proteinas, cal_dia):
        porcentaje = 100 - 35 - porcentaje_proteinas
        calorias = (porcentaje * cal_dia) / 100
        gramos = calorias / 4
        self.label_carb_porcentaje.setText(f"{porcentaje:.2f} %")
        self.label_carb_gramos.setText(f"{gramos:.2f} g")
        self.label_carb_cal.setText(f"{calorias:.2f} Kcal")

    def lipidos_dia(self, cal_dia):
        calorias = (35 * cal_dia) / 100
        porcentaje = 35 # medida estándar proporcionada por nutricionistas para todas las personas
        gramos = calorias / 9
        self.label_lipidos_porcentaje.setText(f"{porcentaje:.2f} %")
        self.label_lipidos_gramos.setText(f"{gramos:.2f} g")
        self.label_lipidos_cal.setText(f"{calorias:.2f} Kcal")

    def info_ger(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("INFORMACIÓN")
        message_box.setText("GER significa Gasto Energético en Reposo")
        message_box.exec()

    def info_link(self):
        url = QUrl("https://www.who.int/health-topics/nutrition#tab=tab_1")
        QDesktopServices.openUrl(url)

    def equipo(self):
        self.stackedWidget.setCurrentIndex(8)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()