# Guía de Uso del Sistema de Gestión de DPTs

Esta guía explica paso a paso cómo utilizar todas las funcionalidades del Sistema de Gestión de Descripciones de Puesto de Trabajo (DPTs).

## Índice
1. [Acceso al sistema](#1-acceso-al-sistema)
2. [Crear un nuevo DPT](#2-crear-un-nuevo-dpt)
3. [Modificar un DPT existente](#3-modificar-un-dpt-existente)
4. [Analizar un DPT externo](#4-analizar-un-dpt-externo)
5. [Supervisar y generar informes](#5-supervisar-y-generar-informes)
6. [Uso del asistente de IA](#6-uso-del-asistente-de-ia)
7. [Conversión entre formatos](#7-conversión-entre-formatos)
8. [Administración del repositorio](#8-administración-del-repositorio)

## 1. Acceso al sistema

1. Abre tu navegador web y accede a la aplicación:
   ```
   http://localhost:5000
   ```

2. Verás la pantalla principal con cuatro opciones principales:
   - Crear DPT
   - Modificar DPT
   - Analizar DPT
   - Supervisar DPTs

## 2. Crear un nuevo DPT

### Selección de formato

1. Desde la pantalla principal, haz clic en "Crear DPT" o en el botón "Comenzar".
2. Se mostrarán los 10 formatos disponibles. Selecciona el que mejor se adapte a tus necesidades:
   - **Formato 1: Estándar Básico** - Para roles generales con información esencial
   - **Formato 2: Detallado por Competencias** - Enfocado en habilidades y competencias
   - **Formato 3: Por Objetivos** - Centrado en metas y resultados esperados
   - Y así sucesivamente...

3. Haz clic en el formato deseado para seleccionarlo. El formato se resaltará y mostrará el formulario específico.

### Completar el formulario

1. Completa todos los campos requeridos (marcados con *):
   - Título del puesto
   - Departamento
   - Resumen/Propósito
   - Responsabilidades
   - Requisitos/Cualificaciones
   - Etc. (dependiendo del formato seleccionado)

2. Para obtener ayuda con la redacción, puedes:
   - Hacer clic en el botón "Asistente IA" junto a cada campo
   - Utilizar el panel de Asistente de Redacción IA en la parte inferior

### Uso del asistente de IA durante la creación

1. En el panel de "Asistente de Redacción IA", selecciona una de las opciones predefinidas:
   - Mejorar resumen del puesto
   - Redactar responsabilidades
   - Sugerir requisitos
   - Verificar coherencia

2. O bien, escribe tu pregunta específica en el campo de texto y haz clic en el botón de enviar.

3. La IA generará sugerencias que puedes copiar directamente en los campos del formulario.

### Guardar el DPT

1. Una vez completado el formulario, tienes tres opciones:
   - **Vista Previa**: Para revisar cómo se verá el DPT antes de guardarlo
   - **Guardar Borrador**: Para guardar una versión no finalizada
   - **Guardar DPT**: Para guardar la versión final

2. Al guardar, el sistema:
   - Evalúa automáticamente la calidad del DPT
   - Guarda el DPT en la base de datos
   - Crea una versión en el repositorio de GitHub
   - Muestra un mensaje de confirmación

## 3. Modificar un DPT existente

### Buscar un DPT

1. Desde la pantalla principal, selecciona "Modificar DPT".
2. Utiliza el campo de búsqueda para encontrar el DPT por:
   - Título
   - Departamento
   - ID

3. Los resultados se mostrarán en una tabla con información básica.

### Editar un DPT

1. En la lista de resultados, haz clic en el icono de edición (lápiz) junto al DPT que deseas modificar.
2. Se cargará el formulario con todos los datos actuales del DPT.
3. Realiza los cambios necesarios en cualquier campo.
4. Opcionalmente, añade notas sobre los cambios en el campo "Notas de cambio".

### Ver historial de versiones

1. En la lista de DPTs, haz clic en el icono de historial (reloj) para ver las versiones anteriores.
2. Se mostrará una lista de todas las versiones con:
   - Número de versión
   - Fecha de modificación
   - Usuario que realizó los cambios
   - Notas de cambio

3. Puedes comparar versiones o restaurar una versión anterior si es necesario.

## 4. Analizar un DPT externo

### Subir un DPT para análisis

1. Desde la pantalla principal, selecciona "Analizar DPT".
2. Tienes dos opciones:
   - **Subir archivo**: Soporta formatos DOC, DOCX, PDF, TXT y RTF
   - **Pegar texto**: Copia y pega el contenido de un DPT directamente

### Configurar análisis

1. Selecciona las opciones de análisis deseadas:
   - **Identificar formato**: Detecta automáticamente el formato del DPT
   - **Extraer componentes**: Identifica y estructura las partes del DPT
   - **Comprobar calidad**: Evalúa la calidad y completitud
   - **Sugerir mejoras**: Proporciona recomendaciones para optimizar el DPT

2. Haz clic en "Analizar DPT" para iniciar el proceso.

### Interpretar resultados

El sistema mostrará un informe completo con:

1. **Formato identificado**:
   - Nombre del formato detectado
   - Nivel de confianza de la detección

2. **Componentes extraídos**:
   - Título del puesto
   - Departamento
   - Responsabilidades
   - Requisitos
   - Etc.

3. **Evaluación de calidad**:
   - Puntuación general (0-100)
   - Desglose por criterios:
     - Claridad
     - Completitud
     - Alineación estratégica
     - Medibilidad

4. **Sugerencias de mejora**:
   - Recomendaciones específicas por campo
   - Ejemplos de redacción mejorada

### Acciones posteriores

Con los resultados del análisis, puedes:

1. **Exportar análisis**: Guardar el informe en formato PDF o Markdown
2. **Convertir a otro formato**: Transformar el DPT al formato deseado
3. **Editar con sugerencias**: Crear un nuevo DPT implementando las mejoras sugeridas

## 5. Supervisar y generar informes

### Dashboard principal

1. Desde la pantalla principal, selecciona "Supervisar DPTs".
2. Se mostrará un panel con estadísticas y métricas clave:
   - Total de DPTs
   - DPTs actualizados recientemente
   - DPTs pendientes de revisión
   - Calidad promedio

### Visualización de datos

El dashboard incluye gráficos interactivos:

1. **Distribución por formato**:
   - Gráfico circular que muestra el porcentaje de DPTs por formato

2. **Actividad reciente**:
   - Gráfico de líneas mostrando la creación y actualización de DPTs en el tiempo

3. **Distribución por departamento**:
   - Gráfico de barras con el número de DPTs por departamento

### Generación de informes

1. En la sección "Exportar Informes", encontrarás diferentes tipos de informes:
   - **Reporte Completo**: Todos los DPTs con detalles completos y métricas
   - **Resumen Ejecutivo**: Versión resumida para directivos
   - **Análisis de Brechas**: Identifica áreas de mejora en los DPTs

2. Para generar un informe:
   - Selecciona el tipo de informe deseado
   - Configura los filtros (opcional): por departamento, formato, fecha, etc.
   - Haz clic en "Exportar" y selecciona el formato deseado (PDF, Word, Excel, HTML)

3. Los informes se pueden:
   - Descargar inmediatamente
   - Enviar por correo electrónico
   - Programar para generación periódica (semanal, mensual)

## 6. Uso del asistente de IA

El sistema integra asistencia de IA (Gemini 2.0 Flash) que puede utilizarse en diferentes contextos:

### Asistencia en tiempo real

1. Durante la creación o edición de un DPT, el botón "Asistente IA" junto a cada campo proporciona:
   - Sugerencias de redacción específicas para ese campo
   - Ejemplos basados en mejores prácticas
   - Correcciones de estilo y gramática

2. Las sugerencias se adaptan al contexto del puesto y departamento.

### Consultas específicas

El panel de "Asistente de Redacción IA" permite hacer preguntas abiertas:

1. **Ejemplos de consultas efectivas**:
   - "¿Cómo redactar requisitos para un puesto de marketing digital?"
   - "¿Qué responsabilidades debe tener un gerente de operaciones?"
   - "¿Cuáles son las tendencias actuales en descripciones de puestos de ingeniería?"

2. La IA generará respuestas detalladas que pueden usarse como punto de partida.

### Verificación de calidad

Antes de guardar un DPT, el asistente puede verificar:

1. **Completitud**: ¿Se han completado todos los campos importantes?
2. **Claridad**: ¿La redacción es clara y comprensible?
3. **Especificidad**: ¿Las responsabilidades son específicas y medibles?
4. **Coherencia**: ¿Hay alineación entre las diferentes secciones?

## 7. Conversión entre formatos

### Convertir un DPT existente

1. En la sección de "Modificar DPT", selecciona un DPT existente.
2. Haz clic en el botón "Convertir formato" en la barra de acciones.
3. Selecciona el formato destino deseado entre los 10 disponibles.
4. El sistema realizará la conversión automáticamente, preservando toda la información importante.

### Previsualización de la conversión

1. Antes de confirmar la conversión, puedes ver una comparación lado a lado:
   - Formato original
   - Formato convertido

2. Puedes realizar ajustes manuales si es necesario antes de guardar.

### Conversión por lotes

Para convertir múltiples DPTs al mismo tiempo:

1. En la sección "Supervisar DPTs", selecciona varios DPTs mediante las casillas de verificación.
2. Haz clic en "Acciones por lotes" y selecciona "Convertir formato".
3. Elige el formato destino y confirma la acción.
4. El sistema procesará todos los DPTs seleccionados y mostrará un informe del resultado.

## 8. Administración del repositorio

### Visualización del repositorio

1. En el menú principal, selecciona "Repositorio" para ver todos los DPTs almacenados.
2. La vista del repositorio muestra:
   - Estructura de carpetas organizadas por departamento
   - Lista de archivos con información de versiones
   - Histórico de cambios

### Sincronización con GitHub

El sistema se sincroniza automáticamente con GitHub, pero también puedes:

1. **Sincronización manual**: Forzar una sincronización inmediata con el botón "Sincronizar ahora"
2. **Resolución de conflictos**: Manejar conflictos si un archivo fue modificado en ambos sistemas
3. **Control de acceso**: Configurar permisos de acceso al repositorio desde la interfaz

### Gestión de versiones

Para cada DPT en el repositorio, puedes:

1. **Ver diferencias**: Comparar cualquier versión con la anterior o con la actual
2. **Restaurar versión**: Volver a una versión anterior específica
3. **Añadir etiquetas**: Marcar versiones importantes (ej. "Aprobado", "En revisión")
4. **Añadir comentarios**: Documentar cambios o decisiones importantes

## Casos de uso prácticos

### Caso 1: Creación de un nuevo puesto

1. El departamento de RRHH necesita crear la descripción para un nuevo puesto de "Especialista en IA".
2. Pasos:
   - Seleccionar "Crear DPT"
   - Elegir "Formato 5: Detalle Técnico" (ideal para roles tecnológicos)
   - Completar los campos básicos (título, departamento)
   - Utilizar el asistente de IA para sugerir responsabilidades y requisitos específicos
   - Revisar y ajustar el contenido
   - Guardar y compartir con los interesados

### Caso 2: Actualización masiva por cambio organizacional

1. La empresa ha reorganizado su estructura y necesita actualizar 20 DPTs.
2. Pasos:
   - Ir a "Supervisar DPTs"
   - Filtrar por departamentos afectados
   - Seleccionar todos los DPTs relevantes
   - Usar "Edición por lotes" para actualizar la estructura organizativa
   - Revisar individualmente los casos que requieran cambios específicos
   - Generar un informe de los cambios realizados

### Caso 3: Estandarización de formatos

1. La empresa desea estandarizar todos los DPTs al "Formato 3: Por Objetivos".
2. Pasos:
   - Ir a "Supervisar DPTs"
   - Seleccionar los DPTs que necesitan conversión
   - Usar la función "Convertir formato" por lotes
   - Revisar y aprobar cada conversión
   - Generar un informe de estandarización

## Solución de problemas comunes

### Problema: Error al subir archivo para análisis

**Solución:**
1. Verifica que el formato del archivo esté soportado (DOC, DOCX, PDF, TXT, RTF)
2. Comprueba que el archivo no esté dañado o protegido con contraseña
3. Intenta convertir a PDF o texto plano antes de subir
4. Si el archivo es muy grande (>10MB), intenta dividirlo o reducir su tamaño

### Problema: Baja calidad en las sugerencias de IA

**Solución:**
1. Proporciona más contexto en tu consulta
2. Especifica el sector o industria del puesto
3. Incluye ejemplos de lo que esperas recibir
4. Verifica que la API key de Gemini esté configurada correctamente

### Problema: Error en sincronización con GitHub

**Solución:**
1. Verifica que el token de GitHub sea válido y tenga los permisos necesarios
2. Comprueba que el nombre del repositorio esté correctamente formateado (usuario/repo)
3. Intenta sincronizar manualmente desde la sección de administración
4. Revisa los logs de errores para identificar problemas específicos

## Consejos para aprovechar al máximo el sistema

1. **Estandarizar nomenclatura**: Utiliza títulos de puesto consistentes para facilitar búsquedas y análisis
2. **Crear plantillas personalizadas**: Para departamentos específicos o tipos de roles recurrentes
3. **Programar revisiones periódicas**: Establece un calendario de revisión de DPTs (trimestral o semestral)
4. **Utilizar etiquetas y categorías**: Para organizar y filtrar DPTs fácilmente
5. **Aprovechar los datos analíticos**: Utiliza las métricas del dashboard para mejorar continuamente la calidad

## Recursos adicionales

- [Manual técnico completo](https://example.com/manual) (enlace ficticio)
- [Video tutoriales](https://example.com/tutorials) (enlace ficticio)
- [Foro de soporte](https://example.com/support) (enlace ficticio)
- [Mejores prácticas en redacción de DPTs](https://example.com/best-practices) (enlace ficticio)