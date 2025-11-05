# calificaciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from .forms import CargaCSVForm, FiltroCalificacionesForm, IngresoBasicoForm, IngresoMontosForm, IngresoFactoresForm
from .models import CalificacionTributaria, Corredor
import pandas as pd
from decimal import Decimal, InvalidOperation

# --- Decorador de ayuda para verificar si el usuario es un corredor ---
def corredor_requerido(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'corredor'):
            # Si el usuario no está vinculado a un corredor, no puede hacer nada
            return HttpResponseForbidden("Acceso denegado. No está vinculado a un corredor.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# --- ¡VISTA CORREGIDA! PARA PREVISUALIZAR CSV ---
@corredor_requerido
def previsualizar_csv(request):
    if request.method == 'POST':
        # El form ahora solo tiene el archivo
        form = CargaCSVForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                archivo = request.FILES['archivo_csv']
                df = pd.read_csv(archivo, sep=';', nrows=5)
                
                if 'monto_8' in df.columns:
                    monto_cols_base = [f'monto_{i}' for i in range(8, 20) if f'monto_{i}' in df.columns]
                    df['suma_base'] = df[monto_cols_base].sum(axis=1) 
                    for i in range(8, 38):
                        col_monto = f'monto_{i}'
                        col_factor = f'factor_{i} (calc)'
                        if col_monto in df.columns:
                            df[col_factor] = df.apply(
                                lambda row, m=col_monto: (row[m] / row['suma_base']) if row['suma_base'] > 0 else 0, 
                                axis=1
                            ).round(8)
                    df = df.drop(columns=['suma_base'], errors='ignore')
                
                tabla_html = df.to_html(classes=['table', 'table-sm', 'table-bordered'], index=False)
                return JsonResponse({'success': True, 'tabla_html': tabla_html})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': f'Error al leer el archivo: {e}'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- VISTA 1: CARGA MASIVA DE FACTORES (ACTUALIZADA) ---
@corredor_requerido
def carga_masiva_factores(request):
    if request.method == 'POST':
        form = CargaCSVForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_csv']
            corredor = request.user.corredor # <-- ¡OBTENEMOS EL CORREDOR DEL USUARIO!
            try:
                df = pd.read_csv(archivo, sep=';') 
                registros_creados = 0
                registros_actualizados = 0
                for index, row in df.iterrows():
                    calificacion, created = CalificacionTributaria.objects.update_or_create(
                        corredor=corredor, # <-- Usamos el corredor del usuario
                        instrumento=row['instrumento'],
                        fecha=row['fecha'],
                        defaults={
                            'secuencia': row.get('secuencia', 0),
                            'numero_dividendo': row.get('numero_dividendo', 0),
                            'tipo_sociedad': row.get('tipo_sociedad', 'A'),
                            'valor_historico': Decimal(str(row.get('valor_historico', '0.0')).replace(',', '.')),
                            'instrumento_no_inscrito': bool(row.get('instrumento_no_inscrito', False)),
                            'fuente_ingreso': 'FAC',
                            'factor_8': Decimal(str(row.get('factor_8', '0.0')).replace(',', '.')),
                            'factor_9': Decimal(str(row.get('factor_9', '0.0')).replace(',', '.')),
                            'factor_10': Decimal(str(row.get('factor_10', '0.0')).replace(',', '.')),
                            'factor_11': Decimal(str(row.get('factor_11', '0.0')).replace(',', '.')),
                            'factor_12': Decimal(str(row.get('factor_12', '0.0')).replace(',', '.')),
                            'factor_13': Decimal(str(row.get('factor_13', '0.0')).replace(',', '.')),
                            'factor_14': Decimal(str(row.get('factor_14', '0.0')).replace(',', '.')),
                            'factor_15': Decimal(str(row.get('factor_15', '0.0')).replace(',', '.')),
                            'factor_16': Decimal(str(row.get('factor_16', '0.0')).replace(',', '.')),
                            'factor_17': Decimal(str(row.get('factor_17', '0.0')).replace(',', '.')),
                            'factor_18': Decimal(str(row.get('factor_18', '0.0')).replace(',', '.')),
                            'factor_19': Decimal(str(row.get('factor_19', '0.0')).replace(',', '.')),
                            'factor_20': Decimal(str(row.get('factor_20', '0.0')).replace(',', '.')),
                            'factor_21': Decimal(str(row.get('factor_21', '0.0')).replace(',', '.')),
                            'factor_22': Decimal(str(row.get('factor_22', '0.0')).replace(',', '.')),
                            'factor_23': Decimal(str(row.get('factor_23', '0.0')).replace(',', '.')),
                            'factor_24': Decimal(str(row.get('factor_24', '0.0')).replace(',', '.')),
                            'factor_25': Decimal(str(row.get('factor_25', '0.0')).replace(',', '.')),
                            'factor_26': Decimal(str(row.get('factor_26', '0.0')).replace(',', '.')),
                            'factor_27': Decimal(str(row.get('factor_27', '0.0')).replace(',', '.')),
                            'factor_28': Decimal(str(row.get('factor_28', '0.0')).replace(',', '.')),
                            'factor_29': Decimal(str(row.get('factor_29', '0.0')).replace(',', '.')),
                            'factor_30': Decimal(str(row.get('factor_30', '0.0')).replace(',', '.')),
                            'factor_31': Decimal(str(row.get('factor_31', '0.0')).replace(',', '.')),
                            'factor_32': Decimal(str(row.get('factor_32', '0.0')).replace(',', '.')),
                            'factor_33': Decimal(str(row.get('factor_33', '0.0')).replace(',', '.')),
                            'factor_34': Decimal(str(row.get('factor_34', '0.0')).replace(',', '.')),
                            'factor_35': Decimal(str(row.get('factor_35', '0.0')).replace(',', '.')),
                            'factor_36': Decimal(str(row.get('factor_36', '0.0')).replace(',', '.')),
                            'factor_37': Decimal(str(row.get('factor_37', '0.0')).replace(',', '.')),
                        }
                    )
                    if created: registros_creados += 1
                    else: registros_actualizados += 1
                return JsonResponse({'success': True, 'message': f'Archivo de factores procesado. Se crearon {registros_creados} y se actualizaron {registros_actualizados} registros.'})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': f'Ocurrió un error al procesar el archivo: {e}'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- VISTA 2: CARGA MASIVA DE MONTOS (ACTUALIZADA) ---
@corredor_requerido
def carga_masiva_montos(request):
    if request.method == 'POST':
        form = CargaCSVForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_csv']
            corredor = request.user.corredor # <-- ¡OBTENEMOS EL CORREDOR DEL USUARIO!
            try:
                df = pd.read_csv(archivo, sep=';')
                registros_creados = 0
                registros_actualizados = 0
                for index, row in df.iterrows():
                    suma_base = sum(Decimal(str(row.get(f'monto_{i}', '0.0')).replace(',', '.')) for i in range(8, 20))
                    factores_calculados = {}
                    if suma_base > 0:
                        for i in range(8, 38):
                            monto_actual = Decimal(str(row.get(f'monto_{i}', '0.0')).replace(',', '.'))
                            factores_calculados[f'factor_{i}'] = (monto_actual / suma_base)
                    else:
                        for i in range(8, 38):
                            factores_calculados[f'factor_{i}'] = Decimal('0.0')
                    calificacion, created = CalificacionTributaria.objects.update_or_create(
                        corredor=corredor, # <-- Usamos el corredor del usuario
                        instrumento=row['instrumento'],
                        fecha=row['fecha'],
                        defaults={
                            'secuencia': row.get('secuencia', 0),
                            'numero_dividendo': row.get('numero_dividendo', 0),
                            'tipo_sociedad': row.get('tipo_sociedad', 'A'),
                            'valor_historico': Decimal(str(row.get('valor_historico', '0.0')).replace(',', '.')),
                            'instrumento_no_inscrito': bool(row.get('instrumento_no_inscrito', False)),
                            'fuente_ingreso': 'MON',
                            **factores_calculados
                        }
                    )
                    if created: registros_creados += 1
                    else: registros_actualizados += 1
                return JsonResponse({'success': True, 'message': f'Archivo de montos procesado. Se crearon {registros_creados} y se actualizaron {registros_actualizados} registros.'})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': f'Ocurrió un error al procesar el archivo: {e}'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- VISTA 3: MANTENEDOR PRINCIPAL (ACTUALIZADA) ---
@login_required # <-- Ya la teníamos protegida
def mantenedor_calificaciones(request):
    # ¡FILTRAMOS! Solo mostramos los datos del corredor que inició sesión
    try:
        corredor_actual = request.user.corredor
        calificaciones = CalificacionTributaria.objects.filter(corredor=corredor_actual).order_by('-fecha')
    except Corredor.DoesNotExist:
        # Si el usuario no es un corredor (ej. es un superadmin sin vínculo)
        calificaciones = CalificacionTributaria.objects.none() # No mostramos nada
        messages.warning(request, "Tu usuario no está vinculado a ningún corredor. Contacta al administrador.")

    filtro_form = FiltroCalificacionesForm(request.GET)
    if filtro_form.is_valid():
        tipo_mercado = filtro_form.cleaned_data.get('tipo_mercado')
        origen = filtro_form.cleaned_data.get('origen')
        periodo_comercial = filtro_form.cleaned_data.get('periodo_comercial')
        if tipo_mercado: calificaciones = calificaciones.filter(tipo_mercado=tipo_mercado)
        if origen: calificaciones = calificaciones.filter(origen=origen)
        if periodo_comercial: calificaciones = calificaciones.filter(fecha__year=periodo_comercial)
    
    ingreso_form = IngresoBasicoForm() 
    montos_form = IngresoMontosForm() 
    factores_form = IngresoFactoresForm()
    carga_csv_form = CargaCSVForm()

    nombres_factores = {
        'factor_8': 'Créd. DPC s/d', 'factor_9': 'Créd. DPC Acum.', 'factor_10': 'Créd. DPC Vol.',
        'factor_11': 'Créd. s/d Acum.', 'factor_12': 'Rentas Prov.', 'factor_13': 'Otras Rentas',
        'factor_14': 'Distr. Desprop.', 'factor_15': 'Util. Afectas', 'factor_16': 'Rentas Gen.',
        'factor_17': 'Rentas Exentas (IGC)', 'factor_18': 'Rentas Exentas (IA)', 'factor_19': 'Ing. No Renta',
        'factor_20': 'No Sujetos (Sin/d) H. 31.12.2019', 'factor_21': 'No Sujetos (Con/d) H. 31.12.2019',
        'factor_22': 'No Sujetos (Sin/d) A. 01.01.2020', 'factor_23': 'No Sujetos (Con/d) A. 01.01.2020',
        'factor_24': 'Sujeto Rest. (Sin/d)', 'factor_25': 'Sujeto Rest. (Con/d)',
        'factor_26': 'Sujeto Rest. Sin derecho', 'factor_27': 'Sujeto Rest. Con derecho',
        'factor_28': 'Crédito IPE', 'factor_29': 'Asoc. Rentas (Sin/d)', 'factor_30': 'Asoc. Rentas (Con/d)',
        'factor_31': 'Asoc. Rentas Exentas (Sin)', 'factor_32': 'Asoc. Rentas Exentas (Con)',
        'factor_33': 'Crédito por IPE (Asoc.)', 'factor_34': 'Tasa Efectiva', 'factor_35': 'Tasa Efectiva (Rest.)',
        'factor_36': 'Tasa Efectiva (Acum.)', 'factor_37': 'Tasa Efectiva (Art. 20)',
    }

    context = {
        'form': filtro_form,
        'ingreso_form': ingreso_form, 
        'montos_form': montos_form, 
        'factores_form': factores_form, 
        'carga_csv_form': carga_csv_form,
        'calificaciones': calificaciones,
        'nombres_factores': nombres_factores
    }
    return render(request, 'calificaciones/mantenedor.html', context)


# --- VISTA 4: INGRESAR (Paso 1) (ACTUALIZADA) ---
@corredor_requerido
def ingresar_calificacion(request):
    if request.method == 'POST':
        form = IngresoBasicoForm(request.POST)
        if form.is_valid():
            corredor = request.user.corredor # <-- ¡Usamos el corredor del usuario!
            nueva_calificacion = form.save(commit=False)
            nueva_calificacion.corredor = corredor # <-- Asignamos
            nueva_calificacion.fuente_ingreso = 'MAN'
            nueva_calificacion.save()
            return JsonResponse({'success': True, 'calificacion_id': nueva_calificacion.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- VISTA 5: CALCULAR MONTOS (Paso 2) (Sin cambios de lógica) ---
@corredor_requerido
def ingresar_montos(request, calificacion_id):
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id, corredor=request.user.corredor) # Seguridad
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
                        factores_calculados[f'factor_{i}'] = (monto_actual / suma_base)
                else:
                    for i in range(8, 38):
                        factores_calculados[f'factor_{i}'] = Decimal('0.0')
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


# --- VISTA 6: ELIMINAR (ACTUALIZADA) ---
@corredor_requerido
def eliminar_calificacion(request, calificacion_id):
    if request.method == 'POST':
        try:
            # ¡Seguridad! Solo podemos borrar si el registro pertenece a nuestro corredor
            calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id, corredor=request.user.corredor)
            instrumento_nombre = calificacion.instrumento
            calificacion.delete()
            return JsonResponse({'success': True, 'message': f'Registro para {instrumento_nombre} eliminado exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


# --- VISTA 7: OBTENER DATOS (Para Modificar) (ACTUALIZADA) ---
@corredor_requerido
def obtener_calificacion_json(request, calificacion_id):
    if request.method == 'GET':
        try:
            # ¡Seguridad! Solo podemos obtener si el registro pertenece a nuestro corredor
            calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id, corredor=request.user.corredor)
            data = model_to_dict(calificacion)
            data['fecha'] = calificacion.fecha.strftime('%Y-%m-%d')
            return JsonResponse({'success': True, 'data': data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


# --- VISTA 8: MODIFICAR (Paso 1) (ACTUALIZADA) ---
@corredor_requerido
def modificar_calificacion(request, calificacion_id):
    # ¡Seguridad!
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id, corredor=request.user.corredor)
    if request.method == 'POST':
        form = IngresoBasicoForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save() 
            return JsonResponse({'success': True, 'calificacion_id': calificacion.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})


# --- VISTA 9: GUARDAR FACTORES (Paso 3) (ACTUALIZADA) ---
@corredor_requerido
def guardar_factores(request, calificacion_id):
    # ¡Seguridad!
    calificacion = get_object_or_404(CalificacionTributaria, id=calificacion_id, corredor=request.user.corredor)
    if request.method == 'POST':
        form = IngresoFactoresForm(request.POST)
        if form.is_valid():
            try:
                suma_factores_validacion = sum(form.cleaned_data.get(f'factor_{i}', Decimal('0.0')) for i in range(8, 20))
                if suma_factores_validacion > 1:
                    return JsonResponse({'success': False, 'errors': 'Error: La suma de los factores del 8 al 19 no puede ser mayor que 1.'})
                for i in range(8, 38):
                    setattr(calificacion, f'factor_{i}', form.cleaned_data[f'factor_{i}'])
                calificacion.save() 
                return JsonResponse({'success': True, 'message': 'Calificación guardada exitosamente.'})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})