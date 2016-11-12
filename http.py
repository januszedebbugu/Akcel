pins = [(0, 12, 234, 355), (1, 134, 2545, 334), (2, 122, 662, 3745), (3, 145, 25, 43)]
html = """<!DOCTYPE html>
<html>
    <head> <title>Akcelerometr ESP8266</title> </head>
    <body> <h1>Akcelerometr ESP8266</h1>
        <table border="1"> <tr><th>ts</th><th>X</th><th>Y</th><th>Z</th></tr> %s </table>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (p[0], p[1], p[2], p[3]) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
