# INFILE News API

API para la gestión de noticias, usuarios y categorías, desarrollada con
**FastAPI** y **SQLAlchemy**.

## Características

-   Autenticación JWT
-   Gestión de usuarios, roles y confirmación por correo
-   CRUD de noticias y categorías
-   Subida de imágenes
-   PostgreSQL como base de datos
-   pgAdmin para administración visual de la base de datos
-   Docker para despliegue sencillo

## Requisitos

-   Docker y Docker Compose instalados
-   Python 3.13 (solo necesario si corres el proyecto fuera de Docker)

## Configuración del archivo `.env`

Antes de ejecutar el proyecto, debes crear el archivo `.env` con tus
variables de entorno.\
Se incluye un archivo de ejemplo llamado [`envexample`](envexample).

1.  Copia el archivo de ejemplo y renómbralo como `.env`:

    ``` sh
    cp envexample .env
    ```

2.  Edita el archivo `.env` y reemplaza los valores según tu entorno.
    Por ejemplo:

    ``` env
    # App
    APP_NAME=INFILE News API
    ENV=dev

    # Configuración de archivos estáticos
    STATIC_DIR=static

    # Security
    SECRET_KEY=tu_clave_secreta
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    EMAIL_TOKEN_EXPIRE_MINUTES=60
    RESET_TOKEN_EXPIRE_MINUTES=30
    ALGORITHM=HS256

    # Database (importante: en Docker el host es `db`)
    DATABASE_URL=postgresql+psycopg2://postgres:admin@db:5432/infile_news

    # SMTP
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USER=tu_correo@gmail.com
    SMTP_PASSWORD=tu_contraseña_app
    SMTP_TLS=true
    EMAILS_FROM=tu_correo@gmail.com

    # Frontend base URL para links de confirmación
    FRONTEND_BASE_URL=http://localhost:8001
    ```

### Generar la `SECRET_KEY`

La `SECRET_KEY` se utiliza para firmar y validar los tokens JWT.\
Debe ser un valor aleatorio y seguro.

Genera una clave de **64 caracteres hexadecimales (256 bits)** con:

``` sh
python -c "import secrets; print(secrets.token_hex(32))"
```

Ejemplo de resultado:

    d9f2b4f10e2f4dfb8a65c5b7a4b8c6f26e4af14208b03e43e682baed9f76f4d2

> **Nota:** Nunca compartas tu `SECRET_KEY` ni la subas al repositorio.

## Ejecución con Docker

1.  **Construye y levanta los contenedores**

    ``` sh
    docker-compose up -d --build
    ```

2.  **Accede a la aplicación**

    <http://localhost:8000>

3.  **Accede a pgAdmin** en: [http://localhost:5050](http://localhost:5050)

    - **Usuario:** `admin@admin.com`
    - **Contraseña:** `admin`

    > Estos datos están definidos en el archivo `docker-compose.yml`.

4.  **Configura un nuevo servidor de base de datos en pgAdmin en pgAdmin**

    -   **Host name/address**: db
    -   **Port**: 5432
    -   **Maintenance database**: postgres
    -   **Username**: POSTGRES_USER (por defecto: postgres)
    -   **Password**: POSTGRES_PASSWORD (por defecto: admin)

## Uso de la API

-   Documentación interactiva: <http://localhost:8000/docs>
-   Cliente HTTP recomendado: Postman, Insomnia o directamente Swagger
    UI

## Notas

-   Antes de correr el proyecto asegúrate de que Docker y Docker Compose
    están activos.

-   Para detener los contenedores:

    ``` sh
    docker-compose down
    ```

-   Los datos de la base de datos se guardan en un volumen de Docker
    para persistencia.
