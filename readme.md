# DEVOPS Test
---

### Requrimientos

- `Docker`
- `Docker-compose v3.8`
- `Make`

---

### Instalación de Make en Linux

#### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install make
```
---
### Descripción de los Stacks
---
-  #### Descripción del Stack 1: API y MongoDB

    Este stack ofrece una API con MongoDB para registro, inicio de sesión y gestión de mensajes con `JWT`. Todas las rutas están documentadas y accesibles en 
    `Swagger`: `http://[API_URL]/apidocs`.

    Ademas cada una de las rutas realiza interaccion con `Graylog` [STACK2] enviando logs sobre el comportamiento de la api y las interacciones de usuarios

-  #### Descripción del Stack 2: Configuración de Graylog
    Este stack consiste en una configuracion basica de graylog utilizando MongoDB y Opensearch para su funcionamiento.

    El objetivo de este stack es obtener informacion sobre el funcionamiento y las interacciones de los ususarios en la api.

    Los stacks se comunican utilizando el formato de registro GELF para una optima comunicacion con graylog, y atravez del protocolo UDP en el puerto 12201. 
    La interfaz de usuario se encuentra en el puerto 9000.

-  #### Descripción del Stack 3: Configuración de Proxy con nginx
    Esta configuración de `Nginx` constituye un stack básico para gestionar el tráfico en un entorno de Docker Swarm. Utiliza la directiva `upstream` para dirigir el tráfico a los servidores virtuales que escuchan en los puertos 80 y 9000. Luego, mediante `proxy_pass`, redirige el tráfico a los servicios correspondientes, como `Graylog` y `API`.

    Además, se emplea la propiedad `least_conn`, la cual distribuye las solicitudes entrantes entre varios servidores backend de manera específica. Concretamente, Nginx enruta las solicitudes entrantes al servidor backend que tenga la menor cantidad de conexiones activas en ese momento. Esto optimiza el balanceo de carga y mejora la eficiencia del sistema al distribuir equitativamente la `carga` entre los servidores disponibles.

---
## Pasos para el despliegue de los stacks en un cluster de docker swarm

### Pasos

1. #### Clone the repository:
    ```
    git clone https://github.com/alvarovega99/test-devops.git
    ```

2. #### Navigate to the project directory:
    ```
    cd test-devops
    ```

3. #### (`Opcional`) Crear una nueva imagen de la api:
    #### Se deben modificar las siguientes variables en del archivo `makefile`

    - `DOCKER_HUB_USERNAME` (Usuario de dockerhub)
    - `DOCKER_HUB_PASSWORD` (Password de dockerhub)

    #### Ejecutar el comando para realizar el build de la imagen y subirla a su cuenta de `dockerhub`
  
    ```
    make build-and-push
    ```

    #### Luego se debe modificar la imagen en el `docker-compose` del stack
    - `./stack-1/api/docker-compose.yml`



4. #### Desplegar `Stack 1` (API y MongoDB):
    ```
    make create-stack-1
    ```

5. #### Desplegar `Stack 2` (Graylog):
    ```
    make create-stack-2
    ```

6. #### Una vez funcionando el `Stack 2` se debe ejecutar el siguiente comando:
    ```
    make init-graylog
    ```
    `Este se encarga de crear el input necesario para que graylog sea capaz de obtener los logs de la api`

7. #### Desplegar `Stack 3` (Nginx):
    ```
    make create-stack-3
    ```
---
#### Para su optimo funcionamiendo se necesitan habilitar los siguientes puertos en el cluster:

- `9000` (Interfaz de graylog)
- `80` (Puerto de ejecucion de la api y Swagger)
