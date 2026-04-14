from pathlib import Path
from datetime import datetime


def parse_line(line, source="test.log"):
    """
    Convierte una línea de log en un evento básico.
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "event_type": "log",
        "severity": "info",
        "message": line.strip()
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
                events.append(parse_line(line, path.name))

    return events


if __name__ == "__main__":
    log_file = "logs/test.log"
    events = read_log_file(log_file)

    for event in events:
        print(event)