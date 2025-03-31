from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
import markdown2
from rest_framework.authtoken.models import Token
from django.conf import settings

def send_markdown_email(subject, markdown_content, to_email):
    """
    Envía un correo electrónico con contenido en Markdown.
    El Markdown se convierte a HTML para clientes de correo que soportan HTML.
    """
    # Convertir Markdown a HTML
    html_content = markdown2.markdown(
        markdown_content,
        extras=["fenced-code-blocks", "tables", "header-ids", "break-on-newline"]
    )
    
    # Crear el correo con ambas versiones (texto plano y HTML)
    from_email = settings.DEFAULT_FROM_EMAIL
    email = EmailMultiAlternatives(subject, markdown_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Envía un correo de bienvenida cuando se crea un nuevo usuario.
    """
    if created:
        subject = '¡Bienvenido a LumWallet! 🎉'
        
        # Contenido en Markdown
        content = f"""
# ¡Bienvenido a LumWallet, {instance.first_name}! 🎉

¡Nos alegra que te hayas unido a nuestra comunidad! ✨

Con LumWallet, podrás:

* **Gestionar tus finanzas** de manera sencilla 💼
* **Realizar seguimiento** de tus gastos e ingresos 📊
* **Establecer metas** financieras y alcanzarlas 🎯
* **Recibir notificaciones** personalizadas 🔔

Para comenzar, [accede a tu panel de control](https://lumwallet.lumace.cloud) y completa tu perfil.

Si tienes alguna duda sobre cómo comenzar, puedes consultar nuestra [guía para nuevos usuarios](https://lumwallet.lumace.cloud/help).

¡Estamos emocionados de tenerte a bordo!

Saludos cordiales,  
El equipo de LumWallet 💙
        """
        
        # Enviar el correo
        send_markdown_email(subject, content, instance.email)

# Crear un token para el nuevo usuario
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def notify_account_changes(sender, instance, created, **kwargs):
    """
    Notifica al usuario cuando se realizan cambios en su cuenta.
    """
    # No enviamos para usuarios nuevos
    if not created:
        # En una implementación real, deberías comprobar qué campos han cambiado
        # Esta es una implementación simplificada
        
        subject = 'Cambios en tu cuenta LumWallet 🔄'
        
        # Contenido en Markdown
        content = f"""
## Actualización en tu cuenta 🔄

Hola {instance.first_name},

Te informamos que se han realizado cambios en tu cuenta de LumWallet.

### Detalles de los cambios: 📝

* **Datos personales**: Se actualizaron tus datos personales
* **Fecha del cambio**: {timezone.now().strftime('%d-%m-%Y %H:%M')}

Si no has realizado estos cambios o detectas algo sospechoso, por favor contacta inmediatamente con nuestro [equipo de soporte](https://lumwallet.lumace.cloud/support).

La seguridad de tu cuenta es nuestra prioridad. Te recomendamos revisar regularmente tu configuración de seguridad.

Atentamente,  
Equipo de Seguridad de LumWallet 🔒
        """
        
        # Enviar el correo
        send_markdown_email(subject, content, instance.email)

@receiver(post_delete, sender=User)
def notify_account_deactivation(sender, instance, **kwargs):
    """
    Notifica al usuario cuando su cuenta ha sido desactivada.
    """
    # Verificamos si el usuario ha sido desactivado
    if not instance.is_active:
        subject = 'Tu cuenta LumWallet ha sido desactivada 🔚'
        
        # Contenido en Markdown
        content = f"""
## Tu cuenta ha sido desactivada 🔚

Hola {instance.username},

Hemos procesado tu solicitud para desactivar tu cuenta en LumWallet.

### Información importante: ℹ️

* Tu cuenta ha sido desactivada el **{timezone.now().strftime('%d-%m-%Y %H:%M')}**
* Tus datos personales serán retenidos durante **30 días** antes de ser eliminados permanentemente
* Durante este período, puedes reactivar tu cuenta en cualquier momento

Lamentamos que hayas decidido dejarnos. Nos encantaría saber tu opinión sobre cómo podríamos mejorar nuestros servicios: [compartir opinión](https://lumwallet.com/feedback).

Si has desactivado tu cuenta por error o deseas reactivarla, simplemente [haz clic aquí para reactivarla](https://lumwallet.com/reactivate?user_id={instance.id}).

Gracias por haber sido parte de LumWallet. Esperamos verte de nuevo pronto.

Saludos,  
El equipo de LumWallet 👋
        """
        
        # Enviar el correo
        send_markdown_email(subject, content, instance.email)