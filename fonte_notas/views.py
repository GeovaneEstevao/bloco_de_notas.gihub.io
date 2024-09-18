from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, NoteForm
from django.contrib import messages
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def user_dashboard(request):
    if request.method == 'POST':
        # Se o formulário de alteração de senha foi enviado
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Manter o usuário logado após a alteração da senha
            return redirect('user_dashboard')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'user': request.user,
        'form': form,
    }
    return render(request, 'user/user_dashboard.html', context)


# Parte da logica da criação, edição e exclusão das notas
@login_required
def manage_notes(request, note_id=None):
    if note_id:
        note = get_object_or_404(Note, id=note_id, user=request.user)
    else:
        note = None

    if request.method == 'POST':
        if 'edit_note' in request.POST and note:
            form = NoteForm(request.POST, instance=note)
            if form.is_valid():
                print("Form data:", form.cleaned_data)  # Verifique os dados do formulário
                form.save()
                return redirect('home')
        elif 'create_note' in request.POST:
            form = NoteForm(request.POST)
            if form.is_valid():
                print("Form data:", form.cleaned_data)  # Verifique os dados do formulário
                new_note = form.save(commit=False)
                new_note.user = request.user
                new_note.save()
                return redirect('home')
        elif 'delete_note' in request.POST and note:
            note.delete()
            return redirect('home')
    else:
        form = NoteForm(instance=note)

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
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('home')  # Redirecione para a página inicial ou outra página
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

# Logica de deslogar
def user_logout(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('home')