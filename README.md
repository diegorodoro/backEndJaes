

# 🛠️ Backend - Generador de Etiquetas de Productos (Masivo)

Este proyecto es el backend del sistema que permite generar etiquetas masivas en PDF a partir de información de productos. Está construido con **Python y Django** y utiliza **PostgreSQL** como base de datos.

---

## 🚀 Instrucciones para configurar el entorno de desarrollo

### 1. Clonar el repositorio

```bash
git clone https://github.com/diegorodoro/backEndJaes.git
cd backEndJaes
```

---

### 2. Crear y activar el entorno virtual (venv)

#### En Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### En macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Instalar dependencias del proyecto

```bash
pip install -r requirements.txt
```

---

### 4. Crear la base de datos en PostgreSQL

Debes asegurarte de tener instalado **PostgreSQL**. Luego, puedes crear la base de datos de cualquiera de las siguientes formas:

#### Opción A: Usando **pgAdmin**

1. Abre pgAdmin.
2. Conéctate al servidor `localhost`.
3. Haz clic derecho en "Databases" → "Create" → "Database".
4. Nombra la base de datos `Jaes`.
5. Asegúrate de que el usuario sea `postgres`.

#### Opción B: Usando comandos en consola de PostgreSQL:

```sql
CREATE DATABASE Jaes;
```

---

### 5. Crear el archivo `.env`

En la raíz del proyecto, crea un archivo llamado `.env` con el siguiente contenido (ajústalo si cambias los datos):

```env
DB_NAME=Jaes
DB_USER=postgres
DB_PASSWORD=Rodoro$%diego102&
DB_HOST=localhost
DB_PORT=5432
```

---

### 6. Aplicar migraciones

Una vez creada la base de datos y configuradas las variables de entorno, ejecuta:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 7. Correr el servidor

```bash
python manage.py runserver
```

El servidor estará disponible por defecto en:

```
http://127.0.0.1:8000/
```
