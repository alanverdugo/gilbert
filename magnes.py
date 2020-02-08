"""
Mages - A graphical application to learn electricity and magnetism.

Usage:
    python invitados.py

Optional arguments:
    None

Description:

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

Author:

"""

# Asegurarnos de que el sistema tiene instalados los modulos necesarios,
# De no ser asi, informar al usuario.
try:
    from tkinter import*
    import sys
    import tkinter.ttk as ttk
    import tkinter.messagebox as tkMessageBox
    from PIL import ImageTk, Image
except ImportError:
    print('Los modulos siguientes son necesarios para el correcto funcionamiento '\
        + 'de este sistema:\n\tsys\n\ttkinter\n\tpillow')
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

#==================================METODOS======================================

def close():
    """Exit application."""
    result = tkMessageBox.askquestion('Do you really want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        sys.exit()


#==================================VARIABLES====================================
NUM_EMP = StringVar()
NOMBRES = StringVar()
APELLIDOS = StringVar()
ASISTIO = StringVar()


#==================================FRAME========================================
Top = Frame(root, width=900, height=50, bd=8, relief="ridge", background='white')
Top.pack(side=TOP)

# Mostrar el logo de la UACH, en la esquina superior izquierda.
LOGO_UACH = "logo_uach.png"
LOGO_UACH = Image.open(LOGO_UACH)
LOGO_UACH = LOGO_UACH.resize((80, 80), Image.ANTIALIAS)
LOGO_UACH = ImageTk.PhotoImage(LOGO_UACH)
img_logo1 = Label(Top, image=LOGO_UACH, background='white')
img_logo1.pack(side=LEFT)

# Mostrar el logo de la FING, en la esquina superior derecha.
LOGO_ING = "logo_ingenieria.png"
LOGO_ING = Image.open(LOGO_ING)
LOGO_ING = LOGO_ING.resize((80, 80), Image.ANTIALIAS)
LOGO_ING = ImageTk.PhotoImage(LOGO_ING)
img_logo2 = Label(Top, image=LOGO_ING, background='white')
img_logo2.pack(side=RIGHT)

Buttons = Frame(root, width=300, height=100, bd=8, relief="flat")
Buttons.pack(side=TOP)

Right = Frame(root, width=600, height=200, bd=8, relief="raise")
Right.pack(side=RIGHT)

Left = Frame(root, width=600, height=300, bd=8, relief="raise")
Left.pack(side=LEFT)

Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)



#==================================WIDGET DE LABELS=============================
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


#==================================WIDGET DE BOTONES============================
BTN_EXIT = Button(Buttons, width=3, text="Salir", command=close)
BTN_EXIT.pack(side=LEFT)

#==================================WIDGET TREEVIEW==============================
scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right,
                    columns=("num_emp", "nombres", "apellidos", "ASISTIO"),
                    selectmode="extended",
                    height=300,
                    yscrollcommand=scrollbary.set,
                    xscrollcommand=scrollbarx.set)
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
#tree.bind('<Double-Button-1>', OnSelected)

# Mostrar mensaje de bienvenida.
txt_result.config(text="Welcome", fg="blue")


#==================================INICIALIZACION===============================
if __name__ == '__main__':
    # INITIATE SELF-DESTRUCTION PROTOCOL!!
    root.protocol("WM_DELETE_WINDOW", close)
    # INITIATE MAIN-LOOP PROTOCOL!!
    root.mainloop()
