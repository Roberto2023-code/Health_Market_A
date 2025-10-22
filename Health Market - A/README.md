# 🏥 Health Market - Plataforma de Salud y Bienestar

## 📋 Descripción

Health Market es una plataforma web integral que combina la venta de suplementos de calidad con servicios profesionales de nutrición. La aplicación permite a los usuarios comprar productos de salud, agendar consultas con nutriólogos y gestionar su bienestar de manera integral.

## ✨ Características Principales

### 🛒 E-commerce de Suplementos
- Catálogo completo de productos de salud
- Carrito de compras avanzado con persistencia
- Sistema de pagos integrado
- Gestión de inventario

### 👥 Sistema Multi-rol
- **Administradores**: Gestión completa del sistema
- **Clientes**: Compra de productos y servicios
- **Usuarios especializados**: Gestión de consultas médicas

### 🩺 Servicios de Salud
- Consultas médicas con nutriólogos certificados
- Planes de alimentación personalizados
- Subida de historial médico
- Seguimiento de citas

### 🔒 Seguridad Avanzada
- Hash seguro de contraseñas
- Validaciones robustas
- Manejo de errores global
- Sanitización de datos

## 🚀 Mejoras Implementadas

### 1. 🔐 Seguridad
- ✅ Hash de contraseñas con Werkzeug
- ✅ Validación de fortaleza de contraseñas
- ✅ Clave secreta configurable
- ✅ Sanitización de entradas de usuario

### 2. 🛡️ Validaciones y Manejo de Errores
- ✅ Validación de email en tiempo real
- ✅ Validación de formato de teléfono
- ✅ Páginas de error personalizadas (404, 500, 403)
- ✅ Manejo de excepciones robusto

### 3. 🎨 Interfaz de Usuario
- ✅ Validaciones en tiempo real en formularios
- ✅ Indicador de fortaleza de contraseña
- ✅ Carrito de compras mejorado con cantidades
- ✅ Persistencia del carrito en localStorage
- ✅ Modales de confirmación mejorados

### 4. 🗄️ Optimización de Base de Datos
- ✅ Índices para consultas optimizadas
- ✅ Funciones de base de datos organizadas
- ✅ Límites en consultas para mejor rendimiento
- ✅ Estructura de datos mejorada

### 5. 🏗️ Arquitectura del Código
- ✅ Separación de configuraciones
- ✅ Funciones de utilidad modulares
- ✅ Manejador de base de datos centralizado
- ✅ Código más limpio y mantenible

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web de Python
- **MongoDB** - Base de datos NoSQL
- **PyMongo** - Driver de MongoDB para Python
- **Werkzeug** - Utilidades de seguridad

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **Bootstrap 5** - Framework CSS
- **JavaScript** - Interactividad
- **Responsive Design** - Diseño adaptable

### Herramientas de Desarrollo
- **Git** - Control de versiones
- **Python 3.8+** - Lenguaje de programación

## 📁 Estructura del Proyecto

```
Dmarket-health 2KKK/
├── app.py                 # Aplicación principal Flask
├── config.py             # Configuraciones de la aplicación
├── utils.py              # Funciones de utilidad
├── database.py           # Manejador de base de datos
├── templates/            # Plantillas HTML
│   ├── pag-principal.html
│   ├── productos.html
│   ├── consultas.html
│   ├── registro.html
│   ├── error.html
│   └── ...
├── static/               # Archivos estáticos
│   ├── img/             # Imágenes
│   ├── css/             # Estilos CSS
│   └── uploads/         # Archivos subidos
└── uploads/             # Directorio de uploads
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- MongoDB 4.4 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd Dmarket-health-2KKK
   ```

2. **Instalar dependencias**
   ```bash
   pip install flask flask-pymongo werkzeug
   ```

3. **Configurar MongoDB**
   - Asegúrate de que MongoDB esté ejecutándose
   - La aplicación se conectará automáticamente a `mongodb://localhost:27017/market-health`

4. **Configurar variables de entorno (opcional)**
   ```bash
   export SECRET_KEY="tu-clave-secreta-super-segura"
   export MONGO_URI="mongodb://localhost:27017/market-health"
   export FLASK_ENV="development"
   ```

5. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

6. **Acceder a la aplicación**
   - Abre tu navegador en `http://localhost:5000`

## 👤 Roles de Usuario

### 🔑 Administrador
- Gestión completa de usuarios
- Acceso a todas las funcionalidades
- Panel de administración

### 👥 Cliente
- Compra de productos
- Agendamiento de consultas
- Acceso a perfil personal

### 🩺 Usuario Especializado
- Gestión de consultas médicas
- Acceso a historiales de pacientes
- Herramientas de seguimiento

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
SECRET_KEY=tu-clave-secreta
MONGO_URI=mongodb://localhost:27017/market-health
FLASK_ENV=development|production|testing
```

### Configuración de Producción
- Cambiar `SECRET_KEY` por una clave segura
- Configurar `FLASK_ENV=production`
- Usar una base de datos MongoDB en producción
- Configurar HTTPS

## 📊 Funcionalidades del Carrito

- ✅ Agregar/eliminar productos
- ✅ Modificar cantidades
- ✅ Cálculo automático de totales
- ✅ Persistencia en localStorage
- ✅ Interfaz responsive

## 🩺 Sistema de Consultas

- ✅ Formulario de agendamiento
- ✅ Subida de historial médico
- ✅ Validación de archivos
- ✅ Gestión de estados
- ✅ Notificaciones automáticas

## 🔒 Medidas de Seguridad

- ✅ Contraseñas hasheadas
- ✅ Validación de entrada
- ✅ Sanitización de datos
- ✅ Manejo seguro de archivos
- ✅ Protección contra inyección

## 🚀 Próximas Mejoras

- [ ] Sistema de notificaciones por email
- [ ] API REST para móviles
- [ ] Panel de analytics
- [ ] Sistema de reviews
- [ ] Integración con pasarelas de pago
- [ ] Tests automatizados

## 📞 Soporte

Para soporte técnico o consultas sobre el proyecto, contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Health Market** - Tu bienestar es nuestra prioridad 🏥✨


