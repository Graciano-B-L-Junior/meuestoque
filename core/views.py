# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required # Importe o decorador
from .models import Produto
from .forms import ProdutoForm,MovimentoEstoqueForm

# --- Views de Autenticação ---
# (Vamos adicioná-las no próximo passo)


# --- Views do Estoque ---

@login_required # Protege a view
def lista_produtos(request):
    # Filtra os produtos para mostrar apenas os do usuário logado
    produtos = Produto.objects.filter(usuario=request.user)
    return render(request, 'core/lista_produtos.html', {'produtos': produtos})

@login_required
def detalhe_produto(request, pk):
    # Garante que o usuário só possa ver seus próprios produtos
    produto = get_object_or_404(Produto, pk=pk, usuario=request.user)
    return render(request, 'core/detalhe_produto.html', {'produto': produto})

@login_required
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            # Use commit=False para criar o objeto sem salvar no banco ainda
            produto = form.save(commit=False)
            # Associe o produto ao usuário logado
            produto.usuario = request.user
            # Agora salve o objeto no banco de dados
            produto.save()
            return redirect('core:lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'core/form_produto.html', {'form': form})

@login_required
def editar_produto(request, pk):
    # Garante que o usuário só possa editar seus próprios produtos
    produto = get_object_or_404(Produto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('core:lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'core/form_produto.html', {'form': form})

@login_required
def deletar_produto(request, pk):
    # Garante que o usuário só possa deletar seus próprios produtos
    produto = get_object_or_404(Produto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        produto.delete()
        return redirect('core:lista_produtos')
    return render(request, 'core/confirmar_delete.html', {'object': produto})

# core/views.py

# ... (imports existentes)
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# --- View de Registro ---
def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login') # Redireciona para a página de login após o registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# ... (resto das views do estoque)
# ATUALIZE a view detalhe_produto para buscar o histórico
@login_required
def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk, usuario=request.user)
    # Buscando o histórico de movimentos para este produto
    movimentos = produto.movimentos.all()
    context = {
        'produto': produto,
        'movimentos': movimentos
    }
    return render(request, 'core/detalhe_produto.html', context)

# CRIE esta nova view
@login_required
def adicionar_movimento(request, produto_pk):
    produto = get_object_or_404(Produto, pk=produto_pk, usuario=request.user)
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            movimento = form.save(commit=False)
            movimento.produto = produto
            movimento.usuario = request.user
            movimento.save()
            # Redireciona para a página de detalhes do produto após salvar
            return redirect('core:detalhe_produto', pk=produto.pk)
    else:
        form = MovimentoEstoqueForm()

    context = {
        'form': form,
        'produto': produto
    }
    return render(request, 'core/form_movimento.html', context)