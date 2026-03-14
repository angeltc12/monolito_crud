#  Sistema Gastronómico PRO (Arquitectura Monolítica)

Sistema de gestión gastronómica desarrollado en **Python**, utilizando **Tkinter** para la interfaz gráfica y **MySQL** como base de datos.

El sistema sigue una **arquitectura monolítica**, donde toda la lógica de negocio, la interfaz gráfica y el acceso a datos se encuentran integrados en una sola aplicación.

---

#  Requisitos técnicos del proyecto

Este proyecto cumple con los siguientes requisitos académicos:

* **Estructura modular:** el sistema contiene **4 módulos funcionales principales**.
* **Base de datos:** utiliza la misma base de datos desarrollada en el módulo **Profundización y Aplicaciones en Bases de Datos**.
* **Integración completa:** el sistema demuestra la **conexión funcional entre interfaz gráfica, lógica del sistema y base de datos MySQL**.

---

#  Arquitectura del sistema

El sistema utiliza una **arquitectura monolítica**, lo que significa que:

* La **interfaz gráfica**
* La **lógica del sistema**
* El **acceso a la base de datos**

se encuentran dentro de **una misma aplicación y un mismo código fuente**.

### Ventajas del enfoque monolítico

* Implementación sencilla
* Fácil despliegue
* Ideal para proyectos académicos
* Menor complejidad de infraestructura

### Desventajas

* Escalabilidad limitada
* Alto acoplamiento entre componentes

---

#  Módulos del sistema

El sistema está dividido en **4 módulos principales**:

| Módulo     | Función                        |
| ---------- | ------------------------------ |
| Inventario | Gestión de productos e insumos |
| Menú       | Gestión de platos y precios    |
| Empleados  | Administración del personal    |
| Sedes      | Gestión de sucursales          |

Cada módulo permite realizar operaciones **CRUD (Crear, Leer, Actualizar y Eliminar)**.

---

# ️ Funcionalidades principales

El sistema incluye las siguientes características:

* CRUD completo en todos los módulos
* Dashboard con estadísticas
* Búsqueda y filtrado de registros
* Exportación de datos a **Excel**
* Exportación de datos a **PDF**
* Validación de campos numéricos
* Validación de texto
* Validación de email
* Carga de imágenes con **Pillow**
* Uso de calendario para selección de fechas
* Confirmación de acciones importantes
* Uso de **Stored Procedures en MySQL**

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

```
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

# ️ Instalación del proyecto

## 1️ Clonar el repositorio

```
git clone https://github.com/angeltc12/monolito_crud.git
cd monolito_crud
```

---

## 2️ Instalar dependencias

```
pip install -r requirements.txt
```

---

## 3️ Crear base de datos

El sistema utiliza **MySQL**.

Crear la base de datos ejecutando:

```
CREATE DATABASE sistema_gastronomico;
```

Luego importar el **script SQL del proyecto** que contiene las tablas:

* inventario
* menu
* empleados
* sedes

---

## 4️ Configurar conexión a la base de datos

El sistema utiliza **variables de entorno** mediante un archivo `.env`.

Crear el archivo `.env` en la raíz del proyecto.

Contenido del archivo:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=sistema_gastronomico
```

### Explicación

| Variable    | Descripción                  |
| ----------- | ---------------------------- |
| DB_HOST     | Dirección del servidor MySQL |
| DB_USER     | Usuario de MySQL             |
| DB_PASSWORD | Contraseña del usuario       |
| DB_NAME     | Nombre de la base de datos   |

---

# ▶ Ejecutar la aplicación

Ejecutar el sistema con:

```
python main.py
```

Si la configuración es correcta, se abrirá la **interfaz gráfica del Sistema Gastronómico PRO**.

---

#  Funcionalidades del sistema

## Dashboard

Muestra estadísticas generales del sistema como:

* cantidad de productos
* cantidad de platillos
* número de empleados

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
* Asignar categorías
* Subir imágenes del plato

---

## Empleados

Permite:

* Registrar empleados
* Guardar teléfono
* Fecha de contratación
* Fotografía del empleado

---

## Sedes

Permite:

* Registrar sedes
* Dirección
* Capacidad
* Teléfono

---

#  Exportación de datos

El sistema permite exportar información a:

* **Excel (.xlsx)**
* **PDF (.pdf)**

Los reportes respetan el **filtro de búsqueda aplicado en la interfaz**.

---

# ️ Validaciones implementadas

El sistema valida:

* Campos obligatorios
* Campos numéricos
* Campos de texto
* Formato de email
* Formato de imágenes

-----

#  Autor

**Miguel Torres**

Proyecto desarrollado como parte de un **Sistema Monolítico de Gestión Gastronómica en Python**.

---

#  Licencia

Proyecto desarrollado con fines **educativos**.
