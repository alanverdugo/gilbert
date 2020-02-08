'''
    Usage:
        python invitados.py

    Optional arguments:
        None

    Description:
        Se creo una sencilla aplicacion de escritorio utilizando Python 3
        como lenguaje y Tkinter como el principal componente grafico. 
        El sistema tiene como proposito manejar la asistencia de invitados a 
        eventos de la UACH.
        Permite agregar, modificar y eliminar invitados, asi como registrar la 
        asistencia. Tambien se pueden exportar los datos a archivos CSV e 
        importarlos desde los mismos.
        Para guardar los datos se utiliza SQLite y para manejar la conexion a 
        la DB se usa una clase llamada DB, la cual se asegura de unicamente 
        crear una conexion, la cual permanecera activa hasta que el objeto 
        salga de scope.

    Intrucciones de compilacion:
        Instalar Python 3 y todos los modulos que sean necesarios. Algunos de 
        la libreria estandar deben estar ya instalados (como sys, time, o csv), 
        mientras que otros puede ser necesario instalarlos mediante el 
        manejador de paquetes de python (pip, el cual es posible que tambien 
        necesite ser instalado).
        En caso de problemas con Tkinter y PIL, es posible que se requieran 
        instalar paquetes mediante los comandos siguientes (para distribuciones 
        basadas en debian):
        sudo apt-get install python3-tk
        sudo apt-get install python3-pil python3-pil.imagetk
        Una vez que todos los modulos funcionan correctamente, la aplicacion 
        puede ser ejecutada en cualquier sistema operativo. Ha sido probada 
        tanto en Windows 10 como en Debian.

    Instrucciones de uso:
        La aplicacion se ejecuta mediante: python invitados.py
        En la base de datos se proveen registros de muestra para probar la 
        aplicacion, pero tambien se pueden borrar todos (o incluso borrar la 
        misma base de datos) y crear todo de nuevo usando la aplicacion.
        Para crear un registro, primero es necesario capturar todos los datos 
        en la parte izquierda de la ventana y despues hacer click en el boton
        Agregar invitado.
        Para modificar algun registro, se hara doble click en este y despues 
        se modificaran sus datos en la parte izquierda de la ventana. Una vez 
        con los datos actualizados, se hara click en el boton Actualizar 
        registro.
        Para borrar un registro, se hara doble click en el y despues se hara
        click en el boton Borrar registro.
        Para registrar la asistencia, se seleccionara un registro y se hara 
        click en el boton Registrar asistencia.
        Al hacer click en el boton Exportar a CSV, un archivo llamado 
        invitados.csv se creara en el mismo directorio de la aplicacion.
        Para importar datos de un archivo CSV, se hara click en el boton 
        Importar de CSV y se buscara el archivo deseado.

    Author:
        Alan Verdugo (a314774@uach.mx)

    Creation date:
        2018-05-26

    Modification list:
        CCYY-MM-DD  Author                  Description

'''

# Asegurarnos de que el sistema tiene instalados los modulos necesarios,
# De no ser asi, informar al usuario.
try:
    from tkinter import*
    from tkinter import filedialog
    import requests
    import json
    import time
    import csv
    import sys
    import tkinter.ttk as ttk
    import tkinter.messagebox as tkMessageBox
    from PIL import ImageTk, Image
except ImportError:
    print('Los modulos siguientes son necesarios para el correcto funcionamiento '\
        + 'de este sistema:\n\tsys\n\ttkinter\n\tsqlite3\n\ttime\n\tcsv\n\tpillow')
    print('Puede que sea necesario instalar algun modulo mediante el comando:'\
        '\n\tsudo pip install <modulo>')
    print('En su defecto, intente ejecutando los comandos:'\
        '\n\tsudo apt-get install python3-tk'\
        '\n\tsudo apt-get install python3-pil python3-pil.imagetk')
    sys.exit(1)

# Global stuff and general settings.
root = Tk()
root.title("UACH - Sistema de manejo de invitados")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 900
height = 600
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(0, 0)
global asistentes
global percentage
global invitados_url
invitados_url = "http://kippel.net:5000/invitados"
global headers
headers = {'content-type': 'application/json'}

#==================================METODOS======================================
# Importar archivos CSV
def import_csv():
    try:
        # Pedirle al usuario buscar el archivo CSV a importar
        filename =  filedialog.askopenfilename(initialdir = "/", 
            title = "Seleccione el archivo", 
            filetypes = (("Archivos CSV","*.csv"),("Todos los archivos","*.*")))
        if filename is not "":
            # Eliminamos los registros de la tabla para hacer un import limpio

            # Obtener todos los IDs
            fetch = requests.get(invitados_url, headers=headers)
            readable_response = fetch.json()
            ids = []
            for data in readable_response["invitados"]:
                ids.append(data[0])

            # Borrar todos los registros
            for item in ids:
                payload = '{"num_emp": " '+ str(item) +'"}'
                response = requests.delete(invitados_url, data=payload, headers=headers)
            
            # Leer archivo
            filename.encode('utf-8')
            with open(filename) as f:
                reader = csv.reader(f)
                for field in reader:
                    # importar a la tabla
                    print (field)
                    payload = '{"num_emp": " '+ str(field[0]) +'","nombres": "' + str(field[1]) + '","apellidos": "' + str(field[2]) + '","asistio": "' + str(field[3]) + '"}'
                    response = requests.post(invitados_url, data=payload, headers=headers)
                    print (response)
            # Actualizar treeview
            Read()
    except Exception as exception:
        txt_result.config(text="Error al insertar datos en la DB", fg="red")
        print (exception)
    else:
        if filename is not "":
            txt_result.config(text="Registros importados exitosamente.", 
                fg="green")
    finally:
        NUM_EMP.set("")
        NOMBRES.set("")
        APELLIDOS.set("")
        ASISTIO.set("")
        # Llamar a la funcion count_assistance para actualizar los 
        # valores necesarios
        count_assistance()


# Crear registro.
def Create():
    if NUM_EMP.get() == "" or NOMBRES.get() == "" or APELLIDOS.get() == "" or \
        ASISTIO.get() == "":
        txt_result.config(text="Primero introduzca todos los valores en la parte izquierda.", 
            fg="red")
    else:
        try:
            payload = '{"num_emp": " '+ num_emp.get() +'","nombres": "' + str(NOMBRES.get()) + '","apellidos": "' + str(APELLIDOS.get()) + '","asistio": "' + str(ASISTIO.get()) + '"}'
            response = requests.post(invitados_url, data=payload, headers=headers)
            print (response)
            tree.delete(*tree.get_children())
            Read()
        except Exception as exception:
            txt_result.config(text="Error al insertar datos en la DB", fg="red")
            print (exception)
        else:
            txt_result.config(text="Registro creado existosamente.", fg="green")
        finally:
            NUM_EMP.set("")
            NOMBRES.set("")
            APELLIDOS.set("")
            ASISTIO.set("")
            # Llamar a la funcion count_assistance para actualizar los 
            # valores necesarios
            count_assistance()


# Leer todos los datos de la tabla.
def Read():
    try:
        tree.delete(*tree.get_children())
        fetch = requests.get(invitados_url, headers=headers)
        readable_response = fetch.json()
        for data in readable_response["invitados"]:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3]))
    except Exception as exception:
        txt_result.config(text="Error al leer datos de la DB", fg="red")
        print (exception)
    else:
        txt_result.config(text="Datos leidos correctamente", fg="green")


# Exportar datos a un archivo separado por comas.
def csv_export():
    try:
        fetch = requests.get(invitados_url, headers=headers)
        readable_response = fetch.json()
        with open('invitados.csv', 'w', newline='') as f:
            for data in readable_response["invitados"]:
                w=csv.writer(f)
                w.writerow(data)
    except Exception as exception:
        txt_result.config(text="Error al exportar datos a ./invitados.csv", 
            fg="red")
        print (exception)
    else:
        txt_result.config(text="Datos exportados correctamente a ./invitados.csv", 
            fg="green")


# Actualizar registro seleccionado.
def Update():
    if ASISTIO.get() == "":
        txt_result.config(text="Por favor seleccione si el invitado asistio o no", 
            fg="red")
    else:
        tree.delete(*tree.get_children())
        payload = '{"num_emp": " '+ num_emp.get() +'","nombres": "' + str(NOMBRES.get()) + '","apellidos": "' + str(APELLIDOS.get()) + '","asistio": "' + str(ASISTIO.get()) + '"}'
        response = requests.put(invitados_url, data=payload, headers=headers)
        print (response)
        Read()
        NUM_EMP.set("")
        NOMBRES.set("")
        APELLIDOS.set("")
        ASISTIO.set("")
        btn_create.config(state=NORMAL)
        btn_update.config(state=DISABLED)
        btn_asist.config(state=DISABLED)
        btn_delete.config(state=NORMAL)
        txt_result.config(text="Datos actualizados exitosamente.", fg="green")
    # Llamar a la funcion count_assistance para actualizar los 
    # valores necesarios
    count_assistance()


# Registrar asistencia del invitado seleccionado.
def registrar_asistencia():
    if not tree.selection():
        txt_result.config(text="Por favor seleccione un registro primero", 
            fg="red")
    else:
        tree.delete(*tree.get_children())
        payload = '{"num_emp": " '+ num_emp.get() +'","nombres": "' + str(NOMBRES.get()) + '","apellidos": "' + str(APELLIDOS.get()) + '","asistio": "Si"}'
        response = requests.put(invitados_url, data=payload, headers=headers)
        print (response)
        Read()
        NUM_EMP.set("")
        NOMBRES.set("")
        APELLIDOS.set("")
        ASISTIO.set("")
        btn_create.config(state=NORMAL)
        btn_update.config(state=NORMAL)
        btn_asist.config(state=NORMAL)
        btn_delete.config(state=NORMAL)
        txt_result.config(text="Datos actualizados exitosamente.", fg="green")
        # Llamar a la funcion count_assistance para actualizar los 
        # valores necesarios
        count_assistance()


# Trigger para seleccionar registros.
def OnSelected(event):
    global NUM_EMP;
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    #NUM_EMP = selecteditem[0]
    NUM_EMP.set("")
    NOMBRES.set("")
    APELLIDOS.set("")
    ASISTIO.set("")
    NUM_EMP.set(selecteditem[0])
    NOMBRES.set(selecteditem[1])
    APELLIDOS.set(selecteditem[2])
    ASISTIO.set(selecteditem[3])
    btn_create.config(state=NORMAL)
    btn_update.config(state=NORMAL)
    btn_delete.config(state=NORMAL)
    btn_asist.config(state=NORMAL)


# Contar las personas que han asistido hasta el momento.
def count_assistance():
    global asistentes
    global percentage
    asistentes = 0
    percentage = 0
    item_count = len(tree.get_children())
    for item in tree.get_children():
        if (tree.set(item, "ASISTIO")) == 'Si':
            asistentes +=1
    if item_count > 0:
        percentage = round((asistentes/item_count)*100, 2)
    # Actualizar el label.
    txt_assistance.config(text="Asistentes: " + str(asistentes) + " de " + \
        str(item_count) + " (" + str(percentage) + "%)")


# Eliminar registro seleccionado.
def Delete():
    global mydb
    if not tree.selection():
        txt_result.config(text="Por favor primero seleccione el registro a eliminar.", 
            fg="red")
    else:
        # Pedir confirmacion antes de eliminar el registro.
        result = tkMessageBox.askquestion('UACH - Sistema de manejo de invitados', 
            'Realmente desea eliminar este registro?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            try:
                tree.delete(curItem)
                payload = '{"num_emp": " '+ num_emp.get() +'"}'
                response = requests.delete(invitados_url, data=payload, headers=headers)
            except Exception as exception:
                txt_result.config(text="Error al eliminar registro", fg="red")
                print (exception)
            else:
                txt_result.config(text="Registro eliminado exitosamente", 
                    fg="green")    
            finally:
                NUM_EMP.set("")
                NOMBRES.set("")
                APELLIDOS.set("")
                ASISTIO.set("")
                # Llamar a la funcion count_assistance para actualizar los 
                # valores necesarios
                count_assistance()


# Actualizar la hora mostrada cada 100 milisegundos.
def clock():
    txt_clock.config(text="Hora actual: " + time.strftime('%H:%M'))
    root.after(100, clock)


# Salir
def Exit():
    result = tkMessageBox.askquestion('UACH - Sistema de manejo de invitados', 
        'Realmente desea salir del sistema?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


#==================================VARIABLES====================================
NUM_EMP = StringVar()
NOMBRES = StringVar()
APELLIDOS = StringVar()
ASISTIO = StringVar()


#==================================FRAME========================================
Top = Frame(root, width=900, height=50, bd=8, relief="ridge", background='white')
Top.pack(side=TOP)

# Mostrar el logo de la UACH, en la esquina superior izquierda.
logo_uach = "logo_uach.png"
logo_uach = Image.open(logo_uach)
logo_uach = logo_uach.resize((80, 80), Image.ANTIALIAS)
logo_uach = ImageTk.PhotoImage(logo_uach)
img_logo1 = Label(Top, image = logo_uach, background='white')
img_logo1.pack(side=LEFT)

# Mostrar el logo de la FING, en la esquina superior derecha.
logo_ingenieria = "logo_ingenieria.png"
logo_ingenieria = Image.open(logo_ingenieria)
logo_ingenieria = logo_ingenieria.resize((80, 80), Image.ANTIALIAS)
logo_ingenieria = ImageTk.PhotoImage(logo_ingenieria)
img_logo2 = Label(Top, image = logo_ingenieria, background='white')
img_logo2.pack(side=RIGHT)

Buttons = Frame(root, width=300, height=100, bd=8, relief="flat")
Buttons.pack(side=TOP)

Right = Frame(root, width=600, height=200, bd=8, relief="raise")
Right.pack(side=RIGHT)

Left = Frame(root, width=600, height=300, bd=8, relief="raise")
Left.pack(side=LEFT)

Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)

RadioGroup = Frame(Forms)
Si = Radiobutton(RadioGroup, text="Si", variable=ASISTIO, value="Si", 
    font=('arial', 16)).pack(side=LEFT)
No = Radiobutton(RadioGroup, text="No", variable=ASISTIO, value="No", 
    font=('arial', 16)).pack(side=LEFT)


#==================================WIDGET DE LABELS=============================
time_string = "Hora actual: " + time.strftime('%H:%M')
txt_clock = Label(Top, width=300, font=('arial', 24), text = time_string, 
    background='white', compound = CENTER)
txt_clock.pack()
txt_assistance = Label(Top, width=300, font=('arial', 24), 
    text = "Asistentes: ", background='white', compound = CENTER)
txt_assistance.pack()
txt_num_emp = Label(Forms, text="# de empleado:", font=('arial', 16), bd=15)
txt_num_emp.grid(row=0, sticky="e")
txt_nombres = Label(Forms, text="Nombre(s):", font=('arial', 16), bd=15)
txt_nombres.grid(row=1, sticky="e")
txt_apellidos = Label(Forms, text="Apellido(s):", font=('arial', 16), bd=15)
txt_apellidos.grid(row=2, sticky="e")
txt_ASISTIO = Label(Forms, text="Asistio?:", font=('arial', 16), bd=15)
txt_ASISTIO.grid(row=3, sticky="e")
txt_result = Label(Buttons)
txt_result.pack(side=TOP)


#==================================WIDGET DE CAPTURA============================
num_emp = Entry(Forms, textvariable=NUM_EMP, width=30)
num_emp.grid(row=0, column=1)
nombres = Entry(Forms, textvariable=NOMBRES, width=30)
nombres.grid(row=1, column=1)
apellidos = Entry(Forms, textvariable=APELLIDOS, width=30)
apellidos.grid(row=2, column=1)
RadioGroup.grid(row=3, column=1)


#==================================WIDGET DE BOTONES============================
btn_create = Button(Buttons, width=12, text="Agregar invitado", command=Create)
btn_create.pack(side=LEFT)
btn_update = Button(Buttons, width=12, text="Actualizar registro", 
    command=Update, state=DISABLED)
btn_update.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Borrar registro", 
    command=Delete)
btn_delete.pack(side=LEFT)
btn_import = Button(Buttons, width=12, text="Importar de CSV", 
    command=import_csv)
btn_import.pack(side=LEFT)
btn_export = Button(Buttons, width=10, text="Exportar a CSV", 
    command=csv_export)
btn_export.pack(side=LEFT)
btn_asist = Button(Buttons, width=13, text="Registrar asistencia", 
    command=registrar_asistencia)
btn_asist.pack(side=LEFT)
btn_exit = Button(Buttons, width=3, text="Salir", 
    command=Exit)
btn_exit.pack(side=LEFT)

#==================================WIDGET TREEVIEW==============================
scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=("num_emp", "nombres", "apellidos", 
    "ASISTIO"), selectmode="extended", height=300, \
    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('num_emp', text="# Emp.", anchor=W)
tree.heading('nombres', text="Nombre(s)", anchor=W)
tree.heading('apellidos', text="Apellido(s)", anchor=W)
tree.heading('ASISTIO', text="Asistio?", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=60)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=100)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

# Cargar los datos (si es que los hay), al iniciar la aplicacion.
Read()

# Mantener la hora actualizada.
clock()

# Contar las personas que han asistido hasta el momento.
count_assistance()

# Mostrar mensaje de bienvenida.
txt_result.config(text="Bienvenido al sistema de registro de invitados de la UACH", 
    fg="blue")


#==================================INICIALIZACION===============================
if __name__ == '__main__':
    # INITIATE SELF-DESTRUCTION PROTOCOL!!
    root.protocol("WM_DELETE_WINDOW", Exit)
    # INITIATE MAIN-LOOP PROTOCOL!!
    root.mainloop()
