from pathlib import Path

def parse_line(line, source="polvorin.log"):
    """
    Convierte una línea de log en un evento básico.
    
     Formato nuevo:
    timestamp | source | event_type | severity | user_id | access_point | 
    deposit_id | device_id | result | message
    """

    parts = [p.strip() for p in line.strip().split("|")]

    if len(parts) != 10:
        print(f"Línea ignorada: {line.strip()}")
        return None
    
    timestamp, source, event_type, severity, user_id, access_point, deposit_id, device_id, result, message = parts
    return {
        "timestamp": timestamp,
        "source": source,
        "event_type": event_type,
        "severity": severity,
        "user_id": user_id,
        "access_point": access_point,
        "deposit_id": deposit_id,
        "device_id": device_id,
        "result": result,
        "message": message
    }

def read_log_file(file_path):
    """
    Lee un archivo de log y devuelve una lista de eventos.
    """
    events = []

    path = Path(file_path)
    if not path.exists():
        print(f"Archivo no encontrado: {file_path}")
        return events

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                event = parse_line(line, path.name)
                if event:
                    events.append(parse_line(line, path.name))

    return events


if __name__ == "__main__":
    log_file = "logs/polvorin.log"
    events = read_log_file(log_file)

    for event in events:
        print(event)