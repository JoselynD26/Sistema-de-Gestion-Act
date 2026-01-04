# Email service using Resend
import random
import string
from datetime import datetime, timedelta
from app.utils.email import send_email_template, send_admin_verification_codes

class EmailService:
    def __init__(self):
        self.verification_codes = {}
    
    def generate_verification_code(self):
        return ''.join(random.choices(string.digits, k=6))
    
    def send_admin_verification_email(self, solicitante_email, solicitante_nombres):
        from app.models.usuario import Usuario
        from app.core.config import SessionLocal
        db = SessionLocal()
        try:
            admins = db.query(Usuario).filter(Usuario.rol == "admin").all()
            if not admins:
                return False
            code = self.generate_verification_code()
            expires = datetime.now() + timedelta(seconds=90)  # 1.5 minutos
            self.verification_codes[solicitante_email] = {"code": code, "expires": expires}
            admin_list = [{"correo": admin.correo, "nombres": admin.nombres or "Administrador"} for admin in admins]
            send_admin_verification_codes(admin_list, solicitante_email, solicitante_nombres, code)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            db.close()
    
    def verify_code(self, email, code):
        if email not in self.verification_codes:
            return False
        stored = self.verification_codes[email]
        if datetime.now() > stored["expires"]:
            del self.verification_codes[email]
            return False
        if stored["code"] != code:
            return False
        del self.verification_codes[email]
        return True
    
    def send_password_recovery_email(self, email, temp_password, nombre):
        content = f"<p>Hola <strong>{nombre}</strong>,</p><p>Tu nueva contrasena temporal es: <strong>{temp_password}</strong></p>"
        return send_email_template(subject="Recuperacion de Contrasena", recipients=[email], title="Recuperacion", content_html=content)

email_service = EmailService()
