# Sistema Gastronómico PRO (Arquitectura Monolítica)

Sistema de gestión gastronómica desarrollado en Python utilizando Tkinter para la interfaz gráfica y MySQL como base de datos.

El sistema sigue una arquitectura monolítica, donde la interfaz gráfica, la lógica del sistema y el acceso a datos se encuentran integrados dentro de una sola aplicación.

---

# Descripción del proyecto

Este proyecto consiste en el desarrollo de un sistema de gestión para un restaurante o negocio gastronómico.  
El objetivo principal es centralizar la administración de información relacionada con inventario, menú, empleados y sedes dentro de una sola aplicación de escritorio.

El sistema permite realizar operaciones de registro, consulta, actualización y eliminación de datos (CRUD), además de generar reportes en formato Excel y PDF.

---

# Requisitos académicos del proyecto

Este proyecto cumple con los siguientes requisitos académicos:

- Implementación de una arquitectura monolítica
- Uso de Python como lenguaje principal
- Conexión con MySQL como base de datos
- Integración de interfaz gráfica con Tkinter
- Uso de procedimientos almacenados (Stored Procedures)
- Desarrollo de múltiples módulos funcionales
- Implementación de validaciones de datos

---

# Arquitectura del sistema

El sistema utiliza una arquitectura monolítica. Esto significa que todos los componentes del sistema se encuentran integrados dentro de una sola aplicación.

Componentes principales:

- Interfaz gráfica (Tkinter)
- Lógica del sistema
- Acceso a datos (MySQL)

### Ventajas del enfoque monolítico

- Implementación sencilla
- Despliegue rápido
- Ideal para proyectos académicos
- Menor complejidad de infraestructura

### Desventajas

- Escalabilidad limitada
- Alto acoplamiento entre componentes

---

# Módulos del sistema

El sistema está dividido en cuatro módulos principales:

| Módulo | Función |
|------|------|
| Inventario | Gestión de productos e insumos |
| Menú | Administración de platos y precios |
| Empleados | Registro y gestión del personal |
| Sedes | Administración de sucursales |

Cada módulo permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar).

---

# Funcionalidades principales

El sistema incluye las siguientes características:

- CRUD completo en todos los módulos
- Dashboard con estadísticas
- Búsqueda y filtrado de registros
- Exportación de datos a Excel
- Exportación de datos a PDF
- Validación de campos numéricos
- Validación de texto
- Validación de formato de email
- Carga de imágenes mediante Pillow
- Selección de fechas mediante calendario
- Confirmación de acciones importantes
- Uso de Stored Procedures en MySQL

---

# Tecnologías utilizadas

- Python 3
- Tkinter
- MySQL
- mysql-connector-python
- Pandas
- ReportLab
- Pillow
- Tkcalendar
- python-dotenv

---

# Estructura del proyecto

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

# Instalación del proyecto

## 1. Clonar el repositorio

```
git clone https://github.com/angeltc12/monolito_crud.git
cd monolito_crud
```

---

## 2. Instalar dependencias

```
pip install -r requirements.txt
```

---

## 3. Crear base de datos

El sistema utiliza MySQL.

Crear la base de datos ejecutando:

```
CREATE DATABASE sistema_gastronomico;
```

Luego importar las tablas necesarias:

- inventario
- menu
- empleados
- sedes

También se deben importar los Stored Procedures utilizados por la aplicación.

---

## 4. Configurar conexión a la base de datos

El sistema utiliza variables de entorno mediante un archivo `.env`.

Crear el archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=sistema_gastronomico
```

### Descripción de variables

| Variable | Descripción |
|------|------|
| DB_HOST | Dirección del servidor MySQL |
| DB_USER | Usuario de la base de datos |
| DB_PASSWORD | Contraseña del usuario |
| DB_NAME | Nombre de la base de datos |

---

# Ejecutar la aplicación

Para iniciar el sistema ejecutar:

```
python main.py
```

Si la configuración es correcta, se abrirá la interfaz del Sistema Gastronómico PRO.

---

# Exportación de datos

El sistema permite exportar información en los siguientes formatos:

- Excel (.xlsx)
- PDF (.pdf)

Los reportes generados respetan el filtro de búsqueda aplicado en la interfaz.

---

# Validaciones implementadas

El sistema valida:

- Campos obligatorios
- Campos numéricos
- Campos de texto
- Formato de correo electrónico
- Formato de imágenes

Estas validaciones ayudan a mantener la integridad de los datos almacenados en la base de datos.

---

# Autor

Miguel Torres

Proyecto desarrollado como parte de la implementación de un sistema monolítico de gestión gastronómica en Python.

---

# Agradecimientos

Agradecimiento especial a ti James por su orientación y apoyo durante el desarrollo del proyecto.

---

# Licencia

Proyecto desarrollado con fines educativos.