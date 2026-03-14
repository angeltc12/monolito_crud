import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
from reportlab.pdfgen import canvas
import re
from tkcalendar import DateEntry
from dotenv import load_dotenv

load_dotenv()


class MonolitoGastronomicoPro:

    def __init__(self, root):

        self.root = root
        self.root.title("Sistema Gastronómico")
        self.root.geometry("1350x850")

        # --------------------------
        # RUTAS BASE
        # --------------------------

        self.base_path = os.path.dirname(__file__)
        self.icon_path = os.path.join(self.base_path, "assets", "icons")

        # --------------------------
        # CARPETA FOTOS EMPLEADOS
        # --------------------------

        self.empleados_img_path = os.path.join(self.base_path, "assets", "empleados")

        if not os.path.exists(self.empleados_img_path):
            os.makedirs(self.empleados_img_path)

        # imagen actual empleado
        self.foto_actual = None


        # --------------------------
        # CARPETA IMAGENES MENU
        # --------------------------

        self.menu_img_path = os.path.join(self.base_path, "assets", "menu")

        if not os.path.exists(self.menu_img_path):
            os.makedirs(self.menu_img_path)

        # --------------------------
        # CARPETA IMAGENES INVENTARIO
        # --------------------------

        self.inventario_img_path = os.path.join(self.base_path, "assets", "inventario")

        if not os.path.exists(self.inventario_img_path):
            os.makedirs(self.inventario_img_path)

        # imagen actual producto
        self.foto_producto = None


        try:
            root.state("zoomed")
        except:
            pass


        # --------------------------
        # ICONOS
        # --------------------------

        def icon(name, size=(18, 18)):
            path = os.path.join(self.icon_path, name)
            img = Image.open(path)
            img = img.resize(size)
            return ImageTk.PhotoImage(img)

        self.ico_add = icon("add.png")
        self.ico_delete = icon("delete.png")
        self.ico_edit = icon("edit.png")
        self.ico_excel = icon("excel.png")
        self.ico_pdf = icon("pdf.png")
        self.ico_search = icon("search.png")

        self.ico_inventory = icon("inventory.png", (20, 20))
        self.ico_menu = icon("menu.png", (20, 20))
        self.ico_employee = icon("employee.png", (20, 20))
        self.ico_restaurant = icon("restaurant.png", (20, 20))
        self.ico_dashboard = icon("dashboard.png", (20, 20))

        # favicon
        try:
            self.root.iconbitmap(os.path.join(self.icon_path, "favicon.ico"))
        except:
            pass

        # --------------------------
        # DB
        # --------------------------

        self.db = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME")
        }

        # --------------------------
        # TEMA
        # --------------------------

        self.tema = "dark"

        self.color_bg = "#0f172a"
        self.color_card = "#1e293b"
        self.color_texto = "white"
        self.color_acento = "#22c55e"

        self.root.configure(bg=self.color_bg)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.estilos()

        # --------------------------
        # HEADER
        # --------------------------

        header = tk.Frame(root, bg="#020617", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="  Sistema Gastronómico PRO",
            image=self.ico_dashboard,
            compound="left",
            bg="#020617",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=20)

        btnTema = tk.Button(
            header,
            text=" Cambiar Tema",
            image=self.ico_edit,
            compound="left",
            command=self.cambiar_tema,
            bg=self.color_acento,
            fg="white",
            bd=0,
            padx=10
        )

        btnTema.pack(side="right", padx=20)

        # --------------------------
        # DASHBOARD
        # --------------------------

        self.frameDash = tk.Frame(root, bg=self.color_bg)
        self.frameDash.pack(fill="x", padx=20, pady=10)

        self.crear_dashboard()

        # --------------------------
        # NOTEBOOK
        # --------------------------

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill="both", padx=20, pady=10)

        self.modulo_inventario()
        self.modulo_menu()
        self.modulo_empleados()
        self.modulo_sedes()

    # --------------------------
    # ESTILOS
    # --------------------------

    def estilos(self):

        self.style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=30,
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    # --------------------------
    # QUERY DB
    # --------------------------

    def query(self, q, params=None, fetch=False):

        try:

            conn = mysql.connector.connect(**self.db)
            cur = conn.cursor()

            cur.execute(q, params or ())

            if fetch:
                data = cur.fetchall()
            else:
                data = None

            conn.commit()
            conn.close()

            return data

        except Error as e:
            messagebox.showerror("SQL", str(e))


    def validar_numero(self, valor):

        if valor == "":
            return True

        try:
            float(valor)
            return True
        except ValueError:
            self.root.bell()
            return False


    # --------------------------
    # VALIDACIONES
    # --------------------------

    def validar_campos(self, entries):

        for label, entry in entries.items():

            valor = entry.get().strip()

            # Quitar borde rojo solo si es Entry normal
            if not isinstance(entry, DateEntry):
                entry.configure(highlightthickness=0)

            # Campo vacío
            if valor == "":

                if not isinstance(entry, DateEntry):
                    entry.configure(
                        highlightbackground="red",
                        highlightcolor="red",
                        highlightthickness=2
                    )

                messagebox.showwarning(
                    "Campo obligatorio",
                    f"El campo '{label}' no puede estar vacío."
                )

                entry.focus()
                return False


            # Validar números
            if label.lower() in ["stock", "costo", "precio", "capacidad", "telefono"]:

                # quitar puntos para validar numero real
                numero = valor.replace(".", "")

                if not numero.isdigit():
                    try:
                        entry.configure(
                            highlightbackground="red",
                            highlightcolor="red",
                            highlightthickness=2
                        )
                    except:
                        pass

                    messagebox.showerror(
                        "Error de validación",
                        f"El campo '{label}' solo acepta números.\n\nEjemplo:\n100\n5.000\n100.000"
                    )

                    entry.focus()
                    return False

                numero = int(numero)

                # limites
                if label.lower() in ["stock", "costo", "precio", "capacidad", "telefono"]:

                    # quitar puntos para validar
                    numero = valor.replace(".", "")

                    if not numero.isdigit():
                        entry.configure(
                            highlightbackground="red",
                            highlightcolor="red",
                            highlightthickness=2
                        )

                        messagebox.showerror(
                            "Error de validación",
                            f"El campo '{label}' solo acepta números enteros.\n\nEjemplo válido:\n100\n5.000\n100.000"
                        )

                        entry.focus()
                        return False



            # --------------------------
            # VALIDAR SOLO LETRAS
            # --------------------------

            if label.lower() in ["nombre", "nombres", "apellidos", "plato", "categoria", "nombre sede"]:
                if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", valor):
                    entry.configure(
                        highlightbackground="red",
                        highlightcolor="red",
                        highlightthickness=2
                    )

                    messagebox.showerror(
                        "Error de validación",
                        f"El campo '{label}' solo acepta letras.\n\nEjemplo válido:\nHarina de trigo"
                    )

                    entry.focus()
                    return False

            # Validar email
            if label.lower() == "email":
                patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|net|org|edu|gov|co|es|mx|ar|us|uk|com\.co|com\.mx|com\.ar|co\.uk)$"

                if not re.match(patron, valor):

                    entry.configure(highlightbackground="red", highlightcolor="red", highlightthickness=2)

                    messagebox.showwarning(
                        "Email inválido",
                        "Ingresa un correo electrónico válido."
                    )

                    entry.focus()
                    return False

        return True

    def validar_texto(self, valor):

        if valor == "":
            return True

        if re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$", valor):
            return True
        else:
            self.root.bell()
            return False

    def validar_email_input(self, valor):

        if valor == "":
            return True

        patron = r"^[A-Za-z0-9@._\-]*$"

        if re.match(patron, valor):
            return True
        else:
            self.root.bell()
            return False

    # --------------------------
    # DASHBOARD 1
    # --------------------------

    def crear_dashboard(self):

        for w in self.frameDash.winfo_children():
            w.destroy()

        def card(titulo, valor, color):

            f = tk.Frame(self.frameDash, bg=self.color_card, width=200, height=90)
            f.pack(side="left", padx=10)

            tk.Label(
                f,
                text=titulo,
                bg=self.color_card,
                fg="gray",
                font=("Segoe UI", 10)
            ).pack(anchor="w", padx=10, pady=5)

            tk.Label(
                f,
                text=str(valor),
                bg=self.color_card,
                fg=color,
                font=("Segoe UI", 18, "bold")
            ).pack(anchor="w", padx=10)

        inv = self.query("SELECT COUNT(*) FROM inventario", fetch=True)
        menu = self.query("SELECT COUNT(*) FROM menu", fetch=True)
        emp = self.query("SELECT COUNT(*) FROM empleados", fetch=True)

        card("Productos", inv[0][0] if inv else 0, "#38bdf8")
        card("Platillos", menu[0][0] if menu else 0, "#4ade80")
        card("Empleados", emp[0][0] if emp else 0, "#f59e0b")

    # --------------------------
    # FORMULARIO BASE
    # --------------------------

    def crear_layout(self, frame, tabla, campos):

        tabla_actual = tabla
        campos_actuales = campos

        izquierda = tk.LabelFrame(
            frame,
            text="Formulario",
            bg=self.color_card,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=20
        )

        izquierda.pack(side="left", fill="y", padx=10, pady=10)

        entries = {}

        # --------------------------
        # CABECERA FORMULARIO
        # --------------------------

        header_form = tk.Frame(izquierda, bg=self.color_card)
        header_form.pack(fill="x", pady=(0, 10))

        tk.Label(
            header_form,
            text="Formulario",
            bg=self.color_card,
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")

        varID = tk.StringVar(value="Nuevo")

        tk.Label(
            header_form,
            text="ID:",
            bg=self.color_card,
            fg="white"
        ).pack(side="right", padx=(10, 5))

        tk.Entry(
            header_form,
            textvariable=varID,
            width=10,
            state="readonly"
        ).pack(side="right")

        for label, col in campos.items():

            tk.Label(izquierda, text=label, bg=self.color_card, fg="white").pack(anchor="w")

            vcmd_num = (self.root.register(self.validar_numero), "%P")
            vcmd_text = (self.root.register(self.validar_texto), "%P")
            vcmd_email = (self.root.register(self.validar_email_input), "%P")

            # CAMPO FECHA (CALENDARIO)
            if "fecha" in col:

                ent = DateEntry(
                    izquierda,
                    width=27,
                    date_pattern="yyyy-mm-dd",
                    state="readonly",
                    showweeknumbers=False
                )

                ent.bind("<FocusOut>", lambda e: "break")

            # EMAIL
            elif label.lower() == "email":

                ent = tk.Entry(
                    izquierda,
                    width=30,
                    validate="key",
                    validatecommand=vcmd_email
                )

            # CAMPOS NUMERICOS
            elif label.lower() in ["stock", "costo", "precio", "capacidad", "telefono"]:

                ent = tk.Entry(
                    izquierda,
                    width=30,
                    validate="key",
                    validatecommand=vcmd_num
                )

            # CAMPOS TEXTO
            # DIRECCION (permite letras y numeros)
            elif label.lower() == "direccion":

                ent = tk.Entry(
                    izquierda,
                    width=30
                )

            # CAMPOS TEXTO
            else:

                ent = tk.Entry(
                    izquierda,
                    width=30,
                    validate="key",
                    validatecommand=vcmd_text
                )

            ent.pack(pady=5)

            entries[label] = ent

        # BOTONES

        def limpiar():
            varID.set("Nuevo")

            for e in entries.values():
                try:
                    e.delete(0, tk.END)  # funciona para Entry normal
                except:
                    e.set_date("")  # funciona para DateEntry

        def guardar():

            # VALIDACIONES
            if not self.validar_campos(entries):
                return

            valores = [e.get().strip() for e in entries.values()]
            cols = list(campos.values())

            # guardar foto si es empleados
            if tabla == "empleados" and self.foto_actual:
                cols.append("foto")
                valores.append(self.foto_actual)

            elif tabla == "menu":
                data = self.query(
                    f"SELECT id,{','.join(campos.values())},imagen FROM {tabla}",
                    fetch=True
                )

            else:
                data = self.query(
                    f"SELECT id,{','.join(campos.values())} FROM {tabla}",
                    fetch=True
                )

            if varID.get() == "Nuevo":

                if tabla == "empleados":
                    cols.append("foto")
                    valores.append(self.foto_actual)

                if tabla == "menu":
                    cols.append("imagen")
                    valores.append(self.foto_producto)

                if varID.get() == "Nuevo":

                    if tabla == "inventario":
                        q = "CALL sp_insert_inventario(%s,%s,%s)"

                    elif tabla == "menu":
                        q = "CALL sp_insert_menu(%s,%s,%s,%s)"

                    elif tabla == "empleados":
                        q = "CALL sp_insert_empleado(%s,%s,%s,%s,%s)"

                    elif tabla == "sedes":
                        q = "CALL sp_insert_sede(%s,%s,%s,%s)"

                    self.query(q, valores)


            else:

                if tabla == "empleados":
                    cols.append("foto")

                    valores.append(self.foto_actual)

                if tabla == "menu":
                    cols.append("imagen")

                    valores.append(self.foto_producto)

                else:

                    if tabla == "inventario":
                        q = "CALL sp_update_inventario(%s,%s,%s,%s)"
                        valores = [varID.get()] + valores

                    elif tabla == "menu":
                        q = "CALL sp_update_menu(%s,%s,%s,%s,%s)"
                        valores = [varID.get()] + valores

                    elif tabla == "empleados":
                        q = "CALL sp_update_empleado(%s,%s,%s,%s,%s,%s)"
                        valores = [varID.get()] + valores

                    elif tabla == "sedes":
                        q = "CALL sp_update_sede(%s,%s,%s,%s,%s)"
                        valores = [varID.get()] + valores

                    self.query(q, valores)


                valores.append(varID.get())

                self.query(q, valores)

            actualizar()
            limpiar()
            self.crear_dashboard()

        def eliminar():

            if varID.get() == "Nuevo":
                messagebox.showwarning("Eliminar", "Selecciona un registro primero.")
                return

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Seguro que deseas eliminar este registro?"
            )

            if not confirmar:
                return

            if tabla == "inventario":
                q = "CALL sp_delete_inventario(%s)"

            elif tabla == "menu":
                q = "CALL sp_delete_menu(%s)"

            elif tabla == "empleados":
                q = "CALL sp_delete_empleado(%s)"

            elif tabla == "sedes":
                q = "CALL sp_delete_sede(%s)"

            self.query(q, (varID.get(),))

            actualizar()
            limpiar()
            self.crear_dashboard()

        tk.Button(izquierda, text=" Guardar", image=self.ico_add, compound="left",
                  command=guardar, bg="#22c55e", fg="white").pack(fill="x", pady=5)


        # TABLA DERECHA

        derecha = tk.Frame(frame, bg=self.color_bg)
        derecha.pack(side="right", expand=True, fill="both")

        search_frame = tk.Frame(derecha, bg=self.color_bg)
        search_frame.pack(fill="x")

        tk.Label(search_frame, image=self.ico_search, bg=self.color_bg).pack(side="left", padx=5)

        tk.Label(search_frame, text="Buscar:", bg=self.color_bg, fg="white").pack(side="left", padx=5)

        buscar = tk.Entry(search_frame)
        buscar.pack(side="left", fill="x", expand=True, padx=5)

        # usar el mismo campo para exportar
        filtro_export = buscar
        # --------------------------
        # FUNCIÓN FILTRAR
        # --------------------------

        def filtrar():

            texto = buscar.get().strip()

            for i in tree.get_children():
                tree.delete(i)

            if texto:

                consulta = f"""
                SELECT id,{','.join(campos.values())}
                FROM {tabla}
                WHERE LOWER(CONCAT_WS(' ',{','.join(campos.values())})) LIKE LOWER(%s)
                """

                data = self.query(consulta, (f"%{texto}%",), fetch=True)

            else:

                data = self.query(
                    f"SELECT id,{','.join(campos.values())} FROM {tabla}",
                    fetch=True
                )

            if data:
                for r in data:
                    tree.insert("", tk.END, values=r)

        # filtrar mientras escribes
        buscar.bind("<KeyRelease>", lambda e: filtrar())

        tk.Button(
            search_frame,
            text="Buscar",
            image=self.ico_search,
            compound="left",
            command=filtrar
        ).pack(side="left", padx=5)

        # --------------------------
        # FILTRO PARA EXPORTACIÓN
        # --------------------------



        cols = ["ID"] + list(campos.keys())

        tree = ttk.Treeview(derecha, columns=cols, show="headings")

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=140)

        tree.pack(expand=True, fill="both")

        scroll = ttk.Scrollbar(derecha, command=tree.yview)
        tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")

        def actualizar():

            for i in tree.get_children():
                tree.delete(i)

            if tabla == "empleados":
                data = self.query(
                    f"SELECT id,{','.join(campos.values())},foto FROM {tabla}",
                    fetch=True
                )

            elif tabla == "menu":
                data = self.query(
                    f"SELECT id,{','.join(campos.values())},imagen FROM {tabla}",
                    fetch=True
                )

            else:
                data = self.query(
                    f"SELECT id,{','.join(campos.values())} FROM {tabla}",
                    fetch=True
                )

            if data:
                for r in data:
                    tree.insert("", tk.END, values=r)

        tree.bind("<<TreeviewSelect>>",
                  lambda e: self.autocargar(tree, varID, list(entries.values())))


           # EXPORT Exel

        def export_excel():

            # aplicar filtro si existe
            filtro = filtro_export.get().strip()

            if filtro:
                consulta = f"""
                SELECT id,{','.join(campos.values())}
                FROM {tabla}
                WHERE LOWER(CONCAT_WS(' ',{','.join(campos.values())})) LIKE LOWER(%s)
                """

                data = self.query(consulta, (f"%{filtro}%",), fetch=True)
            else:
                data = self.query(
                    f"SELECT id,{','.join(campos.values())} FROM {tabla}",
                    fetch=True
                )

            if not data:
                messagebox.showinfo("Excel", "No hay datos para exportar.")
                return

            path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )

            if not path:
                return

            columnas = ["ID"] + list(campos.keys())

            df = pd.DataFrame(data, columns=columnas)

            df.to_excel(path, index=False)

            messagebox.showinfo("Excel", "Archivo Excel exportado correctamente.")

        # EXPORT pdf
        def export_pdf():

            path = filedialog.asksaveasfilename(defaultextension=".pdf")

            if not path:
                return

            filtro = filtro_export.get().strip()


            if filtro:
                consulta = f"""
                SELECT * FROM {tabla}
                WHERE LOWER(CONCAT_WS(' ',{','.join(campos.values())})) LIKE LOWER(%s)
                """

                data = self.query(consulta, (f"%{filtro}%",), fetch=True)
            else:
                data = self.query(f"SELECT * FROM {tabla}", fetch=True)

            c = canvas.Canvas(path)

            y = 800

            # TITULO
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, f"Reporte de {tabla.upper()}")

            y -= 40

            c.setFont("Helvetica-Bold", 10)

            headers = ["ID"] + list(campos.keys())

            x = 50

            for h in headers:
                c.drawString(x, y, h)
                x += 120

            y -= 20

            c.setFont("Helvetica", 10)

            for row in data:

                x = 50

                for value in row[:len(headers)]:
                    c.drawString(x, y, str(value))
                    x += 120

                y -= 20

                if y < 50:
                    c.showPage()
                    y = 800

            c.save()

        botones_frame = tk.Frame(derecha, bg=self.color_bg)
        botones_frame.pack(fill="x", pady=5)

        tk.Button(botones_frame, text=" Excel", image=self.ico_excel,
                  compound="left", command=export_excel).pack(side="left", padx=5)

        tk.Button(botones_frame, text=" PDF", image=self.ico_pdf,
                  compound="left", command=export_pdf).pack(side="left", padx=5)

        tk.Button(botones_frame, text=" Eliminar", image=self.ico_delete,
                  compound="left", command=eliminar,
                  bg="#ef4444", fg="white").pack(side="left", padx=5)

        tk.Button(botones_frame, text=" Limpiar",
                  command=limpiar).pack(side="left", padx=5)
        actualizar()

    def autocargar(self, tree, var_id, entry_list):

        sel = tree.selection()

        if not sel:
            return

        valores = tree.item(sel)['values']

        var_id.set(valores[0])

        for i, ent in enumerate(entry_list):

            valor = valores[i + 1]

            try:
                ent.delete(0, tk.END)
                ent.insert(0, valor)
            except:
                ent.set_date(valor)

        # mostrar foto si existe
        if len(valores) > len(entry_list) + 1:

            ruta = valores[-1]

            if ruta:

                ruta_emp = os.path.join(self.empleados_img_path, ruta)
                ruta_menu = os.path.join(self.menu_img_path, ruta)

                ruta_real = None

                if os.path.exists(ruta_emp):
                    ruta_real = ruta_emp

                elif os.path.exists(ruta_menu):
                    ruta_real = ruta_menu

                if ruta_real:

                    img = Image.open(ruta_real)
                    img.thumbnail((160, 160))

                    foto = ImageTk.PhotoImage(img)

                    if hasattr(self, "preview_empleado"):
                        self.preview_empleado.configure(image=foto)
                        self.preview_empleado.image = foto

                    if hasattr(self, "preview_menu"):
                        self.preview_menu.configure(image=foto)
                        self.preview_menu.image = foto

            # mostrar foto si existe
            if len(valores) > len(entry_list) + 1:

                ruta = valores[-1]

                if ruta:

                    ruta_emp = os.path.join(self.empleados_img_path, ruta)
                    ruta_menu = os.path.join(self.menu_img_path, ruta)

                    ruta_real = None

                    if os.path.exists(ruta_emp):
                        ruta_real = ruta_emp

                    elif os.path.exists(ruta_menu):
                        ruta_real = ruta_menu

                    if ruta_real:

                        img = Image.open(ruta_real)
                        img.thumbnail((160, 160))

                        foto = ImageTk.PhotoImage(img)

                        if hasattr(self, "preview_empleado"):
                            self.preview_empleado.configure(image=foto)
                            self.preview_empleado.image = foto

                        if hasattr(self, "preview_menu"):
                            self.preview_menu.configure(image=foto)
                            self.preview_menu.image = foto

    # --------------------------
    # SUBIR FOTO EMPLEADO
    # --------------------------

    def subir_foto_empleado(self, label_preview):

        path = filedialog.askopenfilename(
            title="Seleccionar foto",
            filetypes=[("Imagen", "*.png *.jpg *.jpeg")]
        )

        if not path:
            return

        img = Image.open(path)

        # recorte cuadrado
        w, h = img.size
        lado = min(w, h)

        img = img.crop((0, 0, lado, lado))

        img.thumbnail((220, 220), Image.LANCZOS)

        preview = ImageTk.PhotoImage(img)

        label_preview.configure(image=preview)
        label_preview.image = preview

        nombre = os.path.basename(path)
        destino = os.path.join(self.empleados_img_path, nombre)

        img.save(destino)

        self.foto_actual = nombre

    def subir_foto_menu(self, label_preview):

        path = filedialog.askopenfilename(
            title="Seleccionar foto",
            filetypes=[("Imagen", "*.png *.jpg *.jpeg")]
        )

        if not path:
            return

        img = Image.open(path).convert("RGB")

        w, h = img.size
        lado = min(w, h)

        x = (w - lado) // 2
        y = (h - lado) // 2

        img = img.crop((x, y, x + lado, y + lado))

        img.thumbnail((220, 220), Image.LANCZOS)

        preview = ImageTk.PhotoImage(img)

        label_preview.configure(image=preview)
        label_preview.image = preview

        import uuid

        nombre = str(uuid.uuid4()) + ".jpg"
        destino = os.path.join(self.menu_img_path, nombre)
        img.save(destino, "JPEG", quality=90)

        # guardar solo nombre (mejor práctica)
        self.foto_producto = nombre


    # --------------------------
    # MODULOS
    # --------------------------

    def modulo_inventario(self):

        f = tk.Frame(self.tabs, bg=self.color_bg)
        self.tabs.add(f, text=" Inventario", image=self.ico_inventory, compound="left")

        self.crear_layout(
            f,
            "inventario",
            {"Nombre": "nombre", "Stock": "cantidad", "Costo": "costo"}
        )

    def modulo_menu(self):

        f = tk.Frame(self.tabs, bg=self.color_bg)
        self.tabs.add(f, text=" Menu", image=self.ico_menu, compound="left")

        self.crear_layout(
            f,
            "menu",
            {"Plato": "nombre", "Precio": "precio", "Categoria": "categoria"}
        )

        # buscar formulario
        izquierda = None
        for widget in f.winfo_children():
            if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Formulario":
                izquierda = widget
                break

        if izquierda is None:
            return

        # --------------------------
        # FOTO DEL PLATO
        # --------------------------

        tk.Label(
            izquierda,
            text="Foto del plato",
            bg=self.color_card,
            fg="white"
        ).pack(anchor="w", pady=(15, 5))

        frame_foto = tk.Frame(
            izquierda,
            width=160,
            height=160,
            bg="#111827"
        )

        frame_foto.pack(pady=10)
        frame_foto.pack_propagate(False)

        preview = tk.Label(frame_foto, bg="#111827")
        preview.pack(expand=True)

        self.preview_menu = preview

        tk.Button(
            izquierda,
            text="Subir Foto",
            command=lambda: self.subir_foto_menu(preview),
            bg=self.color_acento,
            fg="white"
        ).pack(pady=10, fill="x")

    def modulo_empleados(self):

        f = tk.Frame(self.tabs, bg=self.color_bg)
        self.tabs.add(f, text=" Empleados", image=self.ico_employee, compound="left")

        # crear layout base
        self.crear_layout(
            f,
            "empleados",
            {
                "Nombres": "nombres",
                "Apellidos": "apellidos",
                "Telefono": "telefono",
                "Fecha Contratacion": "fecha_contratacion"
            }
        )

        # buscar el formulario
        izquierda = None

        for widget in f.winfo_children():
            if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Formulario":
                izquierda = widget
                break

        if izquierda is None:
            return

        # --------------------------
        # FOTO EMPLEADO
        # --------------------------

        tk.Label(
            izquierda,
            text="Foto empleado",
            bg=self.color_card,
            fg="white"
        ).pack(anchor="w", pady=(15, 5))

        frame_foto = tk.Frame(
            izquierda,
            width=160,
            height=160,
            bg="#111827"
        )

        frame_foto.pack(pady=10)
        frame_foto.pack_propagate(False)

        preview = tk.Label(frame_foto, bg="#111827")
        preview.pack(expand=True)

        self.preview_empleado = preview

        tk.Button(
            izquierda,
            text="Subir Foto",
            command=lambda: self.subir_foto_empleado(preview),
            bg=self.color_acento,
            fg="white"
        ).pack(pady=10, fill="x")


    def modulo_sedes(self):

        f = tk.Frame(self.tabs, bg=self.color_bg)
        self.tabs.add(f, text=" Sedes", image=self.ico_restaurant, compound="left")

        self.crear_layout(
            f,
            "sedes",
            {
                "Nombre Sede": "nombre_sede",
                "Direccion": "direccion",
                "Capacidad": "capacidad",
                "Telefono": "telefono"
            }
        )

    # --------------------------
    # CAMBIAR TEMA
    # --------------------------

    def cambiar_tema(self):

        if self.tema == "dark":

            self.tema = "light"

            self.color_bg = "#f1f5f9"
            self.color_card = "white"
            self.color_texto = "#0f172a"
            self.color_acento = "#2563eb"

        else:

            self.tema = "dark"

            self.color_bg = "#0f172a"
            self.color_card = "#1e293b"
            self.color_texto = "white"
            self.color_acento = "#22c55e"

        self.root.configure(bg=self.color_bg)
        self.frameDash.configure(bg=self.color_bg)

        self.crear_dashboard()


# --------------------------
# MAIN
# --------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = MonolitoGastronomicoPro(root)

    root.mainloop()

# --------------------------
# VALIDACIONES
# -------------------------

