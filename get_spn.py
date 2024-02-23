def get_spn(toponym):
    x1, y1 = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split())
    x2, y2 = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split())
    delta_x = str(x2 - x1)
    delta_y = str(y2 - y1)
    return ",".join([delta_x, delta_y])