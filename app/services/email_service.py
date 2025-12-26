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
                    <html>
                    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <div style="background: linear-gradient(135deg, #1E3A8A, #FF6B35); padding: 20px; text-align: center;">
                            <h1 style="color: white; margin: 0;">🎓 YAVIRAC</h1>
                            <p style="color: white; margin: 5px 0;">Sistema de Gestión Académica</p>
                        </div>
                        
                        <div style="padding: 30px; background: #f9f9f9;">
                            <h2 style="color: #1E3A8A;">Hola {admin.nombres} te damos la bienvenida al Sistema de Gestión Académica Yavirac,</h2>
                            
                            <p><strong>{solicitante_nombres}</strong> ({solicitante_email}) ha solicitado crear una cuenta de <strong>Administrador</strong> en el sistema.</p>
                            
                            <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                                <p style="margin: 0; color: #666;">Código de autorización:</p>
                                <h1 style="color: #FF6B35; font-size: 36px; margin: 10px 0; letter-spacing: 5px;">{code}</h1>
                                <p style="margin: 0; color: #666; font-size: 14px;">Este código expira en 10 minutos</p>
                            </div>
                            
                            <p style="color: #666;">
                                <strong>⚠️ Instrucciones:</strong><br>
                                • Si autorizas esta solicitud, proporciona este código al solicitante<br>
                                • Si no conoces al solicitante, NO compartas este código<br>
                                • Cada código solo puede usarse una vez
                            </p>
                            
                            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                            
                            <p style="color: #999; font-size: 12px; text-align: center;">
                                Este es un email automático del Sistema de Gestión Académica Yavirac<br>
                                Desarrollado por: Joselyn Dicao, María Ortiz y Raul Hidalgo
                            </p>
                        </div>
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

# Instancia global del servicio
email_service = EmailService()