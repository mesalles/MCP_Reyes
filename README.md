# MCP UJI Academic Server

Servidor MCP (Model Context Protocol) HTTP que proporciona acceso a la información académica de la Universitat Jaume I (UJI). Optimizado para acceso remoto a través de HTTP con compatibilidad completa con MCP Inspector.

## ✨ Características Principales

- 🎓 **Acceso Completo a Datos Académicos**: Asignaturas, titulaciones, horarios y ubicaciones
- 🌐 **Soporte Multiidioma**: Contenido en catalán, español e inglés  
- 🌍 **HTTP Puro**: Servidor HTTP optimizado para acceso remoto y compatibilidad máxima
- ⚡ **Cache Inteligente**: Sistema de caché integrado para mejor rendimiento
- 🔍 **Funcionalidad de Búsqueda**: Búsqueda avanzada en asignaturas, titulaciones y ubicaciones
- 📅 **Gestión de Horarios**: Análisis y gestión de horarios en formato iCalendar
- 🛡️ **Manejo Robusto de Errores**: Gestión de errores con mensajes descriptivos
- 🔒 **Seguridad de Tipos**: Type hints completos y modelos Pydantic para validación
- 🔧 **Compatible con MCP Inspector**: Funciona perfectamente con herramientas de desarrollo MCP

## 🔧 Instalación

### Prerrequisitos

- Python 3.12 o superior
- Gestor de paquetes UV

### Configuración

1. **Clona el repositorio**:

   ```bash
   git clone <repository-url>
   cd MCP_UJI_academic
   ```

2. **Instala las dependencias con UV**:

   ```bash
   uv sync
   ```

## ⚙️ Configuración de Clientes MCP

> **📡 Servidor Remoto**: El servidor MCP se ejecuta en una máquina remota (ej: `150.128.81.57:8084`), no en tu máquina local. Las configuraciones están optimizadas para este escenario.

### Claude Desktop

Para usar el servidor remoto con Claude Desktop, agrega la siguiente configuración a tu archivo `claude_desktop_config.json`:

**Ubicación del archivo de configuración:**

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

**Configuración para Servidor Remoto (Recomendado):**

> **⚠️ Nota**: Claude Desktop no soporta directamente servidores HTTP remotos, por lo que necesitas usar un proxy local o ejecutar el servidor localmente.

**Opción A: Proxy SSH (Recomendado)**

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "ssh",
      "args": [
        "-L", "8084:localhost:8084",
        "usuario@IP_SERVIDOR_REMOTO",
        "cd /ruta/en/servidor/remoto/MCP_UJI_academic && uv run start_server.py --host 127.0.0.1 --port 8084"
      ]
    }
  }
}
```

**Opción B: Copia Local del Proyecto**

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "uv",
      "args": ["run", "start_server.py", "--host", "127.0.0.1", "--port", "8084"],
      "cwd": "/ruta/local/al/proyecto/MCP_UJI_academic"
    }
  }
}
```

> **⚠️ Importante**: 
> - Cambia `IP_SERVIDOR_REMOTO` por la IP real del servidor
> - Cambia `usuario` por tu usuario en el servidor remoto
> - Asegúrate de tener acceso SSH al servidor remoto

### Visual Studio Code

Para usar el servidor remoto con VS Code y extensiones MCP:

#### Servidor HTTP Remoto (Recomendado)

```json
{
  "mcp.servers": {
    "mcp-uji-academic": {
      "transport": "http",
      "url": "http://IP_SERVIDOR_REMOTO:8084/mcp"
    }
  }
}
```

> **⚠️ Importante**: Cambia `IP_SERVIDOR_REMOTO` por la IP real del servidor (ej: `150.128.81.57`)

#### Túnel SSH (Alternativo)

Si prefieres usar un túnel SSH:

1. **Establece el túnel:**
   ```bash
   ssh -L 8084:localhost:8084 usuario@IP_SERVIDOR_REMOTO
   ```

2. **Configuración VS Code:**
   ```json
   {
     "mcp.servers": {
       "mcp-uji-academic": {
         "transport": "http",
         "url": "http://127.0.0.1:8084/mcp"
       }
     }
   }
   ```

### Otras Aplicaciones MCP

Para cualquier cliente MCP que soporte HTTP, conecta al servidor remoto:

- **Endpoint MCP Remoto**: `http://IP_SERVIDOR_REMOTO:8084/mcp`
- **Endpoint Desarrollo**: `http://150.128.81.57:8084/mcp`
- **Método**: `POST`
- **Headers**: `Content-Type: application/json`
- **Protocolo**: JSON-RPC 2.0

**Ejemplo de configuración genérica:**

```json
{
  "servers": {
    "uji-academic": {
      "transport": "http",
      "endpoint": "http://150.128.81.57:8084/mcp",
      "timeout": 30000
    }
  }
}
```

## 🚀 Uso del Servidor

### Servidor HTTP MCP

```bash
# Servidor en localhost (desarrollo)
python start_server.py --mode remote --host 127.0.0.1 --port 8084

# Servidor accesible desde la red
python start_server.py --mode remote --host 0.0.0.0 --port 8084

# Con auto-reload para desarrollo
python start_server.py --mode remote --host 127.0.0.1 --port 8084 --reload

# Usando UV directamente
uv run start_server.py --mode remote --host 0.0.0.0 --port 8084
```

> **💡 Nota**: El servidor solo funciona en modo remoto HTTP. Para acceso desde la red, usa `--host 0.0.0.0`.

## � Integración y Testing

### MCP Inspector (Recomendado)

Para probar y explorar el servidor de forma interactiva:

1. **Instala el MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **Configura la conexión**:
   - **Transport**: `Streamable HTTP`
   - **URL Remota**: `http://150.128.81.57:8084/mcp`
   - **URL Local**: `http://localhost:8084/mcp` (si usas túnel SSH)
   - **Method**: `POST`

3. **Explora las herramientas**: El inspector te permitirá ver y probar todas las 8 herramientas disponibles

### Test Manual con curl

```bash
# Verificar servidor activo
curl -X GET http://localhost:8084/health

# Listar herramientas disponibles
curl -X GET http://localhost:8084/tools

# Test de ping MCP
curl -X POST http://localhost:8084/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "ping"}'

# Listar herramientas MCP
curl -X POST http://localhost:8084/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```

## 🌐 Endpoints del Servidor HTTP

### Desarrollo Local (localhost)

- 🏠 **Información del servidor**: `GET http://localhost:8084/`  
- 💓 **Health check**: `GET http://localhost:8084/health`
- 🛠️ **Lista de herramientas**: `GET http://localhost:8084/tools`
- 🔌 **Endpoint MCP**: `POST http://localhost:8084/mcp`

### Servidor de Producción

- 🏠 **Información del servidor**: `GET http://150.128.81.57:8084/`  
- 💓 **Health check**: `GET http://150.128.81.57:8084/health`
- 🛠️ **Lista de herramientas**: `GET http://150.128.81.57:8084/tools`
- 🔌 **Endpoint MCP**: `POST http://150.128.81.57:8084/mcp`

## �️ Herramientas MCP Disponibles (8 herramientas)

El servidor HTTP MCP proporciona herramientas optimizadas para acceso académico UJI:

### 📚 Asignaturas (2 herramientas)

- **`get_subjects`**: Lista paginada con filtros y soporte multiidioma
- **`search_subjects`**: Búsqueda inteligente por nombre o código

### 🎓 Titulaciones (2 herramientas)

- **`get_degrees`**: Catálogo completo de grados y másteres
- **`search_degrees`**: Búsqueda de titulaciones por nombre

### 🏢 Ubicaciones (2 herramientas)

- **`get_locations`**: Directorio de edificios, aulas y laboratorios
- **`search_locations`**: Búsqueda de espacios universitarios

### 📅 Horarios (2 herramientas)

- **`get_class_schedule`**: Calendarios de clases por titulación/año
- **`get_exam_schedule`**: Calendarios de exámenes por titulación/año

> **🌐 Todas las herramientas**: Soporte CA/ES/EN y respuestas JSON estructuradas

## 📚 Recursos MCP

- **`uji://api/info`**: Información sobre la API y endpoints disponibles

## 🧪 Desarrollo y Testing

### Tests de Integración

```bash
# Test completo del sistema
uv run python integration_test.py

# Test específico de herramientas
python test_websocket.py  # Ahora solo prueba HTTP
```

### Desarrollo con Auto-reload

```bash
# Servidor con recarga automática
python start_server.py --mode remote --host 127.0.0.1 --port 8084 --reload
```

### Verificación Rápida

```bash
# Verificar servidor activo
curl http://localhost:8084/health

# Test de conectividad MCP
curl -X POST http://localhost:8084/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "ping"}'
```

### Verificar Servidor Remoto

**Desarrollo local:**

```bash
# Health check
curl http://localhost:8084/health

# Lista de herramientas disponibles  
curl http://localhost:8084/tools
```

**Servidor de prueba:**

```bash
# Health check
curl http://150.128.81.57:8084/health

# Lista de herramientas disponibles  
curl http://150.128.81.57:8084/tools
```

## 🔗 API Externa Utilizada

Este servidor utiliza la API REST oficial de UJI:

- **Base URL**: https://ujiapps.uji.es/lod-autorest/api/
- **Datasets**: asignaturas, titulaciones, ubicaciones, horarios
- **Formatos**: JSON, iCalendar (para horarios)

## 📁 Estructura del Proyecto

```
MCP_UJI_academic/
├── mcp_server.py          # Servidor HTTP MCP principal
├── start_server.py        # Launcher del servidor HTTP
├── api_client.py          # Cliente API de UJI
├── models.py              # Modelos Pydantic
├── integration_test.py    # Tests de integración
├── pyproject.toml         # Configuración del proyecto
└── README.md              # Esta documentación
```

## 🔧 Solución de Problemas

### Error "Port already in use"

```bash
# Verificar qué proceso usa el puerto
lsof -i :8084

# Usar otro puerto
python start_server.py --mode remote --port 8001
```

### Error de conexión WebSocket

- Verifica que el servidor remoto esté ejecutándose
- Comprueba la URL del WebSocket en la configuración
- Revisa los logs del servidor para errores

### Conexión al servidor de prueba (150.128.81.57)

Si no puedes conectarte al servidor de prueba:

```bash
# Verificar conectividad de red
ping 150.128.81.57

# Verificar que el puerto 8084 esté accesible
telnet 150.128.81.57 8084
# o con nc:
nc -zv 150.128.81.57 8084
```

**Configuración de firewall** (en el servidor de prueba):

```bash
# Permitir tráfico en puerto 8084
sudo ufw allow 8084/tcp

# Verificar estado del firewall
sudo ufw status
```

### Problemas con uv

```bash
# Reinstalar dependencias
uv sync --reinstall
```

## 🚦 Estado del Proyecto

- ✅ Servidor local (stdio) funcional
- ✅ Servidor remoto (HTTP/WebSocket) funcional  
- ✅ 8 herramientas MCP implementadas
- ✅ Tests de integración completos
- ✅ Documentación completa
- ✅ Ejemplos de configuración

## 📄 Licencia

MIT License

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la sección de solución de problemas
2. Ejecuta los tests de integración
3. Prueba con MCP Inspector
4. Crea un issue en el repositorio
