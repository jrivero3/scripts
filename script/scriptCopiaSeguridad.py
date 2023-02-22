import os
import ftplib
import tarfile
import datetime
import smtplib
from email.mime.text import MIMEText

# Directorio a copiar
directorio = '/var/www/html/public_html'
# Servidor FTP remoto
servidorFTP = '213.194.172.127' #Tenemos asociado un subdominio a la IP pública
usuarioFTP = 'afernandez193'
contrasenaFTP = 'Admin2323'
# Número máximo de copias de seguridad
copiasMaximas = 10
# Correo del administrador
correoAdmin = 'jrivero32@ieszaidinvergeles.org'

# Obtener la fecha actual
fechaActual = datetime.datetime.now()
fechaCadena = fechaActual.strftime("%Y%m%d")

#Comprobamos si tiene todos los permisos.
permisos = oct(os.stat(directorio).st_mode)[-3:]

# Crear nombre de archivo de copia de seguridad
nombreCopia = 'copia' + fechaCadena + '.tar.gz'

# Comprimir directorio
with tarfile.open(nombreCopia, mode='w:gz') as archive:
    archive.add(directorio, recursive=True)

# Conectarse al servidor FTP
ftp = ftplib.FTP('213.194.172.127')
ftp.login('afernandez193', 'Admin2323')


# Subir archivo de copia de seguridad al servidor FTP
with open(nombreCopia, 'rb') as f:
    ftp.storbinary('STOR ' + nombreCopia, f)

# Eliminar archivo de copia de seguridad local
os.remove(nombreCopia)

# Obtener lista de archivos de copia de seguridad en el servidor FTP
archivos = ftp.nlst()
compruebaArchivos = [f for f in archivos if f.startswith('copia')]

# Borrar archivos de copia de seguridad antiguos si hay más de 10
if len(compruebaArchivos) > copiasMaximas:
    copiaAntigua = min(compruebaArchivos, key=lambda x: x[5:])
    ftp.delete(copiaAntigua)

# Cerrar conexión FTP
ftp.quit()

"""
# Enviar e-mail de confirmación
remitente = 'ftpserver@ieszaidinvergeles.org'
receptor = correoAdmin
mensaje = 'La copia de seguridad del directorio public_html se ha realizado con éxito.'
msg = MIMEText(mensaje)
msg['Subject'] = 'Copia de seguridad completada'
msg['From'] = remitente
msg['To'] = receptor

server = smtplib.SMTP('smtp.example.com')
server.sendmail(remitente, [receptor], msg.as_string())

#La tarea se realizará todos los días a las 12:00h mediante crontab
os.system("(crontab -l ; echo '0 12 * * * /usr/bin/python3 " + nombreCopia + "') | crontab -")

#Cortamos la conexión
server.quit()
"""

#Envío de correo
from email.message import EmailMessage
import smtplib
remitente = "ftprf@outlook.com"
destinatario = "jrivero32@ieszaidinvergeles.org"
mensaje = "La copia de seguridad del servidor realizada con el script fue exitosa"
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Copia de seguridad"
email.set_content(mensaje)
smtp = smtplib.SMTP_SSL("smtp.office365.com")
smtp.login(remitente, "Admin23Admin23")
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()
print ("El correo fue enviado éxitosamente")
