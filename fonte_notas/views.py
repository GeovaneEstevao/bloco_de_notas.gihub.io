from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, NoteForm
from django.contrib import messages
from .models import Note
from django.contrib.auth.decorators import login_required


# Parte da logica da criação, edição e exclusão das notas
@login_required
def manage_notes(request, note_id=None):
    if note_id:
        note = get_object_or_404(Note, id=note_id, user=request.user)  # Nota para edição ou exclusão
    else:
        note = None

    if request.method == 'POST':
        # Caso seja edição de uma nota existente
        if 'edit_note' in request.POST and note:
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                form.save()
                return redirect('home')

        # Caso seja uma nova nota
        elif 'create_note' in request.POST:
            form = NoteForm(request.POST)
            if form.is_valid():
                new_note = form.save(commit=False)
                new_note.user = request.user
                new_note.save()
                return redirect('home')

        # Caso seja exclusão de uma nota
        elif 'delete_note' in request.POST and note:
            note.delete()
            return redirect('home')

    else:
        # Se a requisição não for POST, mostramos o formulário vazio (para criação) ou com dados (para edição)
        form = NoteForm(instance=note)

    # Carregar todas as notas do usuário para exibir na página
    notes = Note.objects.filter(user=request.user)

    context = {
        'form': form,
        'notes': notes,
        'note': note
    }
    return render(request, 'note_list.html', context)



# Logica de apresentação do home
def home(request):
    user_notes = None
    if request.user.is_authenticated:
        # Exibe apenas as notas do usuário autenticado
        user_notes = Note.objects.filter(user=request.user)
    
    return render(request, 'home.html', {'user_notes': user_notes})

# Logica de cadastro
def cadastrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/cadastrar.html', {'form': form})

# Logica de login do usuario cadastrado
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirecione para a página inicial ou outra página
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

# Logica de deslogar
def user_logout(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('home')