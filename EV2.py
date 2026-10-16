import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "fc141ccb-37fa-4230-b359-94514cbf11a5"  # Reemplazar con clave personal

def geocoding(location, key):
    while location == "":
        location = input("La ubicación no puede estar vacía. Ingrésela nuevamente: ")
    
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key, "locale": "es"})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("URL de API de Geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
        print("Coordenadas: Latitud {:.2f}, Longitud {:.2f}".format(lat, lng))
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data.get("message", "Error en la solicitud"))
            
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("auto, bicicleta, pie (car, bike, foot)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    
    vehiculos_opciones = {
        "auto": "car", "car": "car",
        "bicicleta": "bike", "bike": "bike",
        "pie": "foot", "foot": "foot"
    }
    
    vehiculo_input = input("Ingrese un perfil de vehículo (o 's' / 'salir' para finalizar): ").strip().lower()
    
    if vehiculo_input in ["s", "salir", "q", "quit"]:
        print("¡Programa finalizado exitosamente!")
        break
    
    if vehiculo_input in vehiculos_opciones:
        vehicle = vehiculos_opciones[vehiculo_input]
    else:
        vehicle = "car"
        print("No ingresó un perfil válido. Se usará el perfil de 'auto' (car) por defecto.")
    
    loc1 = input("Ubicación de Origen (o 's' / 'salir' para finalizar): ").strip()
    if loc1.lower() in ["s", "salir", "q", "quit"]:
        print("¡Programa finalizado exitosamente!")
        break
        
    orig = geocoding(loc1, key)
    
    loc2 = input("Ubicación de Destino (o 's' / 'salir' para finalizar): ").strip()
    if loc2.lower() in ["s", "salir", "q", "quit"]:
        print("¡Programa finalizado exitosamente!")
        break
        
    dest = geocoding(loc2, key)
    
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        
        print("Estado de API de Ruta: " + str(paths_status) + "\nURL de API de Ruta:\n" + paths_url)
        print("=================================================")
        print("Indicaciones de viaje desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle)
        print("=================================================")
        
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            
            print("Distancia recorrida: {:.2f} millas / {:.2f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            print("NARRATIVA DEL VIAJE (INSTRUCCIONES PASO A PASO):")
            print("=================================================")
            
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {:.2f} km / {:.2f} millas )".format(path, distance / 1000, (distance / 1000) / 1.61))
            print("=================================================")
        else:
            print("Mensaje de error: " + paths_data.get("message", "No se encontró una conexión entre las ubicaciones."))
            print("*************************************************")