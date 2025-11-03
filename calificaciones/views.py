# calificaciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.forms.models import model_to_dict
# Importamos TODOS los formularios
from .forms import CargaCSVForm, FiltroCalificacionesForm, IngresoBasicoForm, IngresoMontosForm, IngresoFactoresForm
from .models import CalificacionTributaria, Corredor
import pandas as pd
from decimal import Decimal, InvalidOperation

# --- VISTA 1: CARGA MASIVA DE FACTORES (Sin cambios) ---
def carga_masiva_factores(request):
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
                            'fuente_ingreso': 'FAC',
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
                    if created: registros_creados += 1
                    else: registros_actualizados += 1
                messages.success(request, f'Archivo de factores procesado. Se crearon {registros_creados} y se actualizaron {registros_actualizados} registros.')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo: {e}')
            return redirect('carga_masiva_factores')
    else:
        form = CargaCSVForm()
    return render(request, 'calificaciones/carga_masiva.html', {'form': form})


# --- VISTA 2: CARGA MASIVA DE MONTOS (Sin cambios) ---
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
                    suma_base = sum(Decimal(str(row.get(f'monto_{i}', '0.0')).replace(',', '.')) for i in range(8, 20))
                    factores_calculados = {}
                    if suma_base > 0:
                        for i in range(8, 38):
                            monto_actual = Decimal(str(row.get(f'monto_{i}', '0.0')).replace(',', '.'))
                            factores_calculados[f'factor_{i}'] = monto_actual / suma_base
                    else:
                        for i in range(8, 38):
                            factores_calculados[f'factor_{i}'] = Decimal('0.0')
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
                            'fuente_ingreso': 'MON',
                            **factores_calculados
                        }
                    )
                    if created: registros_creados += 1
                    else: registros_actualizados += 1
                messages.success(request, f'Archivo de montos procesado. Se crearon {registros_creados} y se actualizaron {registros_actualizados} registros.')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo: {e}')
            return redirect('carga_masiva_montos')
    else:
        form = CargaCSVForm()
    return render(request, 'calificaciones/carga_masiva_montos.html', {'form': form})


# --- VISTA 3: MANTENEDOR PRINCIPAL (MODIFICADA) ---
def mantenedor_calificaciones(request):
    calificaciones = CalificacionTributaria.objects.all().order_by('-fecha')
    filtro_form = FiltroCalificacionesForm(request.GET)
    if filtro_form.is_valid():
        tipo_mercado = filtro_form.cleaned_data.get('tipo_mercado')
        origen = filtro_form.cleaned_data.get('origen')
        periodo_comercial = filtro_form.cleaned_data.get('periodo_comercial')
        if tipo_mercado: calificaciones = calificaciones.filter(tipo_mercado=tipo_mercado)
        if origen: calificaciones = calificaciones.filter(origen=origen)
        if periodo_comercial: calificaciones = calificaciones.filter(fecha__year=periodo_comercial)
    
    # Pasamos los 3 formularios vacíos
    ingreso_form = IngresoBasicoForm() 
    montos_form = IngresoMontosForm() 
    factores_form = IngresoFactoresForm() # --- NUEVA LÍNEA ---

    context = {
        'form': filtro_form,
        'ingreso_form': ingreso_form, 
        'montos_form': montos_form, 
        'factores_form': factores_form, # --- NUEVA LÍNEA ---
        'calificaciones': calificaciones
    }
    return render(request, 'calificaciones/mantenedor.html', context)


# --- VISTA 4: INGRESAR (Paso 1) (Sin cambios) ---
def ingresar_calificacion(request):
    if request.method == 'POST':
        form = IngresoBasicoForm(request.POST)
        if form.is_valid():
            corredor = Corredor.objects.first() # Temporal
            nueva_calificacion = form.save(commit=False)
            nueva_calificacion.corredor = corredor
            nueva_calificacion.fuente_ingreso = 'MAN'
            nueva_calificacion.save()
            return JsonResponse({'success': True, 'calificacion_id': nueva_calificacion.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- VISTA 5: CALCULAR MONTOS (Paso 2) (MODIFICADA) ---
def ingresar_montos(request, calificacion_id):
    # Ya no necesitamos 'calificacion' aquí, solo calculamos
    if request.method == 'POST':
        form = IngresoMontosForm(request.POST)
        
        if form.is_valid():
            try:
                montos = form.cleaned_data
                suma_base = sum(montos.get(f'monto_{i}', Decimal('0.0')) for i in range(8, 20))

                factores_calculados = {}
                if suma_base > 0:
                    for i in range(8, 38):
                        monto_actual = montos.get(f'monto_{i}', Decimal('0.0'))
                        factores_calculados[f'factor_{i}'] = monto_actual / suma_base
                else:
                    for i in range(8, 38):
                        factores_calculados[f'factor_{i}'] = Decimal('0.0')
                
                # NO GUARDAMOS. Solo devolvemos los factores calculados
                return JsonResponse({
                    'success': True,
                    'calificacion_id': calificacion_id,
                    'factores': {k: f"{v:.8f}" for k, v in factores_calculados.items()}
                })

            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- VISTA 6: ELIMINAR (Sin cambios) ---
def eliminar_calificacion(request, calificacion_id):
    if request.method == 'POST':
        try:
            calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id)
            instrumento_nombre = calificacion.instrumento
            calificacion.delete()
            return JsonResponse({'success': True, 'message': f'Registro para {instrumento_nombre} eliminado exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


# --- VISTA 7: OBTENER DATOS (Sin cambios) ---
def obtener_calificacion_json(request, calificacion_id):
    if request.method == 'GET':
        try:
            calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id)
            data = model_to_dict(calificacion)
            data['fecha'] = calificacion.fecha.strftime('%Y-%m-%d')
            return JsonResponse({'success': True, 'data': data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


# --- VISTA 8: MODIFICAR (Paso 1) (Sin cambios) ---
def modificar_calificacion(request, calificacion_id):
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id)
    if request.method == 'POST':
        form = IngresoBasicoForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save() 
            return JsonResponse({'success': True, 'calificacion_id': calificacion.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- ¡NUEVA VISTA 9! GUARDAR FACTORES (Paso 3) ---
def guardar_factores(request, calificacion_id):
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id)
    if request.method == 'POST':
        form = IngresoFactoresForm(request.POST)
        if form.is_valid():
            try:
                # Validamos la suma de factores (8-19)
                suma_factores_validacion = sum(form.cleaned_data.get(f'factor_{i}', Decimal('0.0')) for i in range(8, 20))
                if suma_factores_validacion > 1:
                    return JsonResponse({'success': False, 'errors': 'Error: La suma de los factores del 8 al 19 no puede ser mayor que 1.'})

                # Guardamos CADA factor en el objeto
                for i in range(8, 38):
                    setattr(calificacion, f'factor_{i}', form.cleaned_data[f'factor_{i}'])
                
                calificacion.save() # Guardamos todos los cambios
                return JsonResponse({'success': True, 'message': 'Calificación guardada exitosamente.'})

            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})