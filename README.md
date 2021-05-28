# Private Teams Bot

Crea canales de texto y voz, privados para equipos.

## Instalación

Para instalar las bibliotecas requeridas, utiliza el manejador de paquetes [pip](https://pip.pypa.io/en/stable/).

```bash
pip install -r requirements.txt
```

Crea el archivo `.env` con el token de Discord:
```bash
echo DISCORD=<token> > .env
```

## Comandos

### Administradores

Solo los administradores pueden ejecutar los siguientes comandos.


Iniciar (o reiniciar) el bot:
```
!start
```

Cambiar CSV con datos:
```
!new_csv <subir CSV como archivo adjunto>
```

Revisar los actuales valores de la configuración:
```
!view_config
```

### Usuarios

Todos los usuarios pueden ejecutar estos comandos.

Identificar usuario:
```
!check <email>
```

## Licencia
[MIT](LICENSE)
