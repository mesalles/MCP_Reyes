# MCP UJI Academic Server

Servidor HTTP del Model Context Protocol (MCP) que expone la información académica de la Universitat Jaume I (UJI). Permite consultar asignaturas, titulaciones, ubicaciones y calendarios oficiales desde clientes MCP compatibles y desde integraciones HTTP sencillas.

## ✨ Características clave

- 🎓 Acceso unificado a datos académicos (asignaturas, estudios, ubicaciones y horarios)
- 🌐 Soporte multiidioma cuando la API lo proporciona (catalán, español e inglés)
- ⚡ Caché en memoria para reducir llamadas repetidas a la API de la UJI
- 🧰 Ocho herramientas MCP listas para usar y compatibles con MCP Inspector
- 🛡️ Modelos Pydantic y manejo consistente de errores para clientes remotos

## 🧱 Requisitos previos

- Python 3.12 o superior
- [uv](https://docs.astral.sh/uv/) instalado como gestor de dependencias
- Acceso a internet para consultar la API pública de la UJI

## 🚀 Instalación y configuración

```bash
git clone <repository-url>
cd MCP_UJI_academic
uv sync
```

## ▶️ Ejecución del servidor

```bash
# Desarrollo local
uv run start_server.py --host 127.0.0.1 --port 8084

# Servidor accesible desde la red
uv run start_server.py --host 0.0.0.0 --port 8084

# Desarrollo con recarga automática
uv run start_server.py --host 127.0.0.1 --port 8084 --reload
```

> `start_server.py` es un lanzador que arranca `mcp_server.py` con los parámetros indicados. Si prefieres usar directamente Python, ejecuta `python start_server.py`.

## 🌐 Endpoints HTTP principales

| Método | Ruta       | Descripción                                                   |
|--------|------------|---------------------------------------------------------------|
| GET    | `/`        | Información básica del servidor                               |
| GET    | `/health`  | Comprobación rápida de estado                                  |
| GET    | `/tools`   | Lista de herramientas MCP y sus esquemas de entrada           |
| POST   | `/mcp`     | Endpoint MCP JSON-RPC 2.0 para clientes compatibles           |

### Servidor remoto de referencia

- URL base: `http://150.128.81.57:8084`
- Endpoint MCP: `http://150.128.81.57:8084/mcp`
- Health check: `http://150.128.81.57:8084/health`

Sustituye la IP por la de tu despliegue cuando publiques el servidor en otro host.

## 🧰 Herramientas MCP disponibles

| Herramienta            | Datos que devuelve                                      | Parámetros principales |
|------------------------|----------------------------------------------------------|------------------------|
| `get_subjects`         | Listado paginado de asignaturas                         | `start`, `limit`, `full` |
| `search_subjects`      | Búsqueda por código o nombre de asignaturas             | `query`, `language`    |
| `get_degrees`          | Catálogo completo de titulaciones                       | `full`                 |
| `search_degrees`       | Búsqueda de titulaciones                                | `query`, `language`    |
| `get_locations`        | Ubicaciones (edificios, aulas, laboratorios)            | `full`                 |
| `search_locations`     | Búsqueda de ubicaciones                                 | `query`                |
| `get_class_schedule`   | Horario lectivo en formato iCalendar                    | `year`, `degree_id`    |
| `get_exam_schedule`    | Calendario de exámenes en formato iCalendar             | `year`, `degree_id`    |

Todas las herramientas devuelven JSON estructurado y, cuando procede, información en múltiples idiomas.

## 🤖 Conectar clientes MCP

### Recomendaciones generales

- El endpoint MCP habla JSON-RPC 2.0 sobre HTTP; cualquier cliente compatible puede usarlo.
- Asegúrate de que el puerto (`8084` por defecto) esté accesible desde tu máquina o túnel SSH.
- Para entornos públicos, añade autenticación o proxies seguros según tus políticas.

### MCP Inspector (`npx`)

```bash
npx @modelcontextprotocol/inspector
```

1. Abre el navegador (suele abrir `http://localhost:3000`).
2. Selecciona **Streamable HTTP** como transporte.
3. Introduce la URL del endpoint (`http://150.128.81.57:8084/mcp` o tu instancia).
4. Pulsa **Connect** y prueba cualquiera de las ocho herramientas disponibles.

### VS Code (extensión MCP)

Añade al `settings.json` del usuario o del workspace:

```json
{
  "mcp.servers": {
    "mcp-uji-academic": {
      "transport": "http",
      "url": "http://150.128.81.57:8084/mcp"
    }
  }
}
```

Si usas un túnel SSH:

```bash
ssh -L 8084:localhost:8084 usuario@IP_SERVIDOR_REMOTO
```

Y cambia la URL a `http://127.0.0.1:8084/mcp`.

### Claude Desktop

Claude Desktop **no** puede llamar a un servidor HTTP remoto por sí mismo: solo lanza comandos locales. Por eso necesitas que el servidor MCP esté disponible en tu máquina (directamente o a través de un túnel) **antes** de arrancar Claude.

1. **Decide cómo traer el servidor a tu máquina**

    **Ejecución local:** clona el repo y arranca `uv run start_server.py --host 127.0.0.1 --port 8084` en una terminal independiente.

    **Túnel SSH:** si el servidor vive en otra máquina, abre `ssh -L 8084:localhost:8084 usuario@IP_REMOTO` para redirigir el puerto 8084 hacia tu equipo. Mantén el túnel abierto mientras uses Claude.

2. **Configura Claude para lanzar/verificar el servidor**

    Claude ejecutará un comando local cada vez que necesite el servidor MCP. Puedes usar `uv run start_server.py` (cuando trabajas con una copia local) o un script que establezca el túnel y compruebe que responde.

Como punto de partida, añade algo similar a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "uv",
      "args": [
        "run",
        "start_server.py",
        "--host",
        "127.0.0.1",
        "--port",
        "8084"
      ],
      "cwd": "/ruta/completa/a/MCP_UJI_academic"
    }
  }
}
```

Si dependes de un túnel SSH, puedes hacer que Claude abra el túnel, espere a que responda el `/health` y mantenga la sesión mientras esté activo:

```json
{
  "mcpServers": {
    "mcp-uji-academic": {
      "command": "bash",
      "args": [
        "-lc",
        "trap 'kill $SSH_PID' EXIT; ssh -N -L 8084:localhost:8084 usuario@IP_REMOTO & SSH_PID=$!; sleep 2; curl --fail http://127.0.0.1:8084/health >/dev/null; wait $SSH_PID"
      ]
    }
  }
}
```

- Ajusta `cwd` a la ruta real del proyecto cuando uses la copia local.
- En el ejemplo del túnel, reemplaza `usuario@IP_REMOTO`, ajusta puertos si lo necesitas y añade lógica de limpieza si piensas cerrar Claude manualmente.
- Si la cuenta remota usa contraseña, el comando te pedirá la clave en la terminal que arranca Claude; instala una clave SSH o usa herramientas como `sshpass` (solo si tu política de seguridad lo permite) para automatizarlo.
- El comando dentro de `args` debe ir en una sola línea; JSON no admite saltos manuales (`\`) dentro de strings.
- Reinicia Claude Desktop tras modificar el archivo para que recargue la configuración.

> `npx @modelcontextprotocol/inspector` es una herramienta de testing. VS Code y Claude necesitan configuraciones JSON propias.

## 🧪 Pruebas y verificación

```bash
# Test de integración (arranca el servidor temporalmente y verifica endpoints)
uv run python integration_test.py

# Checks manuales rápidos
curl http://127.0.0.1:8084/health
curl -X POST http://127.0.0.1:8084/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "ping"}'
```

## 📁 Estructura del proyecto

```text
MCP_UJI_academic/
├── api_client.py       # Cliente HTTP con caché y parseo iCalendar
├── integration_test.py # Prueba de arranque y endpoints HTTP
├── mcp_server.py       # FastAPI con endpoints HTTP y MCP JSON-RPC
├── models.py           # Modelos Pydantic para datos académicos
├── start_server.py     # Lanzador de conveniencia
├── pyproject.toml      # Configuración y dependencias
└── README.md           # Documentación (este archivo)
```

## 🛠️ Resolución de problemas

| Problema                                | Cómo solucionarlo |
|-----------------------------------------|--------------------|
| Puerto 8084 ocupado                     | `lsof -i :8084` para identificar el proceso o arranca con `--port 8001`. |
| Timeout o conexión rechazada            | Comprueba firewall/túneles y ejecuta `curl http://<host>:8084/health`. |
| Dependencias inconsistentes con uv      | Ejecuta `uv sync --reinstall`. |
| Errores de la API pública de la UJI     | Revisa los logs del servidor y reintenta; la API puede ser lenta o intermitente. |

## 🌍 API externa usada

- Base URL: `https://ujiapps.uji.es/lod-autorest/api/`
- Datos disponibles: asignaturas, estudios, ubicaciones y calendarios en JSON/iCalendar

## 📄 Licencia y soporte

- Licencia: MIT
- ¿Dudas o incidencias? Abre un issue, revisa la tabla de solución de problemas o ejecuta el test de integración antes de reportar.

---

Proyecto creado para facilitar el acceso programático a la información académica de la UJI dentro del ecosistema MCP. ¡Aprovecha y automatiza tus flujos educativos!
