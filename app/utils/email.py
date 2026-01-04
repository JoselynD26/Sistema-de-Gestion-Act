"""
Email utilities using Resend API - Simple, reliable, and modern
"""
import os
import resend
from typing import List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Resend configuration from environment
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
RESEND_FROM_NAME = os.getenv("RESEND_FROM_NAME", "Sistema Yavirac")

# Initialize Resend
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
    print(f"DEBUG EMAIL CONFIG: Using Resend API with from={RESEND_FROM_EMAIL}")
else:
    print("WARNING: RESEND_API_KEY not found in environment variables!")


def send_email_template(subject: str, recipients: List[str], title: str, content_html: str, footer_text: str = "Sistema de Gestión Académica - Yavirac"):
    """Función base para enviar correos con un diseño premium usando Resend."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                color: #2d3748;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            .header::before {{
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: pulse 3s ease-in-out infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); opacity: 0.5; }}
                50% {{ transform: scale(1.1); opacity: 0.8; }}
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: -0.5px;
                color: white;
                text-shadow: 0 2px 10px rgba(0,0,0,0.2);
                position: relative;
                z-index: 1;
            }}
            .logo {{
                width: 60px;
                height: 60px;
                margin: 0 auto 15px;
                background: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 30px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                position: relative;
                z-index: 1;
            }}
            .content {{
                padding: 45px 35px;
                line-height: 1.8;
                font-size: 15px;
            }}
            .content p {{
                margin: 0 0 15px 0;
                color: #4a5568;
            }}
            .content strong {{
                color: #2d3748;
                font-weight: 600;
            }}
            .footer {{
                background: linear-gradient(to bottom, #f7fafc 0%, #edf2f7 100%);
                padding: 25px;
                text-align: center;
                font-size: 13px;
                color: #718096;
                border-top: 1px solid #e2e8f0;
            }}
            .footer p {{
                margin: 5px 0;
            }}
            .info-table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin: 25px 0;
                background: linear-gradient(to bottom, #f7fafc 0%, #ffffff 100%);
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}
            .info-table td {{
                padding: 16px 20px;
                border-bottom: 1px solid #e2e8f0;
            }}
            .info-table tr:last-child td {{
                border-bottom: none;
            }}
            .info-table td.label {{
                font-weight: 600;
                color: #4a5568;
                width: 35%;
                font-size: 14px;
            }}
            .info-table td:last-child {{
                color: #2d3748;
                font-weight: 500;
            }}
            .status-badge {{
                display: inline-block;
                padding: 8px 16px;
                border-radius: 25px;
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .status-pendiente {{ 
                background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
                color: #78350f;
            }}
            .status-aprobada {{ 
                background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
                color: #064e3b;
            }}
            .status-rechazada {{ 
                background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
                color: #7f1d1d;
            }}
            .button {{
                display: inline-block;
                padding: 14px 32px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white !important;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin-top: 20px;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                transition: all 0.3s ease;
                font-size: 15px;
                letter-spacing: 0.3px;
            }}
            .button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
            }}
            .code-box {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                padding: 25px;
                text-align: center;
                margin: 25px 0;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            }}
            .code-box p {{
                margin: 0 0 10px 0;
                color: rgba(255,255,255,0.9);
                font-size: 13px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .code-box h2 {{
                margin: 0;
                color: white;
                font-size: 36px;
                font-weight: 700;
                letter-spacing: 8px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            .code-box .expiry {{
                margin: 10px 0 0 0;
                color: rgba(255,255,255,0.8);
                font-size: 12px;
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
    
    print(f"DEBUG EMAIL: Preparando '{subject}' para {recipients}...")
    try:
        params = {
            "from": f"{RESEND_FROM_NAME} <{RESEND_FROM_EMAIL}>",
            "to": recipients,
            "subject": subject,
            "html": html
        }
        
        response = resend.Emails.send(params)
        print(f"DEBUG EMAIL: '{subject}' enviado satisfactoriamente. Response: {response}")
        return True
    except Exception as e:
        print(f"DEBUG EMAIL ERROR: Falló el envío de '{subject}'. Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def fecha_actual():
    return datetime.now().year

def send_admin_notification(admin_emails: List[str], reserva_id: int, docente_nombre: str, aula_nombre: str, fecha: str, hora: str):
    """Notifica a los administradores sobre una nueva solicitud de reserva con diseño premium."""
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
    return send_email_template(
        subject="🚀 Nueva Solicitud de Reserva Registrada",
        recipients=admin_emails,
        title="Nueva Solicitud de Reserva",
        content_html=content
    )

def send_status_update_email(email_docente: str, docente_nombre: str, aula_nombre: str, fecha: str, nuevo_estado: str):
    """Notifica al docente sobre el cambio de estado con diseño premium."""
    estado_class = "status-aprobada" if nuevo_estado.upper() == "APROBADA" else "status-rechazada"
    icon = "✅" if nuevo_estado.upper() == "APROBADA" else "❌"
    
    content = f"""
        <p>Estimado/a <strong>{docente_nombre}</strong>,</p>
        <p>Le informamos que el estado de su reserva ha sido actualizado:</p>
        <table class="info-table">
            <tr><td class="label">Aula</td><td>{aula_nombre}</td></tr>
            <tr><td class="label">Fecha</td><td>{fecha}</td></tr>
            <tr><td class="label">Nuevo Estado</td><td><span class="status-badge {estado_class}">{nuevo_estado}</span></td></tr>
        </table>
        <p>Si tiene alguna pregunta, por favor contacte con el departamento de coordinación académica.</p>
    """
    return send_email_template(
        subject=f"{icon} Actualización de su Reserva: {nuevo_estado}",
        recipients=[email_docente],
        title="Actualización de Reserva",
        content_html=content
    )

def send_cancellation_notification(admin_emails: List[str], reserva_id: int, docente_nombre: str, aula_nombre: str, fecha: str):
    """Notifica a los administradores sobre una cancelación de reserva."""
    content = f"""
        <p>Hola <strong>Administrador</strong>,</p>
        <p>Se ha <strong>cancelado</strong> una reserva previamente registrada:</p>
        <table class="info-table">
            <tr><td class="label">Docente</td><td>{docente_nombre}</td></tr>
            <tr><td class="label">Aula</td><td>{aula_nombre}</td></tr>
            <tr><td class="label">Fecha</td><td>{fecha}</td></tr>
            <tr><td class="label">Estado</td><td><span class="status-badge status-rechazada">Cancelada</span></td></tr>
        </table>
        <p>El espacio correspondiente ahora se encuentra nuevamente disponible para otros docentes.</p>
    """
    return send_email_template(
        subject="⚠️ Reserva Cancelada por un Docente",
        recipients=admin_emails,
        title="Notificación de Cancelación",
        content_html=content
    )

def send_admin_verification_codes(admins: List[dict], solicitante_email: str, solicitante_nombres: str, code: str):
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
        
        send_email_template(
            subject="🔐 Autorización de Nuevo Administrador",
            recipients=[admin_email],
            title="Autorización Requerida",
            content_html=content
        )
