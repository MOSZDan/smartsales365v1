# Choreo Deployment Guide - SmartSales365 Backend

Este documento explica cómo desplegar el backend de SmartSales365 en Choreo.

## Archivos de Configuración Creados

### 1. `.choreo/component.yaml`
Este archivo configura el endpoint y las variables de entorno para Choreo:
- **Endpoint**: API REST en el puerto 8000
- **Base Path**: `/api`
- **Visibilidad**: Pública
- **Variables de entorno**: Todas las configuraciones necesarias para Django

### 2. `Dockerfile`
Dockerfile optimizado para producción que incluye:
- Python 3.11 slim
- PostgreSQL client
- Gunicorn como servidor WSGI
- Usuario no-root para seguridad
- Recolección automática de archivos estáticos

### 3. `Procfile` (actualizado)
Configurado para usar Gunicorn en producción:
- 4 workers
- Timeout de 120 segundos
- Migraciones automáticas en release

### 4. `.dockerignore`
Excluye archivos innecesarios del build de Docker para optimizar el tamaño de la imagen.

## Pasos para Desplegar en Choreo

### Paso 1: Preparar el Repositorio

Asegúrate de que todos los cambios estén commiteados y pusheados a tu repositorio Git:

```bash
cd backend
git add .choreo/ Dockerfile .dockerignore Procfile CHOREO_DEPLOYMENT.md
git commit -m "Add Choreo deployment configuration"
git push origin main
```

### Paso 2: Crear un Componente en Choreo

1. Inicia sesión en [Choreo](https://console.choreo.dev/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Click en **"Create"** > **"Service"**
4. Selecciona tu repositorio Git
5. Configura el componente:
   - **Buildpack**: Python
   - **Python Version**: 3.11.x
   - **Project Directory**: `/backend` (o la ruta donde está tu backend)
   - **Port**: 8000

### Paso 3: Configurar Variables de Entorno

Durante el despliegue, configura las siguientes variables de entorno en Choreo:

#### Variables Requeridas:

```bash
# Django Secret Key (genera una nueva para producción)
SECRET_KEY=your-super-secret-key-here

# Database URL (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Allowed Hosts (dominio de Choreo)
ALLOWED_HOSTS=your-app.choreoapis.dev,localhost

# CORS Origins (frontend URL)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Email Configuration (MailerSend)
ANYMAIL_MAILERSEND_API_TOKEN=your-mailersend-api-token
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# JWT Secret Key
JWT_SECRET_KEY=your-jwt-secret-key
```

#### Variables Opcionales:

```bash
# Debug (siempre False en producción)
DEBUG=False

# Database SSL Mode
DATABASE_SSL_MODE=require
```

### Paso 4: Build y Deploy

1. Click en **"Build"** para construir la imagen Docker
2. Espera a que el build termine exitosamente
3. Ve a la sección **"Deploy"**
4. Click en **"Configure & Deploy"**
5. Configura las variables de entorno mencionadas arriba
6. Click en **"Deploy"**

### Paso 5: Verificar el Despliegue

Una vez desplegado, verifica que la API esté funcionando:

```bash
# Health check
curl https://your-app.choreoapis.dev/api/health/

# API documentation (si está habilitada)
curl https://your-app.choreoapis.dev/api/schema/
```

## Configuración de Base de Datos

### Opción 1: Base de Datos Propia
Proporciona la `DATABASE_URL` de tu base de datos PostgreSQL existente.

### Opción 2: Base de Datos Gestionada de Choreo
Choreo puede proporcionar bases de datos gestionadas. Consulta la documentación de Choreo para más detalles.

## Migraciones de Base de Datos

Las migraciones se ejecutan automáticamente durante el despliegue gracias al comando `release` en el Procfile:

```
release: python manage.py migrate --noinput
```

## Archivos Estáticos

Los archivos estáticos se recolectan automáticamente durante el build de Docker:

```dockerfile
RUN python manage.py collectstatic --noinput
```

## Configuración de CORS

Asegúrate de actualizar `CORS_ALLOWED_ORIGINS` en las variables de entorno con la URL de tu frontend:

```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-app.vercel.app
```

## Monitoring y Logs

Choreo proporciona herramientas de observabilidad integradas:
- **Logs**: Ver logs en tiempo real en la consola de Choreo
- **Metrics**: Monitorear CPU, memoria y request rates
- **Traces**: Debugging de requests individuales

## Solución de Problemas

### Error: "ModuleNotFoundError"
- Verifica que todas las dependencias estén en `requirements.txt`
- Asegúrate de que el build haya terminado exitosamente

### Error: "Database connection failed"
- Verifica que `DATABASE_URL` esté correctamente configurado
- Asegúrate de que la base de datos permita conexiones desde Choreo

### Error: "Static files not found"
- Verifica que `collectstatic` se ejecute correctamente en el build
- Configura `STATIC_ROOT` en `settings.py`

### Error: "CORS errors"
- Verifica `CORS_ALLOWED_ORIGINS` en las variables de entorno
- Asegúrate de que `django-cors-headers` esté instalado y configurado

## Comandos Útiles

### Generar SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Verificar configuración local
```bash
python manage.py check --deploy
```

### Crear superusuario en producción
```bash
python manage.py createsuperuser
```

## Actualizaciones

Para desplegar nuevas versiones:

1. Realiza los cambios en tu código
2. Commit y push al repositorio
3. Choreo detectará los cambios automáticamente
4. Click en **"Build"** y luego **"Deploy"**

## CI/CD

Choreo soporta CI/CD automático. Puedes configurar:
- **Auto Deploy**: Despliega automáticamente cuando se hace push a una rama específica
- **Environments**: Crea diferentes entornos (dev, staging, production)
- **Approval Gates**: Requiere aprobación manual antes del despliegue

## Seguridad

### Recomendaciones:
- ✅ Usa HTTPS (Choreo lo proporciona automáticamente)
- ✅ Mantén `DEBUG=False` en producción
- ✅ Usa contraseñas fuertes para la base de datos
- ✅ Rota las claves secretas periódicamente
- ✅ Habilita `DATABASE_SSL_MODE=require`
- ✅ Configura CORS correctamente
- ✅ Mantén las dependencias actualizadas

## Recursos Adicionales

- [Documentación de Choreo](https://wso2.com/choreo/docs/)
- [Guía de Django en Choreo](https://medium.com/choreo-tech-blog/effortless-development-of-cloud-native-applications-in-django-with-choreo-1ca4b349c58c)
- [Documentación de Django Deployment](https://docs.djangoproject.com/en/5.2/howto/deployment/)

## Soporte

Si encuentras problemas:
1. Revisa los logs en la consola de Choreo
2. Consulta la documentación de Choreo
3. Contacta al soporte de Choreo o WSO2

---

**¡Tu backend está listo para desplegarse en Choreo!** 🚀
