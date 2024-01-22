from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages
from django.urls import reverse


def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')

    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)

        return render(request, 'novo_flashcard.html',{'categorias': categorias,
                                                        'dificuldades': dificuldades,
                                                        'flashcards': flashcards,})
    
    elif request.method == "POST":
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha os campos de pergunta e resposta',)
            return redirect('/flashcard/novo_flashcard')

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        flashcard.save()

        messages.add_message(request, constants.SUCCESS, 'Flashcard criado com sucesso!')
        return redirect('/flashcard/novo_flashcard')


def deletar_flashcard(request, id):

    try:
        flashcard = Flashcard.objects.get(id=id, user=request.user)
    except Flashcard.DoesNotExist:
        messages.add_message(
            request, constants.ERROR, 'Flashcard não encontrado ou você não tem permissão para excluir.')
        return redirect('/flashcard/novo_flashcard')

    flashcard.delete()

    messages.add_message(request, constants.SUCCESS, 'Flashcard deletado com sucesso!')
    return redirect('/flashcard/novo_flashcard')

 
def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(request, 'iniciar_desafio.html', {'categorias': categorias,
                                                        'dificuldades': dificuldades})
    
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(

            user = request.user,
            titulo = titulo,
            quantidade_perguntas = qtd_perguntas,
            dificuldade=dificuldade,
        )

        desafio.save()

        for categoria in categorias:
            desafio.categoria.add()

        flashcard = (Flashcard.objects.filter(user=request.user)
                     .filter(dificuldade=dificuldade)
                     .filter(categoria_id__in=categorias)
                     )
        