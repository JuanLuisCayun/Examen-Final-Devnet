from ncclient import manager
from getpass import getpass

ROUTER = {
    "host": "192.168.56.101",
    "port": 830,
    "username": input("Usuario del CSR1000v: "),
    "password": getpass("Contraseña del CSR1000v: "),
    "hostkey_verify": False,
    "device_params": {"name": "csr"}
}

CONFIGURACION = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>JuanLuis-Cayun</hostname>
    <interface>
      <Loopback>
        <name>11</name>
        <description>Configurada mediante NETCONF</description>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

try:
    print("\nConectando mediante SSH y NETCONF...")

    with manager.connect(**ROUTER) as conexion:
        print("Conexión NETCONF establecida correctamente.")
        print(f"ID de sesión NETCONF: {conexion.session_id}")

        respuesta = conexion.edit_config(
            target="running",
            config=CONFIGURACION
        )

        if respuesta.ok:
            print("Configuración aplicada correctamente.")
            print("Hostname configurado: JuanLuis-Cayun")
            print("Interfaz creada: Loopback11")
            print("Dirección IPv4: 11.11.11.11/32")

except Exception as error:
    print(f"Error durante la conexión o configuración: {error}")

