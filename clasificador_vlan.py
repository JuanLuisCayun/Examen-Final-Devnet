def clasificar_vlan(vlan):
    if 1 <= vlan <= 1005:
        return "La VLAN pertenece al rango normal."
    elif 1006 <= vlan <= 4094:
        return "La VLAN pertenece al rango extendido."
    else:
        return "El número ingresado no corresponde a una VLAN válida."


try:
    vlan = int(input("Ingrese el número de VLAN: "))
    print(clasificar_vlan(vlan))
except ValueError:
    print("Error: debe ingresar un número entero.")
