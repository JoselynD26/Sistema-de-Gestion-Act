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
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=None  # Podríamos usar Jinja2 directamente o configurar una carpeta
)

fastmail = FastMail(conf)

async def send_email_template(subject: str, recipients: List[EmailStr], title: str, content_html: str, footer_text: str = "Sistema de Gestión Académica - Yavirac"):
    """Función base para enviar correos con un diseño premium."""
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
                <p>Este es un correo automático, por favor no lo respondas.</p>
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
    
    print(f"DEBUG EMAIL: Enviando correo '{subject}' a {recipients}...")
    await fastmail.send_message(message)
    print(f"DEBUG EMAIL: Correo '{subject}' enviado correctamente.")

def fecha_actual():
    from datetime import datetime
    return datetime.now().year

async def send_admin_notification(reserva_id: int, docente_nombre: str, aula_nombre: str, fecha: str, hora: str):
    """Notifica al admin sobre una nueva solicitud de reserva con diseño premium."""
    content = f"""
        <p>Hola <strong>Administrador</strong>,</p>
        <p>Se ha recibido una nueva solicitud de reserva que requiere su revisión técnica y administrativa.</p>
        <table class="info-table">
            <tr><td class="label">Docente</td><td>{docente_nombre}</td></tr>
            <tr><td class="label">Aula</td><td>{aula_nombre}</td></tr>
            <tr><td class="label">Fecha</td><td>{fecha}</td></tr>
            <tr><td class="label">Horario</td><td>{hora}</td></tr>
            <tr><td class="label">Estado</td><td><span class="status-badge status-pendiente">Pendiente</span></td></tr>
        </table>
        <p>Por favor, ingrese al panel de administración para gestionar esta solicitud.</p>
        <div style="text-align: center;">
            <a href="https://sistemagestionyavirac.netlify.app/" class="button">Gestionar Reservas</a>
        </div>
    """
    await send_email_template(
        subject="🚀 Nueva Solicitud de Reserva Registrada",
        recipients=[ADMIN_EMAIL],
        title="Nueva Solicitud de Reserva",
        content_html=content
    )

async def send_status_update_email(email_docente: str, docente_nombre: str, aula_nombre: str, fecha: str, nuevo_estado: str):
    """Notifica al docente sobre el cambio de estado con diseño premium."""
    estado_class = "status-aprobada" if nuevo_estado.upper() == "APROBADA" else "status-rechazada"
    icon = "✅" if nuevo_estado.upper() == "APROBADA" else "❌"
    
    content = f"""
        <p>Estimado/a <strong>{docente_nombre}</strong>,</p>
        <p>Le informamos que se ha procesado su solicitud de reserva para el aula indicada abajo.</p>
        <table class="info-table">
            <tr><td class="label">Aula</td><td>{aula_nombre}</td></tr>
            <tr><td class="label">Fecha</td><td>{fecha}</td></tr>
            <tr><td class="label">Nuevo Estado</td><td><span class="status-badge {estado_class}">{nuevo_estado}</span></td></tr>
        </table>
        <p>Si tiene alguna pregunta, por favor contacte con el departamento de coordinación académica.</p>
    """
    await send_email_template(
        subject=f"{icon} Actualización de su Reserva: {nuevo_estado}",
        recipients=[email_docente],
        title="Actualización de Reserva",
        content_html=content
    )

async def send_cancellation_notification(reserva_id: int, docente_nombre: str, aula_nombre: str, fecha: str):
    """Notifica al admin que un docente ha cancelado su reserva."""
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
        subject="⚠️ Reserva Cancelada por un Docente",
        recipients=[ADMIN_EMAIL],
        title="Notificación de Cancelación",
        content_html=content
    )

async def send_verification_email_to_admins(admins: List[dict], solicitante_email: str, solicitante_nombres: str, code: str):
    """Envía el código de verificación personalizado a cada administrador."""
    for admin in admins:
        admin_email = admin.get("correo")
        admin_nombre = admin.get("nombres", "Administrador")
        
        content = f"""
            <p>Hola <strong>{admin_nombre}</strong>,</p>
            <p><strong>{solicitante_nombres}</strong> ({solicitante_email}) ha solicitado acceso administrativo al sistema.</p>
            <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; border: 1px solid #e9ecef;">
                <p style="margin: 0; color: #6c757d; font-size: 14px;">CÓDIGO DE VERIFICACIÓN</p>
                <h2 style="margin: 10px 0; color: #1e3c72; font-size: 32px; letter-spacing: 5px;">{code}</h2>
                <p style="margin: 0; color: #dc3545; font-size: 12px;">Este código expira en 10 minutos.</p>
            </div>
            <p>Solo comparte este código si reconoces y autorizas esta solicitud.</p>
        """
        
        await send_email_template(
            subject="🔐 Autorización de Nuevo Administrador",
            recipients=[admin_email],
            title="Autorización Requerida",
            content_html=content
        )
