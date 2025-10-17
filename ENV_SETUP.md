# 🔧 Variables de Entorno - Guía de Configuración

## Frontend (Next.js)

### Archivos:
- **`.env.local`** ✅ - Archivo real con tus valores (NO commitear)
- **`.env.example`** - Template de ejemplo (SÍ commitear)

### Variables Requeridas:

```bash
# 1. API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```
- **Descripción**: URL del backend Django
- **Desarrollo**: `http://localhost:8000/api`
- **Producción**: `https://tu-dominio-backend.com/api`

---

```bash
# 2. Stripe Configuration
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51SCyCwRejqoz7DSb...
```
- **Descripción**: Clave pública de Stripe
- **Obtener**: https://dashboard.stripe.com/apikeys
- **Desarrollo**: Usar `pk_test_...` (modo test)
- **Producción**: Usar `pk_live_...` (modo live)

---

```bash
# 3. Currency Symbol
NEXT_PUBLIC_CURRENCY_SYMBOL=$
```
- **Descripción**: Símbolo de moneda para mostrar precios
- **Valores comunes**: `$`, `€`, `£`, `₹`, `MXN$`

---

### ⚠️ Importante:
- Variables con prefijo `NEXT_PUBLIC_` son **expuestas al navegador**
- **NUNCA** pongas claves secretas con prefijo `NEXT_PUBLIC_`
- Reinicia el servidor de desarrollo después de cambiar variables
- En producción (Vercel/Netlify), configura las variables en el dashboard

---

## Backend (Django)

### Archivo:
- **`backend/.env`** - Archivo con variables del backend

### Variables Requeridas:

```bash
# 1. Django Settings
SECRET_KEY=tu-clave-secreta-super-aleatoria-aqui
DEBUG=True  # False en producción
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Generar SECRET_KEY seguro:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

```bash
# 2. Database (PostgreSQL)
DATABASE_URL=postgresql://usuario:password@host:puerto/database?sslmode=require
```
- **Formato**: `postgresql://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require`
- **Ejemplo Neon**: Ya configurado en tu `.env`

---

```bash
# 3. CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```
- **Desarrollo**: URLs locales
- **Producción**: Agregar tu dominio frontend real

---

```bash
# 4. MailerSend (Email)
MAILERSEND_API_KEY=mlsn.tu_api_key_aqui
MAILERSEND_SENDER_DOMAIN=tu-dominio.com
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com
```
- **Obtener**: https://www.mailersend.com/
- **Opcional** en desarrollo (emails no funcionarán)

---

```bash
# 5. Stripe (Backend)
STRIPE_SECRET_KEY=sk_test_51SCyCwRejqoz7DSb...
STRIPE_PUBLISHABLE_KEY=pk_test_51SCyCwRejqoz7DSb...
```
- **Secret key**: `sk_test_...` (NUNCA exponer al público)
- **Obtener**: https://dashboard.stripe.com/apikeys

---

```bash
# 6. JWT Settings (Opcional - hay defaults)
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
```

---

## 📝 Checklist de Setup

### Desarrollo Local:

#### Frontend:
- [ ] Copiar `frontend/.env.example` a `frontend/.env.local`
- [ ] Configurar `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
- [ ] Agregar tu Stripe publishable key
- [ ] Configurar símbolo de moneda
- [ ] Reiniciar servidor: `npm run dev`

#### Backend:
- [ ] Crear `backend/.env` si no existe
- [ ] Generar y configurar `SECRET_KEY`
- [ ] Configurar `DATABASE_URL` (PostgreSQL)
- [ ] Configurar `CORS_ALLOWED_ORIGINS`
- [ ] Agregar Stripe secret key
- [ ] (Opcional) Configurar MailerSend
- [ ] Activar venv: `.venv\Scripts\activate` (Windows)
- [ ] Aplicar migraciones: `python manage.py migrate`
- [ ] Iniciar servidor: `python manage.py runserver`

---

## 🚀 Producción

### Frontend (Vercel/Netlify):
En el dashboard de tu hosting, agrega estas variables:
```
NEXT_PUBLIC_API_URL=https://api.tu-dominio.com/api
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_CURRENCY_SYMBOL=$
```

### Backend (Heroku/Railway/Render):
```
SECRET_KEY=clave-super-segura-aleatoria
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://...  (proporcionado por el host)
CORS_ALLOWED_ORIGINS=https://tu-frontend.com
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
```

---

## 🔐 Seguridad

### ✅ Hacer:
- Usar `.env.local` para variables locales en Next.js
- Agregar `.env` y `.env*.local` al `.gitignore`
- Generar `SECRET_KEY` único y aleatorio
- Usar claves de test (`pk_test_`, `sk_test_`) en desarrollo
- Cambiar a claves live (`pk_live_`, `sk_live_`) en producción
- Mantener `DEBUG=False` en producción

### ❌ NO Hacer:
- NO commitear archivos `.env` con valores reales
- NO usar la misma `SECRET_KEY` en dev y producción
- NO exponer `SECRET_KEY` o claves privadas en frontend
- NO usar `DEBUG=True` en producción
- NO reutilizar contraseñas entre servicios

---

## 🛠️ Troubleshooting

### "Backend no conecta"
- Verifica `NEXT_PUBLIC_API_URL` en frontend
- Verifica `CORS_ALLOWED_ORIGINS` en backend
- Asegúrate que backend está corriendo en puerto 8000

### "Stripe no funciona"
- Verifica que tienes claves de test configuradas
- Revisa que la publishable key está en frontend
- Revisa que la secret key está en backend

### "Emails no se envían"
- MailerSend requiere configuración y dominio verificado
- En desarrollo, los emails fallarán sin configuración
- Esto es opcional para testing básico

---

## 📞 Ayuda

Si tienes problemas:
1. Verifica que todas las variables están configuradas
2. Reinicia ambos servidores después de cambios
3. Revisa los logs de errores
4. Verifica que las URLs no tengan espacios o caracteres extraños

---

**Última actualización**: 2025-10-17
