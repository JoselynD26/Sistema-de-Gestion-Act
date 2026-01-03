import smtplib
import secrets
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("SMTP_FROM_EMAIL")
        self.from_name = os.getenv("SMTP_FROM_NAME", "Sistema Yavirac")
        
        # Almacén temporal de códigos de verificación (en producción usar Redis)
        self.verification_codes: Dict[str, dict] = {}
        # Rate limiting storage: email -> last_sent_timestamp
        self.last_sent: Dict[str, datetime] = {}
    
    def generate_verification_code(self, email: str) -> str:
        """Genera un código de verificación de 6 dígitos"""
        code = secrets.randbelow(900000) + 100000  # Genera número entre 100000-999999
        
        # Guardar código con expiración de 10 minutos
        self.verification_codes[email] = {
            "code": str(code),
            "expires_at": datetime.now() + timedelta(minutes=10),
            "attempts": 0
        }
        
        return str(code)
    
    def verify_code(self, email: str, code: str) -> bool:
        """Verifica si el código es válido"""
        if email not in self.verification_codes:
            return False
        
        stored_data = self.verification_codes[email]
        
        # Verificar si el código ha expirado
        if datetime.now() > stored_data["expires_at"]:
            del self.verification_codes[email]
            return False
        
        # Verificar intentos (máximo 3)
        if stored_data["attempts"] >= 3:
            del self.verification_codes[email]
            return False
        
        # Incrementar intentos
        stored_data["attempts"] += 1
        
        # Verificar código
        if stored_data["code"] == code:
            del self.verification_codes[email]  # Eliminar código usado
            return True
        
        return False
    
    def send_admin_verification_email(self, solicitante_email: str, solicitante_nombres: str) -> bool:
        """Envía email con código de verificación a administradores existentes"""
        try:
            from sqlalchemy.orm import Session
            from app.core.config import SessionLocal
            from app.models.usuario import Usuario
            
            # Obtener administradores existentes
            db = SessionLocal()
            try:
                admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
                if not admins:
                    print("No hay administradores registrados")
                    return False
                
                code = self.generate_verification_code(solicitante_email)
                
                # Enviar email a todos los administradores
                for admin in admins:
                    msg = MIMEMultipart()
                    msg['From'] = f"{self.from_name} <{self.from_email}>"
                    msg['To'] = admin.correo
                    msg['Subject'] = "Solicitud de Autorización - Nuevo Administrador Yavirac"
                    
                    # Cuerpo del email
                    body = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    </head>
                    <body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 40px 0; text-align: center;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1px;">YAVIRAC</h1>
                                    <p style="color: #94A3B8; margin: 5px 0 0 0; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;">Gestión Académica</p>
                                </td>
                            </tr>
                            
                            <!-- Content -->
                            <tr>
                                <td style="padding: 40px 30px;">
                                    <h2 style="color: #1E293B; margin: 0 0 20px 0; font-size: 24px; font-weight: 600;">Autorización Requerida</h2>
                                    
                                    <p style="color: #475569; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                                        Hola <strong>{admin.nombres}</strong>,<br><br>
                                        <strong>{solicitante_nombres}</strong> ({solicitante_email}) ha solicitado acceso administrativo al sistema.
                                    </p>
                                    
                                    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 25px; text-align: center; margin: 30px 0;">
                                        <p style="margin: 0 0 10px 0; color: #64748B; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Código de Verificación</p>
                                        <div style="color: #0F172A; font-size: 38px; font-weight: 700; letter-spacing: 6px; font-family: monospace;">{code}</div>
                                        <p style="margin: 10px 0 0 0; color: #EF4444; font-size: 13px;">Expira en 10 minutos</p>
                                    </div>
                                    
                                    <div style="background-color: #FFF7ED; border-left: 4px solid #F97316; padding: 15px; border-radius: 4px;">
                                        <p style="margin: 0; color: #C2410C; font-size: 14px; line-height: 1.5;">
                                            <strong>Seguridad:</strong> Solo comparte este código si reconoces y autorizas esta solicitud.
                                        </p>
                                    </div>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #F1F5F9; padding: 20px; text-align: center; border-top: 1px solid #E2E8F0;">
                                    <p style="margin: 0; color: #64748B; font-size: 12px;">
                                        &copy; {datetime.now().year} Instituto Tecnológico Yavirac<br>
                                        Sistema de Gestión Académica Seguro
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </body>
                    </html>
                    """
                    
                    msg.attach(MIMEText(body, 'html'))
                    
                    # Enviar email
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
                    server.quit()
                
                print(f"Código de autorización {code} enviado a {len(admins)} administradores para solicitud de {solicitante_email}")
                return True
                
            finally:
                db.close()
            
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False

    def send_password_recovery_email(self, email: str, temp_password: str, nombres: str) -> bool:
        """Envía email con contraseña temporal para recuperación"""
        try:
            # Rate Limiting: Ignorar envíos si pasó menos de 30 seg desde el último
            if email in self.last_sent:
                last_time = self.last_sent[email]
                if datetime.now() - last_time < timedelta(seconds=30):
                    print(f"Rate Limit: Ignorando envío duplicado a {email} hace menos de 30s")
                    return True  # Retornamos True para que el usuario crea que se envió (evita spam)

            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = email
            msg['Subject'] = "Recuperación de Contraseña - Yavirac"
            
            body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 40px 0; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1px;">YAVIRAC</h1>
                            <p style="color: #94A3B8; margin: 5px 0 0 0; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;">Recuperación de Cuenta</p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #1E293B; margin: 0 0 20px 0; font-size: 24px; font-weight: 600;">Contraseña Temporal</h2>
                            
                            <p style="color: #475569; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                                Hola <strong>{nombres}</strong>,<br><br>
                                Hemos recibido una solicitud para recuperar tu acceso. Tu contraseña ha sido reseteada temporalmente.
                            </p>
                            
                            <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; padding: 25px; text-align: center; margin: 30px 0;">
                                <p style="margin: 0 0 10px 0; color: #15803D; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Tu Nueva Contraseña</p>
                                <div style="color: #166534; font-size: 32px; font-weight: 700; letter-spacing: 2px; font-family: monospace;">{temp_password}</div>
                            </div>
                            
                            <p style="color: #475569; font-size: 14px; line-height: 1.6; margin-bottom: 0;">
                                <strong>Siguientes pasos:</strong><br>
                                1. Ingresa al sistema con esta contraseña.<br>
                                2. Ve a tu perfil y cambia la contraseña por una segura.<br>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #F1F5F9; padding: 20px; text-align: center; border-top: 1px solid #E2E8F0;">
                            <p style="margin: 0; color: #64748B; font-size: 12px;">
                                &copy; {datetime.now().year} Instituto Tecnológico Yavirac<br>
                                Si no solicitaste esto, contacta a soporte inmediatamente.
                            </p>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            # Actualizar timestamp del último envío
            self.last_sent[email] = datetime.now()
            
            print(f"Email de recuperación enviado a {email}")
            return True
            
        except Exception as e:
            print(f"Error enviando email de recuperación: {e}")
            return False


# Instancia global del servicio
email_service = EmailService()