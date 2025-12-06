# Proyecto FastAPI + Apache APISIX

Este proyecto implementa una arquitectura de microservicios contenerizada utilizando **FastAPI** para los servicios de backend y **Apache APISIX** como API Gateway. Todo el entorno se orquesta mediante **Docker Compose**.

## 📋 Estructura del Proyecto

*   **`clientes/`**: Microservicio para gestión de clientes (FastAPI + SQLite).
*   **`productos/`**: Microservicio para gestión de productos (FastAPI + SQLite).
*   **`apisix/`**: Configuración del API Gateway.
*   **`dashboard/`**: Configuración del Dashboard de administración web para APISIX.
*   **`docker-compose.yml`**: Definición de la infraestructura completa.

## 🚀 Inicio Rápido

### Prerrequisitos
Asegúrate de tener instalados:
*   [Docker Engine](https://docs.docker.com/engine/install/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Despliegue

1.  **Levantar los servicios**:
    Ejecuta el siguiente comando en la raíz del proyecto. Esto construirá las imágenes de los microservicios e iniciará el gateway, el dashboard y etcd.

    ```bash
    docker compose up --build -d
    ```

2.  **Verificar estado**:
    Asegúrate de que todos los contenedores estén corriendo (`up`):

    ```bash
    docker compose ps
    ```

## ⚙️ Configuración del Gateway (APISIX Dashboard)

Para exponer tus microservicios al mundo exterior de forma unificada, configuraremos APISIX mediante su Dashboard web.

### 1. Acceso al Dashboard
*   **URL**: [http://localhost:9000](http://localhost:9000)
*   **Usuario**: `admin`
*   **Contraseña**: `admin`

### 2. Configurar Upstreams (Servicios Backend)
Los "Upstreams" representan tus microservicios reales dentro de la red de Docker.

#### 👉 Servicio de Productos
1.  En el menú lateral, ve a **Upstream** y haz clic en **Create**.
2.  **Name**: `productos-upstream` (o el nombre que prefieras).
3.  **Nodes**:
    *   **Host**: `productos-service` (Nombre exacto del servicio en `docker-compose.yml`).
    *   **Port**: `80` (Puerto interno del contenedor).
    *   **Weight**: `1`
4.  Haz clic en **Next** (siguientes pasos por defecto) y finalmente en **Submit**.

#### 👉 Servicio de Clientes
1.  En **Upstream**, haz clic en **Create**.
2.  **Name**: `clientes-upstream`.
3.  **Nodes**:
    *   **Host**: `clientes-service`
    *   **Port**: `80`
    *   **Weight**: `1`
4.  Haz clic en **Next** y **Submit**.

### 3. Configurar Routes (Rutas Públicas)
Las "Routes" definen cómo el Gateway recibe peticiones externas y a qué Upstream las envía.

#### 👉 Ruta para Productos
1.  En el menú lateral, ve a **Route** y haz clic en **Create**.
2.  **Name**: `ruta-productos`.
3.  **Path**: `/productos/*` (El `*` es importante para aceptar sub-rutas).
4.  **Upstream**: Selecciona `productos-upstream` en la lista desplegable.
5.  Haz clic en **Next** (validar plugins vacíos por ahora) y **Submit**.

#### 👉 Ruta para Clientes
1.  En **Route**, haz clic en **Create**.
2.  **Name**: `ruta-clientes`.
3.  **Path**: `/clientes/*`.
4.  **Upstream**: Selecciona `clientes-upstream`.
5.  Haz clic en **Next** y **Submit**.

---

## 🧪 Verificación y Uso

Una vez configurado, tu API Gateway está escuchando en el puerto **9080**. Puedes consumir tus servicios a través de él.

### Crear un Producto
**Endpoint**: `POST http://localhost:9080/productos/`

```bash
curl -X POST "http://localhost:9080/productos/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Laptop Gamer", "precio": 1500.00, "descripcion": "Alta gama"}'
```

### Listar Productos
**Endpoint**: `GET http://localhost:9080/productos/`

```bash
curl "http://localhost:9080/productos/"
```

### Crear un Cliente
**Endpoint**: `POST http://localhost:9080/clientes/`

```bash
curl -X POST "http://localhost:9080/clientes/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Juan", "apellido": "Perez", "email": "juan@example.com"}'
```

### Listar Clientes
**Endpoint**: `GET http://localhost:9080/clientes/`

```bash
curl "http://localhost:9080/clientes/"
```

---

## 💾 Persistencia de APISIX

La información de configuración de APISIX se persiste en **etcd**. En este proyecto, los datos se guardan localmente en la carpeta `./etcd-data` (ver `docker-compose.yml`).

### Ver información guardada
Para consultar en consola todo lo que está almacenado actualmente en etcd (rutas, upstreams, etc.), utiliza el siguiente comando:

```bash
docker exec etcd etcdctl --endpoints=http://127.0.0.1:2379 get / --prefix
```

### Eliminar información (Reset)
Si deseas borrar toda la configuración de APISIX y comenzar desde cero:

1.  Baja los contenedores:
    ```bash
    docker compose down
    ```
2.  Borra la carpeta donde se persisten los datos:
    *   Elimina el directorio `./etcd-data` que se encuentra en la raíz del proyecto.
3.  Vuelve a levantar el entorno:
    ```bash
    docker compose up --build -d
    ```

---

## 🛠️ Desarrollo

El proyecto está configurado con volúmenes para desarrollo. El código fuente en tu máquina local (`./productos/app` y `./clientes/app`) está sincronizado con los contenedores.

*   Puedes editar el código en tiempo real.
*   **Nota**: Si añades nuevas dependencias en `requirements.txt`, deberás reconstruir los contenedores:
    ```bash
    docker compose up --build -d
    ```
