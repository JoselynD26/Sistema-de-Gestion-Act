import secrets
import os
from datetime import datetime, timedelta
from typing import Dict
from app.core.config import SessionLocal
from app.models.usuario import Usuario
from app.utils.email import send_verification_email_to_admins, send_email_template


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
    
    async def send_admin_verification_email(self, solicitante_email: str, solicitante_nombres: str) -> bool:
        """Envía email con código de verificación a administradores existentes (Versión Async)"""
        print(f"DEBUG: Iniciando envio codigo admin a administradores para {solicitante_email}")
        try:
            # Obtener administradores existentes
            db = SessionLocal()
            try:
                admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
                if not admins:
                    print(f"DEBUG ALERT: No hay administradores registrados para autorizar a {solicitante_email}")
                    return False
                
                code = self.generate_verification_code(solicitante_email)
                admins_data = [{"correo": admin.correo, "nombres": admin.nombres} for admin in admins]
                
                print(f"DEBUG: Enviando codigo {code} a {len(admins_data)} administradores")
                # Enviar email usando el utilitario async (FastMail)
                await send_verification_email_to_admins(
                    admins=admins_data,
                    solicitante_email=solicitante_email,
                    solicitante_nombres=solicitante_nombres,
                    code=code
                )
                
                print(f"DEBUG: Email admin enviado exitosamente para {solicitante_email}")
                return True
                
            finally:
                db.close()
            
        except Exception as e:
            print(f"ERROR enviando email admin async: {e}")
            return False

    async def send_password_recovery_email(self, email: str, temp_password: str, nombres: str) -> bool:
        """Envía email con contraseña temporal para recuperación (Versión Async)"""
        print(f"DEBUG: Iniciando envio email recuperacion para {email}")
        try:
            # Rate Limiting: Ignorar envíos si pasó menos de 30 seg desde el último
            if email in self.last_sent:
                last_time = self.last_sent[email]
                if datetime.now() - last_time < timedelta(seconds=30):
                    print(f"DEBUG: Rate Limit activo para {email}")
                    return True

            content = f"""
                <p>Hola <strong>{nombres}</strong>,</p>
                <p>Hemos recibido una solicitud para recuperar tu acceso. Tu contraseña ha sido reseteada temporalmente.</p>
                <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 25px; text-align: center; margin: 25px 0;">
                    <p style="margin: 0 0 10px 0; color: #15803d; font-size: 13px; text-transform: uppercase; font-weight: 600;">Tu Nueva Contraseña</p>
                    <div style="color: #166534; font-size: 32px; font-weight: 700; letter-spacing: 2px; font-family: monospace;">{temp_password}</div>
                </div>
                <p><strong>Pasos a seguir:</strong><br>
                1. Ingresa al sistema con esta contraseña.<br>
                2. Cambia tu contraseña en tu perfil por una personalizada.<br>
                </p>
            """
            
            await send_email_template(
                subject="🔑 Recuperación de Contraseña - Yavirac",
                recipients=[email],
                title="Recuperación de Cuenta",
                content_html=content
            )
            
            self.last_sent[email] = datetime.now()
            print(f"DEBUG: Email recuperacion enviado exitosamente a {email}")
            return True
            
        except Exception as e:
            print(f"ERROR enviando email recovery async: {e}")
            return False


# Instancia global del servicio
email_service = EmailService()