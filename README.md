# MCP UJI Academic Server

Servidor MCP (Model Context Protocol) HTTP que proporciona acceso a la información académica de la Universitat Jaume I (UJI). Optimizado para acceso remoto a través de HTTP con compatibilidad completa con MCP Inspector.

## ✨ Características Principales

- 🎓 **Acceso Completo a Datos Académicos**: Asignaturas, titulaciones, horarios y ubicaciones
- 🌐 **Soporte Multiidioma**: Contenido en catalán, español e inglés  
- 🌍 **HTTP Puro**: Servidor HTTP op### Error de conexión HTTP

- Verifica que el servidor remoto esté ejecutándose
- Comprueba la URL HTTP en la configuración (`http://IP:8084/mcp`)
- Revisa los logs del servidor para errores
- Confirma que el puerto 8084 esté abiertoado para acceso remoto y compatibilidad máxima
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

### 🤔 ¿NPX para Claude Desktop o VS Code?

**❌ NO**: `npx @modelcontextprotocol/inspector` es **SOLO** una herramienta de testing y desarrollo, no conecta Claude Desktop o VS Code al servidor.

**✅ SÍ**: Claude Desktop y VS Code necesitan sus propias configuraciones específicas (JSON) para conectarse al servidor MCP.

**Diferencias:**

| Cliente | Método de Conexión | Configuración |
|---------|-------------------|---------------|
| **MCP Inspector** | `npx` (temporal) | Interface web para testing |
| **Claude Desktop** | JSON config | Archivo `claude_desktop_config.json` |
| **VS Code** | JSON config | Settings de extensión MCP |

### Claude Desktop

Para usar el servidor remoto con Claude Desktop, agrega la siguiente configuración a tu archivo `claude_desktop_config.json`:

**Ubicación del archivo de configuración:**

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/claude/claude_desktop_config.json`

**📋 Cómo conectar Claude Desktop al servidor MCP:**

> **⚠️ Limitación**: Claude Desktop **NO puede conectarse directamente** a servidores HTTP remotos. Solo ejecuta comandos locales.

#### Opción A: Túnel SSH + Comando Local (Recomendado)

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "bash",
      "args": [
        "-c",
        "ssh -L 8084:localhost:8084 usuario@150.128.81.57 -N & sleep 3 && curl -s http://127.0.0.1:8084/mcp -X POST -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"ping\"}' > /dev/null && exec python3 -c \"import json,urllib.request; exec(open('/dev/stdin').read())\""
      ]
    }
  }
}
```

#### Opción B: Copia Local Completa (Más Simple)

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "uv",
      "args": ["run", "start_server.py", "--host", "127.0.0.1", "--port", "8084"],
      "cwd": "/ruta/local/completa/al/proyecto/MCP_UJI_academic"
    }
  }
}
```

#### Opción C: Proxy HTTP Local (Avanzado)

Si tienes un proxy HTTP local que redirija a tu servidor remoto:

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "python3",
      "args": ["-m", "http.server", "--bind", "127.0.0.1", "8084"],
      "env": {
        "PROXY_TARGET": "http://150.128.81.57:8084"
      }
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

### 📋 Resumen: NPX vs Configuración de Clientes

**Para aclarar la confusión:**

| Herramienta | ¿Usa NPX? | Propósito | Configuración |
|-------------|-----------|-----------|---------------|
| **MCP Inspector** | ✅ `npx @modelcontextprotocol/inspector` | Testing y desarrollo | Interface web temporal |
| **Claude Desktop** | ❌ NO usa NPX | Cliente productivo | JSON en archivo config |
| **VS Code** | ❌ NO usa NPX | Cliente productivo | JSON en settings |

**Respuesta directa:**
- **NPX**: Solo para testing con MCP Inspector
- **Claude Desktop**: Requiere configuración JSON (no NPX)  
- **VS Code**: Requiere configuración JSON (no NPX)
- **Servidor MCP**: Se conecta a TODOS mediante HTTP, pero cada cliente tiene su propio método

## 🚀 Uso del Servidor

### Servidor HTTP MCP

```bash
# Servidor en localhost (desarrollo)
uv run start_server.py --host 127.0.0.1 --port 8084

# Servidor accesible desde la red
uv run start_server.py --host 0.0.0.0 --port 8084

# Con auto-reload para desarrollo
uv run start_server.py --host 127.0.0.1 --port 8084 --reload

# Usando Python directamente (alternativo)
python start_server.py --host 0.0.0.0 --port 8084
```

> **💡 Nota**: El servidor es HTTP por defecto. Para acceso desde la red, usa `--host 0.0.0.0`.

## � Integración y Testing

### ¿Cuándo conectar con NPX?

**MCP Inspector con `npx` es ideal para:**

🔧 **Desarrollo y Testing**
- Validar que el servidor remoto está funcionando
- Probar nuevas funcionalidades sin configurar clientes
- Debug de problemas de conectividad

🚀 **Exploración Rápida**
- Ver todas las herramientas disponibles (8 herramientas UJI)
- Ejecutar llamadas MCP interactivamente
- Entender la estructura de respuestas JSON

⚡ **Sin Instalación**
- No requiere configuración compleja de clientes
- Funciona desde cualquier máquina con Node.js
- Ideal para demos y presentaciones

### MCP Inspector (Recomendado)

Para probar y explorar el servidor de forma interactiva usando `npx`:

#### Cuándo usar MCP Inspector con npx:

- ✅ **Siempre disponible**: No requiere instalación local
- ✅ **Testing rápido**: Ideal para pruebas y desarrollo
- ✅ **Exploración interactiva**: Ver todas las herramientas y probar llamadas
- ✅ **Validación de endpoints**: Confirmar que el servidor remoto funciona

#### Conexión al Servidor Remoto:

1. **Ejecuta MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **Configura la conexión en la interfaz web**:
   - **Transport**: `Streamable HTTP`
   - **URL**: `http://150.128.81.57:8084/mcp`
   - **Method**: `POST`

3. **Conecta y explora**:
   - El inspector se abrirá en tu navegador (normalmente `http://localhost:3000`)
   - Podrás ver las 8 herramientas disponibles
   - Probar llamadas MCP en tiempo real

#### Conexión con Túnel SSH (Alternativo):

Si prefieres usar un túnel SSH:

1. **Establece el túnel**:
   ```bash
   ssh -L 8084:localhost:8084 usuario@150.128.81.57
   ```

2. **Ejecuta MCP Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. **Configura con URL local**:
   - **URL**: `http://localhost:8084/mcp`
   - **Transport**: `Streamable HTTP`
   - **Method**: `POST`

> **🚀 Tip**: MCP Inspector es la forma más rápida de validar que tu servidor remoto está funcionando correctamente y explorar todas las herramientas disponibles.

### Ejemplo Práctico: Conexión con NPX

**Escenario 1: Conexión Directa al Servidor Remoto**

```bash
# 1. Ejecuta MCP Inspector
npx @modelcontextprotocol/inspector

# 2. Abre el navegador en http://localhost:3000
# 3. Configura la conexión:
#    - Transport: Streamable HTTP
#    - URL: http://150.128.81.57:8084/mcp
#    - Method: POST
# 4. Haz clic en "Connect"
# 5. Explora las 8 herramientas UJI disponibles
```

**Escenario 2: Verificación Rápida de Servidor**

```bash
# Antes de conectar clientes, verifica que el servidor responde:
curl http://150.128.81.57:8084/health

# Si responde {"status": "ok"}, entonces puedes usar:
npx @modelcontextprotocol/inspector
# Y conectar a http://150.128.81.57:8084/mcp
```

**Escenario 3: Desarrollo Local con Túnel**

```bash
# Terminal 1: Establece túnel SSH
ssh -L 8084:localhost:8084 usuario@150.128.81.57

# Terminal 2: Ejecuta inspector
npx @modelcontextprotocol/inspector
# Conecta a http://localhost:8084/mcp
```

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

# Test específico de herramientas HTTP
# (test_websocket.py fue eliminado tras simplificación)
```

### Desarrollo con Auto-reload

```bash
# Servidor con recarga automática
uv run start_server.py --host 127.0.0.1 --port 8084 --reload
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
uv run start_server.py --port 8001
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

- ✅ Servidor HTTP MCP funcional
- ✅ Compatible con MCP Inspector  
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
