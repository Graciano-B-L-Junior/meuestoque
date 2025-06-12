# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Produto
from .forms import ProdutoForm

# View para listar todos os produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'core/lista_produtos.html', {'produtos': produtos})

# View para ver os detalhes de um produto
def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'core/detalhe_produto.html', {'produto': produto})

# View para adicionar um novo produto
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'core/form_produto.html', {'form': form})

# View para editar um produto existente
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('core:lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'core/form_produto.html', {'form': form})

# View para deletar um produto
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('core:lista_produtos')
    return render(request, 'core/confirmar_delete.html', {'object': produto})