#  Sistema Gastronómico PRO (Arquitectura Monolítica)

Sistema de gestión gastronómica desarrollado en **Python**, utilizando **Tkinter** para la interfaz gráfica y **MySQL** como base de datos.

El sistema sigue una **arquitectura monolítica**, donde toda la lógica de negocio, interfaz gráfica y acceso a datos se encuentran integrados en una sola aplicación.

---

#  Arquitectura del sistema

Este proyecto utiliza una **arquitectura monolítica**, lo que significa que:

* La **interfaz gráfica**
* La **lógica del sistema**
* El **acceso a la base de datos**

se encuentran en una **misma aplicación y mismo código fuente**.

### Ventajas del enfoque monolítico

* Implementación sencilla
* Fácil despliegue
* Ideal para proyectos académicos o sistemas pequeños
* Menor complejidad de infraestructura

### Desventajas

* Escalabilidad limitada
* Mayor acoplamiento entre módulos

---

#  Características principales

* Gestión de **Inventario**
* Gestión de **Menú**
* Gestión de **Empleados**
* Gestión de **Sedes**
* **CRUD completo**
* **Dashboard con estadísticas**
* **Búsqueda y filtrado**
* **Exportación a Excel y PDF**
* **Validaciones de datos**
* **Carga de imágenes**
* **Tema oscuro / claro**
* Uso de **Stored Procedures en MySQL**

---

#  Módulos del sistema

| Módulo     | Función                        |
| ---------- | ------------------------------ |
| Inventario | Control de productos e insumos |
| Menú       | Gestión de platos y precios    |
| Empleados  | Gestión de personal            |
| Sedes      | Gestión de sucursales          |

---

#  Tecnologías utilizadas

* **Python 3**
* **Tkinter**
* **MySQL**
* **mysql-connector-python**
* **Pandas**
* **ReportLab**
* **Pillow**
* **Tkcalendar**

---

#  Estructura del proyecto

```id="p4kk1p"
Sistema-Gastronomico-Monolito/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
│
├── assets/
│   ├── icons/
│   ├── empleados/
│   ├── menu/
│   └── inventario/

    
```

---

# ⚙️ Instalación

### 1️⃣ Clonar el repositorio

```bash id="2gtqt2"
git clone https://github.com/usuario/sistema-gastronomico-monolito.git
cd sistema-gastronomico-monolito
```

---

### 2️⃣ Instalar dependencias

```bash id="4fhoab"
pip install pillow
pip install mysql-connector-python
pip install pandas
pip install reportlab
pip install tkcalendar
```

---

### 3️⃣ Crear base de datos

```sql id="szk3op"
CREATE DATABASE sistema_gastronomico;
```

Luego importar el script SQL del proyecto.

---

### 4️⃣ Configurar conexión a la base de datos

Modificar en el código:

```python id="76xg16"
self.db = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "sistema_gastronomico"
}
```

---

# ▶️ Ejecutar la aplicación

```bash id="q6rzk2"
python main.py
```

---

# 📊 Funcionalidades

## Dashboard

Muestra estadísticas de:

* Productos
* Platillos
* Empleados

---

## Inventario

Permite:

* Registrar productos
* Controlar stock
* Gestionar costos

---

## Menú

Permite:

* Registrar platos
* Asignar categoría
* Subir imagen del plato

---

## Empleados

Permite:

* Registrar empleados
* Guardar teléfono
* Fecha de contratación
* Foto del empleado

---

## Sedes

Permite:

* Registrar sedes
* Dirección
* Capacidad
* Teléfono

---

# 📤 Exportación de datos

El sistema permite exportar información a:

* **Excel (.xlsx)**
* **PDF (.pdf)**

Los reportes respetan el **filtro de búsqueda aplicado**.

---

# 🛡️ Validaciones implementadas

El sistema valida:

* Campos obligatorios
* Campos numéricos
* Campos de texto
* Formato de email

---

#  Autor: 
MIGUEL TORRES

Proyecto desarrollado como parte de un **Sistema Monolítico de Gestión Gastronómica en Python**.

---

#  Licencia

Uso educativo.
