from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from app.core.config import (
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, 
    MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME, ADMIN_EMAIL
)
import os

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=465,  # Force port 465 for SSL/TLS (more reliable on Render)
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=False,  # Disable STARTTLS for port 465
    MAIL_SSL_TLS=True,    # Enable SSL/TLS for port 465
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=None
)

print(f"DEBUG EMAIL CONFIG: Server={MAIL_SERVER}:{MAIL_PORT}, User={MAIL_USERNAME}, From={MAIL_FROM}")

fastmail = FastMail(conf)

async def send_email_template(subject: str, recipients: List[EmailStr], title: str, content_html: str, footer_text: str = "Sistema de GestiÃ³n AcadÃ©mica - Yavirac"):
    """FunciÃ³n base para enviar correos con un diseÃ±o premium."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f7f9;
                margin: 0;
                padding: 0;
                color: #333;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                padding: 30px 20px;
                text-align: center;
                color: white;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
                letter-spacing: 1px;
            }}
            .content {{
                padding: 40px 30px;
                line-height: 1.6;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #777;
                border-top: 1px solid #eeeeee;
            }}
            .info-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 25px 0;
                background-color: #f9f9f9;
                border-radius: 8px;
            }}
            .info-table td {{
                padding: 12px 15px;
                border-bottom: 1px solid #f0f0f0;
            }}
            .info-table td.label {{
                font-weight: bold;
                color: #555;
                width: 30%;
            }}
            .status-badge {{
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
                text-transform: uppercase;
            }}
            .status-pendiente {{ background-color: #fff3cd; color: #856404; }}
            .status-aprobada {{ background-color: #d4edda; color: #155724; }}
            .status-rechazada {{ background-color: #f8d7da; color: #721c24; }}
            
            .button {{
                display: inline-block;
                padding: 12px 25px;
                background-color: #1e3c72;
                color: white !important;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{title}</h1>
            </div>
            <div class="content">
                {content_html}
            </div>
            <div class="footer">
                <p>&copy; {fecha_actual()} {footer_text}</p>
                <p>Este es un correo automÃ¡tico, por favor no lo respondas.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=html,
        subtype=MessageType.html
    )
    
    print(f"DEBUG EMAIL_UTILS: Preparando '{subject}' para {recipients}...")
    print(f"DEBUG EMAIL_UTILS_CONFIG: Server={MAIL_SERVER}:{MAIL_PORT}, User={MAIL_USERNAME}, From={MAIL_FROM}")
    try:
        await fastmail.send_message(message)
        print(f"DEBUG EMAIL_UTILS: '{subject}' enviado satisfactoriamente.")
    except Exception as e:
        print(f"DEBUG EMAIL ERROR: FallÃ³ el envÃ­o de '{subject}'. Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e

def fecha_actual():
    from datetime import datetime
    return datetime.now().year

async def send_admin_notification(admin_emails: List[str], reserva_id: int, docente_nombre: str, aula_nombre: str, fecha: str, hora: str):
    """Notifica a los administradores sobre una nueva solicitud de reserva con diseÃ±o premium."""
    content = f"""
        <p>Hola <strong>Administrador</strong>,</p>
        <p>Se ha recibido una nueva solicitud de reserva que requiere su revisiÃ³n tÃ©cnica y administrativa.</p>
        <table class="info-table">
            <tr><td class="label">Docente</td><td>{docente_nombre}</td></tr>
            <tr><td class="label">Aula</td><td>{aula_nombre}</td></tr>
            <tr><td class="label">Fecha</td><td>{fecha}</td></tr>
            <tr><td class="label">Horario</td><td>{hora}</td></tr>
            <tr><td class="label">Estado</td><td><span class="status-badge status-pendiente">Pendiente</span></td></tr>
        </table>
        <p>Por favor, ingrese al panel de administraciÃ³n para gestionar esta solicitud.</p>
        <div style="text-align: center;">
            <a href="https://sistemagestionyavirac.netlify.app/" class="button">Gestionar Reservas</a>
        </div>
    """
    await send_email_template(
        subject="ðŸš€ Nueva Solicitud de Reserva Registrada",
        recipients=admin_emails,
        title="Nueva Solicitud de Reserva",
        content_html=content
    )

async def send_status_update_email(email_docente: str, docente_nombre: str, aula_nombre: str, fecha: str, nuevo_estado: str):
    """Notifica al docente sobre el cambio de estado con diseÃ±o premium."""
    estado_class = "status-aprobada" if nuevo_estado.upper() == "APROBADA" else "status-rechazada"
    icon = "âœ…" if nuevo_estado.upper() == "APROBADA" else "âŒ"
    
    content = f"""
        <p>Estimado/a <strong>{docente_nombre}</strong>,</p>
        <p>Le informamos que se ha procesado su solicitud de reserva para el aula indicada abajo.</p>
        <table class="info-table">
            <tr><td class="label">Aula</td><td>{aula_nombre}</td></tr>
            <tr><td class="label">Fecha</td><td>{fecha}</td></tr>
            <tr><td class="label">Nuevo Estado</td><td><span class="status-badge {estado_class}">{nuevo_estado}</span></td></tr>
        </table>
        <p>Si tiene alguna pregunta, por favor contacte con el departamento de coordinaciÃ³n acadÃ©mica.</p>
    """
    await send_email_template(
        subject=f"{icon} ActualizaciÃ³n de su Reserva: {nuevo_estado}",
        recipients=[email_docente],
        title="ActualizaciÃ³n de Reserva",
        content_html=content
    )

async def send_cancellation_notification(admin_emails: List[str], reserva_id: int, docente_nombre: str, aula_nombre: str, fecha: str):
    """Notifica a los administradores que un docente ha cancelado su reserva."""
    content = f"""
        <p>Hola <strong>Administrador</strong>,</p>
        <p>Le informamos que un docente ha <strong>CANCELADO</strong> una solicitud de reserva previa.</p>
        <table class="info-table">
            <tr><td class="label">Docente</td><td>{docente_nombre}</td></tr>
            <tr><td class="label">Aula</td><td>{aula_nombre}</td></tr>
            <tr><td class="label">Fecha</td><td>{fecha}</td></tr>
            <tr><td class="label">Estado</td><td><span class="status-badge status-rechazada">Cancelada</span></td></tr>
        </table>
        <p>El espacio correspondiente ahora se encuentra nuevamente disponible para otros docentes.</p>
    """
    await send_email_template(
        subject="âš ï¸ Reserva Cancelada por un Docente",
        recipients=admin_emails,
        title="NotificaciÃ³n de CancelaciÃ³n",
        content_html=content
    )

async def send_verification_email_to_admins(admins: List[dict], solicitante_email: str, solicitante_nombres: str, code: str):
    """EnvÃ­a el cÃ³digo de verificaciÃ³n personalizado a cada administrador."""
    for admin in admins:
        admin_email = admin.get("correo")
        admin_nombre = admin.get("nombres", "Administrador")
        
        content = f"""
            <p>Hola <strong>{admin_nombre}</strong>,</p>
            <p><strong>{solicitante_nombres}</strong> ({solicitante_email}) ha solicitado acceso administrativo al sistema.</p>
            <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; border: 1px solid #e9ecef;">
                <p style="margin: 0; color: #6c757d; font-size: 14px;">CÃ“DIGO DE VERIFICACIÃ“N</p>
                <h2 style="margin: 10px 0; color: #1e3c72; font-size: 32px; letter-spacing: 5px;">{code}</h2>
                <p style="margin: 0; color: #dc3545; font-size: 12px;">Este cÃ³digo expira en 10 minutos.</p>
            </div>
            <p>Solo comparte este cÃ³digo si reconoces y autorizas esta solicitud.</p>
        """
        
        await send_email_template(
            subject="ðŸ” AutorizaciÃ³n de Nuevo Administrador",
            recipients=[admin_email],
            title="AutorizaciÃ³n Requerida",
            content_html=content
        )

