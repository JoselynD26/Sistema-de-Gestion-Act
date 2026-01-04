"""
Test script to verify Resend email delivery
"""
import asyncio
from app.utils.email import send_email_template

async def test_resend():
    print("=" * 60)
    print("TESTING RESEND EMAIL DELIVERY")
    print("=" * 60)
    
    test_email = "jmr.dicao@yavirac.edu.ec"
    
    print(f"\n📧 Sending test email to: {test_email}")
    
    success = send_email_template(
        subject="✅ Test Email from Resend API",
        recipients=[test_email],
        title="Prueba de Sistema",
        content_html="""
            <p>¡Hola!</p>
            <p>Si recibes este correo, significa que la migración a <strong>Resend API</strong> fue exitosa.</p>
            <p>✅ El sistema ahora usa Resend en lugar de SMTP tradicional.</p>
            <p>✅ Los emails deberían llegar más rápido y ser más confiables.</p>
            <p>✅ No más problemas de configuración SMTP.</p>
        """
    )
    
    if success:
        print("\n✅ Email enviado exitosamente!")
        print(f"📬 Revisa tu bandeja de entrada: {test_email}")
    else:
        print("\n❌ Error al enviar email")
        print("Revisa los logs arriba para más detalles")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_resend())
