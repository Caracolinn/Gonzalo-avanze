from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CargaCSVForm
from .models import CalificacionTributaria, Corredor
import pandas as pd
from decimal import Decimal, InvalidOperation

# --- VISTA PARA LA CARGA DIRECTA DE FACTORES ---
def carga_masiva_factores(request):
    if request.method == 'POST':
        form = CargaCSVForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_csv']
            corredor_id = form.cleaned_data['corredor']
            
            try:
                corredor = Corredor.objects.get(id=corredor_id)
                df = pd.read_csv(archivo, sep=';') # Asumimos que el CSV usa punto y coma

                registros_creados = 0
                registros_actualizados = 0

                for index, row in df.iterrows():
                    # Usamos update_or_create para actualizar si ya existe, o crear si es nuevo
                    calificacion, created = CalificacionTributaria.objects.update_or_create(
                        corredor=corredor,
                        instrumento=row['instrumento'],
                        fecha=row['fecha'],
                        defaults={
                            'secuencia': row.get('secuencia', 0),
                            'numero_dividendo': row.get('numero_dividendo', 0),
                            'tipo_sociedad': row.get('tipo_sociedad', 'A'),
                            'valor_historico': Decimal(row.get('valor_historico', '0.0')),
                            'instrumento_no_inscrito': bool(row.get('instrumento_no_inscrito', False)),
                            # Mapeo directo de factores desde el CSV al modelo
                            'factor_8': Decimal(row.get('factor_8', '0.0')),
                            'factor_9': Decimal(row.get('factor_9', '0.0')),
                            'factor_10': Decimal(row.get('factor_10', '0.0')),
                            'factor_11': Decimal(row.get('factor_11', '0.0')),
                            'factor_12': Decimal(row.get('factor_12', '0.0')),
                            'factor_13': Decimal(row.get('factor_13', '0.0')),
                            'factor_14': Decimal(row.get('factor_14', '0.0')),
                            'factor_15': Decimal(row.get('factor_15', '0.0')),
                            'factor_16': Decimal(row.get('factor_16', '0.0')),
                            'factor_17': Decimal(row.get('factor_17', '0.0')),
                            'factor_18': Decimal(row.get('factor_18', '0.0')),
                            'factor_19': Decimal(row.get('factor_19', '0.0')),
                            'factor_20': Decimal(row.get('factor_20', '0.0')),
                            'factor_21': Decimal(row.get('factor_21', '0.0')),
                            'factor_22': Decimal(row.get('factor_22', '0.0')),
                            'factor_23': Decimal(row.get('factor_23', '0.0')),
                            'factor_24': Decimal(row.get('factor_24', '0.0')),
                            'factor_25': Decimal(row.get('factor_25', '0.0')),
                            'factor_26': Decimal(row.get('factor_26', '0.0')),
                            'factor_27': Decimal(row.get('factor_27', '0.0')),
                            'factor_28': Decimal(row.get('factor_28', '0.0')),
                            'factor_29': Decimal(row.get('factor_29', '0.0')),
                            'factor_30': Decimal(row.get('factor_30', '0.0')),
                            'factor_31': Decimal(row.get('factor_31', '0.0')),
                            'factor_32': Decimal(row.get('factor_32', '0.0')),
                            'factor_33': Decimal(row.get('factor_33', '0.0')),
                            'factor_34': Decimal(row.get('factor_34', '0.0')),
                            'factor_35': Decimal(row.get('factor_35', '0.0')),
                            'factor_36': Decimal(row.get('factor_36', '0.0')),
                            'factor_37': Decimal(row.get('factor_37', '0.0')),
                        }
                    )
                    
                    if created:
                        registros_creados += 1
                    else:
                        registros_actualizados += 1

                messages.success(request, f'Archivo de factores procesado. Se crearon {registros_creados} y se actualizaron {registros_actualizados} registros.')
            
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo: {e}')
            
            return redirect('carga_masiva_factores')
    else:
        form = CargaCSVForm()
        
    return render(request, 'calificaciones/carga_masiva.html', {'form': form})

# --- VISTA PARA LA CARGA DE MONTOS CON CONVERSIÓN A FACTORES ---
def carga_masiva_montos(request):
    if request.method == 'POST':
        form = CargaCSVForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_csv']
            corredor_id = form.cleaned_data['corredor']
            
            try:
                corredor = Corredor.objects.get(id=corredor_id)
                df = pd.read_csv(archivo, sep=';')

                registros_creados = 0
                registros_actualizados = 0

                for index, row in df.iterrows():
                    # --- LÓGICA DE CONVERSIÓN DE MONTOS A FACTORES ---
                    suma_base = sum(Decimal(str(row.get(f'monto_{i}', '0.0')).replace(',', '.')) for i in range(8, 20))

                    factores_calculados = {}
                    if suma_base > 0:
                        for i in range(8, 38):
                            monto_actual = Decimal(str(row.get(f'monto_{i}', '0.0')).replace(',', '.'))
                            factores_calculados[f'factor_{i}'] = monto_actual / suma_base
                    else:
                        for i in range(8, 38):
                            factores_calculados[f'factor_{i}'] = Decimal('0.0')

                    # Creamos o actualizamos el registro con los factores ya calculados
                    calificacion, created = CalificacionTributaria.objects.update_or_create(
                        corredor=corredor,
                        instrumento=row['instrumento'],
                        fecha=row['fecha'],
                        defaults={
                            'secuencia': row.get('secuencia', 0),
                            'numero_dividendo': row.get('numero_dividendo', 0),
                            'tipo_sociedad': row.get('tipo_sociedad', 'A'),
                            'valor_historico': Decimal(row.get('valor_historico', '0.0')),
                            'instrumento_no_inscrito': bool(row.get('instrumento_no_inscrito', False)),
                            **factores_calculados
                        }
                    )
                    
                    if created:
                        registros_creados += 1
                    else:
                        registros_actualizados += 1

                messages.success(request, f'Archivo de montos procesado. Se crearon {registros_creados} y se actualizaron {registros_actualizados} registros.')
            
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo: {e}')
            
            return redirect('carga_masiva_montos')
    else:
        form = CargaCSVForm()
        
    return render(request, 'calificaciones/carga_masiva_montos.html', {'form': form})