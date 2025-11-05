# calificaciones/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User # <-- ¡NUEVA IMPORTACIÓN!

# --- MODELO PARA LOS CORREDORES (ACTUALIZADO) ---
class Corredor(models.Model):
    # --- ¡NUEVO CAMPO DE VÍNCULO! ---
    usuario = models.OneToOneField(
        User,
        on_delete=models.SET_NULL, # Si borras el Usuario, el Corredor no se borra
        null=True,
        blank=True,
        verbose_name="Usuario Django Vinculado"
    )
    
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Corredor")
    codigo_corredor = models.CharField(max_length=10, unique=True, verbose_name="Código")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Corredor"
        verbose_name_plural = "Corredores"


# --- MODELO PRINCIPAL PARA LAS CALIFICACIONES (COMPLETO) ---
class CalificacionTributaria(models.Model):
    
    # --- Opciones para los nuevos campos ---
    TIPO_MERCADO_CHOICES = [
        ('ACC', 'Acciones'),
        ('CFI', 'CFI'),
        ('FFM', 'Fondos Mutuos'),
    ]
    ORIGEN_CHOICES = [
        ('COR', 'Corredora'),
        ('SIS', 'Sistema'),
    ]
    FUENTE_CHOICES = [
        ('MAN', 'Ingreso Manual'),
        ('FAC', 'Carga Factores'),
        ('MON', 'Carga Montos'),
    ]

    # --- RELACIÓN CON CORREDOR ---
    corredor = models.ForeignKey(
        Corredor,
        on_delete=models.CASCADE,
        verbose_name="Corredor"
    )

    # --- DATOS DE IDENTIFICACIÓN ---
    instrumento = models.CharField(
        max_length=50,
        verbose_name="Instrumento",
        help_text="Código del instrumento. Ej: ACN"
    )
    fecha = models.DateField(
        verbose_name="Fecha",
        help_text="Fecha en formato AAAA-MM-DD"
    )
    secuencia = models.IntegerField(
        verbose_name="Secuencia",
        help_text="Número de secuencia"
    )
    
    # --- CAMPOS DEL MANTENEDOR ---
    tipo_mercado = models.CharField(
        max_length=3,
        choices=TIPO_MERCADO_CHOICES,
        verbose_name="Tipo de Mercado",
        null=True, blank=True # Opcional
    )
    descripcion_dividendo = models.CharField(
        max_length=255,
        verbose_name="Descripción del Dividendo",
        null=True, blank=True
    )
    acogido_isfut = models.BooleanField(
        default=False,
        verbose_name="Acogido a Isfut/Isift"
    )
    origen = models.CharField(
        max_length=3,
        choices=ORIGEN_CHOICES,
        verbose_name="Origen",
        default='SIS' # Por defecto, 'Sistema'
    )
    factor_actualizacion = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        default=0.0,
        verbose_name="Factor de Actualización"
    )
    
    # --- CAMPOS DE AUDITORÍA ---
    fecha_modificacion = models.DateTimeField(
        auto_now=True, # Actualiza automáticamente la fecha cada vez que se guarda
        verbose_name="Última Modificación"
    )
    fuente_ingreso = models.CharField(
        max_length=3,
        choices=FUENTE_CHOICES,
        default='MAN', # Por defecto 'Ingreso Manual'
        verbose_name="Fuente de Ingreso"
    )

    numero_dividendo = models.IntegerField(
        verbose_name="Número de dividendo"
    )
    tipo_sociedad = models.CharField(
        max_length=1,
        choices=[('A', 'Abierta'), ('C', 'Cerrada')],
        verbose_name="Tipo Sociedad"
    )
    valor_historico = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        verbose_name="Valor Histórico"
    )
    instrumento_no_inscrito = models.BooleanField(
        default=False,
        verbose_name="Instrumento No Inscrito"
    )

    # --- CAMPOS DE FACTORES (TODOS) ---
    validator_factor = [MinValueValidator(0), MaxValueValidator(1)]
    factor_8 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_9 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_10 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_11 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_12 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_13 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_14 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_15 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_16 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_17 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_18 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_19 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_20 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_21 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_22 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_23 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_24 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_25 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_26 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_27 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_28 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_29 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_30 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_31 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_32 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_33 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_34 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_35 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_36 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)
    factor_37 = models.DecimalField(max_digits=9, decimal_places=8, default=0.0, validators=validator_factor)

    # --- LÓGICA DE VALIDACIÓN ---
    def clean(self):
        super().clean()
        suma_factores = (
            self.factor_8 + self.factor_9 + self.factor_10 + self.factor_11 +
            self.factor_12 + self.factor_13 + self.factor_14 + self.factor_15 +
            self.factor_16 + self.factor_17 + self.factor_18 + self.factor_19
        )
        if suma_factores > 1:
            raise ValidationError(
                'Error: La suma de los factores del 8 al 19 no puede ser mayor que 1.'
            )

    def __str__(self):
        return f"{self.instrumento} ({self.corredor.nombre}) - {self.fecha}"

    class Meta:
        verbose_name = "Calificación Tributaria"
        verbose_name_plural = "Calificaciones Tributarias"
        ordering = ['-fecha', 'instrumento']