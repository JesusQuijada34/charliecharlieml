# Charlie Charlie MultiLingual

**Identidad del paquete:** `influent.charliecharlieml.v1.0-26.08-21.56`
**Autor:** `JesusQuijada34`
**Plataforma:** `AlphaCube`
**Descripción:** Estructura reparada por MoonFix

## Estructura PackageMaker 3.2.7

Este repositorio fue normalizado mediante **MoonFix**, usando la estructura de PackageMaker 3.2.7. El paquete público debe conservar `details.xml`, `version.res`, `autorun`, `autorun.bat`, `.storedetail`, `updater.py`, `config/settings.json`, los marcadores `.container` y los archivos de documentación correspondientes. El publisher oficial es `influent` y la versión pública no contiene sufijo de plataforma.

## Instalación y ejecución

Instala las dependencias declaradas en `lib/requirements.txt` cuando exista y ejecuta el entrypoint real del proyecto. En Linux, los comandos privilegiados son específicos de Danenone y no deben trasladarse a Windows. En proyectos AlphaCube, la validación Windows debe realizarse con el `buildthis` oficial de PackageMaker.

## Validación

La fuente debe pasar compilación sintáctica, pruebas funcionales disponibles, comprobación de identidad XML, protección contra traversal en ZIP y llamadas seguras a subprocess. Los artefactos `.iflapp` deben ser generados por PackageMaker; los paquetes Debian deben usar el nombre canónico `influent.charliecharlieml.v1.0-26.08-21.56_ARCH.deb`.

## Release

El tag y el título del release deben ser exactamente `v1.0-26.08-21.56`. Los assets deben usar el nombre canónico del paquete y una extensión objetiva. No se permite publicar un release AlphaCube que contenga únicamente el build Linux.

## Imágenes conservadas


![Demo Screenshot](assets/screenshots/screenshot-1.png) ![Demo Screenshot](assets/screenshots/screenshot-2.png)

## Referencia original

# 🔮 CharlieCharlie MultiLingual

![Demo Screenshot](assets/screenshots/screenshot-1.png) ![Demo Screenshot](assets/screenshots/screenshot-2.png)

Un juego místico de preguntas/respuestas estilo "Charlie Charlie" con:
- **Traducción en tiempo real** (10+ idiomas)
- **Efectos visuales glitch**
- **Interfaz estilo posesión** (rojo/negro)
- **Resistencia paranormal al cierre**

## 🌍 Idiomas soportados
| Idioma       | Código |
|--------------|--------|
| English      | `en`   |
| Español      | `es`   |
| Français     | `fr`   |
| Deutsch      | `de`   |
| Italiano     | `it`   |
| Português    | `pt`   |
| 日本語        | `ja`   |
| 中文          | `zh`   |
| Русский      | `ru`   |
| العربية      | `ar`   |

---

## 🚀 Instalación
1. **Requisitos**:
   ```bash
   pip install PyQt5 requests pygame
   ```

2. **Ejecutar**:
   ```bash
   python charliecharlieml.py
   ```

---

## 🎮 Cómo jugar
1. Selecciona tu idioma al iniciar
2. Haz cualquier pregunta al tablero
3. Recibe respuestas aleatorias (SÍ/NO)
4. Para salir: pregunta *"¿Me puedo salir?"* (debe responder "SÍ")

> ⚠️ El juego **resistirá tu intento de cerrarlo** si no obtienes permiso

---

## 🛠️ Configuración
Los ajustes de idioma se guardan en:
```
config/settings.json
```

---

## 📌 Notas técnicas
- Usa la API pública de Google Translate
- Efectos visuales implementados con Qt (sin dependencias externas)
- Diseño responsive para diferentes pantallas

---

## 📜 Licencia
MIT License - Libre para uso y modificación

---

**¿Encontraste un bug?**
Abre un *issue* o contribuye al proyecto!

---

### 🔥 Features destacables:
- **Sistema de traducción dinámica**
- **Efectos de glitch nativos** (sin pygame)
- **Interfaz "poseída"** con animaciones
- **Persistencia de configuración**

¿Quieres que añada algo más específico? 😊
