from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from visitantes.models import Visitante
from .forms import VisitanteForm, AutorizaVisitanteForm
import logging
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)

@login_required
def registrar_visitante(request):
    if request.method == 'POST':
        form = VisitanteForm(request.POST)
        if form.is_valid():
            visitante = form.save(commit=False)
            # Verifica se o usuário está autenticado e atribui o porteiro
            if hasattr(request.user, 'porteiro'):
                visitante.registrado_por = request.user.porteiro  # Atribui o porteiro responsável
                visitante.save()
                messages.success(request, "Visitante registrado com sucesso!")
                return redirect('index')
            else:
                messages.error(request, "Erro ao registrar o visitante. Porteiro não encontrado.")
        else:
            # Adiciona mensagem de erro caso o formulário seja inválido
            messages.error(request, "Erro ao registrar o visitante. Verifique os dados e tente novamente.")
    else:
        form = VisitanteForm()

    return render(request, 'registrar_visitante.html', {'form': form, 'nome_pagina': 'Registrar Visitante'})

@login_required
def informacoes_visitante(request, id):
    visitante = get_object_or_404(Visitante, id=id)
    form = AutorizaVisitanteForm(instance=visitante)

    if request.method == "POST":
        form = AutorizaVisitanteForm(request.POST, instance=visitante)
        if form.is_valid():
            form.save()
            messages.success(request, "Visitante autorizado com sucesso.")
            return redirect("index")

    context = {
        "visitante": visitante,
        "form": form,
    }
    return render(request, "informacoes_visitante.html", context)

@login_required
def finalizar_visita(request, id):
    visitante = get_object_or_404(Visitante, id=id)

    if visitante.status != 'FINALIZADO':
        visitante.status = 'FINALIZADO'
        visitante.horario_saida = timezone.now()
        visitante.save()
        messages.success(request, "Visita finalizada com sucesso!")
    else:
        messages.warning(request, "Essa visita já foi finalizada.")

    return redirect('index')

@login_required
def alterar_status_visitante(request, id):
    visitante = get_object_or_404(Visitante, id=id)
    form = AutorizaVisitanteForm(request.POST or None, instance=visitante)

    if request.method == 'POST' and form.is_valid():
        novo_status = request.POST.get('status')

        if novo_status == 'FINALIZADO' and visitante.status != 'FINALIZADO':
            visitante.status = 'FINALIZADO'
            visitante.horario_saida = timezone.now()
        elif novo_status == 'EM_VISITA' and visitante.status == 'AGUARDANDO':
            visitante.status = 'EM_VISITA'
            visitante.horario_autorizacao = timezone.now()

        visitante.save()
        messages.success(request, f"Status alterado para {visitante.get_status_display()} com sucesso!")
        return redirect('index')
    
    return redirect('informacoes_visitante', id=id)

@login_required


def index(request):
    # Contar visitantes com diferentes status
    visitantes_aguardando = Visitante.objects.filter(status='AGUARDANDO').count()
    visitantes_no_condominio = Visitante.objects.filter(status='EM_VISITA').count()
    visitas_finalizadas = Visitante.objects.filter(status='FINALIZADO').count()
    
    # Contar visitantes registrados no mês atual
    mes_atual = timezone.now().month
    visitantes_registrados_mes = Visitante.objects.filter(horario_chegada__month=mes_atual).count()
    
    # Obter todos os visitantes para exibir na tabela
    todos_visitantes = Visitante.objects.all()

    context = {
        'visitantes_aguardando': visitantes_aguardando,
        'visitantes_no_condominio': visitantes_no_condominio,
        'visitas_finalizadas': visitas_finalizadas,
        'visitantes_registrados_mes': visitantes_registrados_mes, 
        'todos_visitantes': todos_visitantes,
    }

    return render(request, 'index.html', context)


@login_required
def listar_visitantes(request):
    visitantes = Visitante.objects.all()
    return render(request, 'listar_visitantes.html', {'visitantes': visitantes})
