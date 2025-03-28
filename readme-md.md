# Sistema de Gestión de Descripciones de Puesto de Trabajo (DPTs)

Este sistema permite la creación, modificación, análisis y supervisión de Descripciones de Puesto de Trabajo (DPTs) en 10 formatos diferentes, con asistencia de inteligencia artificial para la redacción y normalización.

## Características principales

- Interfaz web intuitiva para gestionar DPTs
- Soporte para 10 formatos diferentes de DPT
- Asistencia de IA (Gemini 2.0 Flash) para redacción y mejoras
- Análisis automático de DPTs existentes
- Conversión entre diferentes formatos
- Almacenamiento en repositorio Git (GitHub)
- Generación de informes y estadísticas
- Búsqueda avanzada de DPTs

## Requisitos previos

- Docker y Docker Compose
- Cuenta de Google AI (para API de Gemini)
- Cuenta de GitHub (para almacenamiento en repositorio)

## Estructura del proyecto

```
dpt-manager/
├── app.py                # Aplicación principal Flask
├── init_formats.py       # Script para inicializar formatos
├── templates/            # Plantillas HTML
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── uploads/              # Carpeta para archivos subidos
├── reports/              # Carpeta para informes generados
├── Dockerfile            # Configuración para Docker
├── docker-compose.yml    # Configuración de Docker Compose
└── requirements.txt      # Dependencias de Python
```

## Configuración

1. **Variables de entorno**

   Crea un archivo `.env` en la raíz del proyecto con la siguiente información:

   ```
   GEMINI_API_KEY=your_gemini_api_key
   GITHUB_TOKEN=your_github_token
   GITHUB_REPO=username/repository
   ```

2. **Configuración de base de datos**

   El sistema usa PostgreSQL por defecto. La configuración está en el archivo `docker-compose.yml`.

## Instalación y ejecución

### Usando Docker (recomendado)

1. Construye y ejecuta los contenedores:

   ```bash
   docker-compose up -d
   ```

2. Inicializa los formatos de DPT (solo primera vez):

   ```bash
   docker-compose exec dpt-manager-app python init_formats.py
   ```

3. Accede a la aplicación en tu navegador:

   ```
   http://localhost:5000
   ```

4. Para acceder a pgAdmin (gestión de base de datos):

   ```
   http://localhost:5050
   ```
   
   Usuario: admin@example.com
   Contraseña: admin

### Ejecución local (desarrollo)

1. Crea un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configura la base de datos:

   ```bash
   export DATABASE_URL="sqlite:///dpt_manager.db"  # En Windows: set DATABASE_URL=sqlite:///dpt_manager.db
   ```

4. Inicializa los formatos:

   ```bash
   python init_formats.py
   ```

5. Ejecuta la aplicación:

   ```bash
   python app.py
   ```

6. Accede a la aplicación en tu navegador:

   ```
   http://localhost:5000
   ```

## Uso del sistema

### Crear un DPT

1. Haz clic en "Crear DPT" en la página principal
2. Selecciona uno de los 10 formatos disponibles
3. Completa todos los campos requeridos en el formulario
4. Utiliza el asistente de IA para recibir sugerencias de redacción
5. Guarda el DPT o guárdalo como borrador

### Modificar un DPT

1. Selecciona "Modificar DPT" en la página principal
2. Busca el DPT que deseas modificar
3. Realiza los cambios necesarios
4. Guarda la nueva versión (se mantendrá un historial de versiones)

### Analizar un DPT

1. Selecciona "Analizar DPT" en la página principal
2. Sube un archivo o pega el texto del DPT
3. Selecciona las opciones de análisis (identificar formato, extraer componentes, etc.)
4. Revisa los resultados del análisis y las sugerencias de mejora

### Supervisar DPTs

1. Accede a "Supervisar DPTs" para ver el dashboard
2. Consulta estadísticas, métricas y tendencias
3. Genera informes personalizados
4. Exporta datos para su uso en otras herramientas

## Integración con IA (Gemini 2.0 Flash)

El sistema utiliza la API de Google Gemini 2.0 Flash para:

1. **Asistencia en redacción**: Sugerencias inteligentes mientras se escribe
2. **Análisis de calidad**: Evaluación de claridad, completitud y efectividad
3. **Detección de formato**: Identificación automática del formato de un DPT existente
4. **Normalización**: Conversión entre diferentes formatos
5. **Extracción de componentes**: Identificación automática de las partes de un DPT

## Integración con GitHub

El sistema guarda automáticamente los DPTs en un repositorio GitHub:

1. Cada DPT se almacena como un archivo Markdown
2. Se mantiene un historial de cambios con control de versiones
3. Facilita la colaboración y revisión por parte de diferentes miembros del equipo

## Formatos de DPT soportados

1. **Formato 1: Estándar Básico**
   - Formato sencillo con campos esenciales para cualquier puesto

2. **Formato 2: Detallado por Competencias**
   - Enfatiza competencias y habilidades específicas requeridas

3. **Formato 3: Por Objetivos**
   - Centrado en objetivos y metas específicas del puesto

4. **Formato 4: Enfoque en Resultados**
   - Orientado a los resultados esperados y el impacto del puesto

5. **Formato 5: Detalle Técnico**
   - Especializado para roles técnicos y tecnológicos

6. **Formato 6: Ejecutivo**
   - Diseñado para roles de liderazgo y dirección

7. **Formato 7: Funcional Avanzado**
   - Descripción detallada con actividades y porcentajes de tiempo

8. **Formato 8: Académico/Investigación**
   - Adaptado para roles en entornos académicos o de investigación

9. **Formato 9: Sector Público**
   - Cumple con requisitos específicos de administraciones públicas

10. **Formato 10: Internacional/Multinacional**
    - Bilingüe y adaptado para roles en entornos internacionales

## Personalización de formatos

El sistema permite personalizar los formatos existentes o crear nuevos:

1. Modifica la estructura de campos en la base de datos
2. Actualiza los formularios correspondientes en la interfaz
3. El sistema se adaptará automáticamente a los cambios

## Solución de problemas

### Problemas de conexión con la API de Gemini

- Verifica que tu clave API sea válida
- Asegúrate de tener suficiente cuota disponible
- Verifica conectividad a Internet

### Problemas con la integración de GitHub

- Confirma que el token tenga los permisos adecuados
- Verifica que el repositorio exista y sea accesible
- Asegúrate de que el formato del nombre de repositorio sea correcto (usuario/repo)

### Problemas con la base de datos

- Verifica las credenciales de conexión
- Asegúrate de que el servicio PostgreSQL esté en ejecución
- Comprueba los logs en Docker para identificar errores específicos

## Contribución al proyecto

1. Haz un fork del repositorio
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Contacto y soporte

Para preguntas, soporte o sugerencias, por favor [abrir un issue](https://github.com/yourusername/dpt-manager/issues) en el repositorio.