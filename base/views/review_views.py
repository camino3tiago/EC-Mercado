from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from base.forms import ReviewForm
from base.models import Review, Item
from django.db.models import Avg, Count

class PostReviewView(CreateView, LoginRequiredMixin):
    model = Review
    form_class = ReviewForm
    template_name = 'pages/post_review.html'
    success_url = reverse_lazy('top')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = Item.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product = Item.objects.get(id=self.kwargs['pk'])
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, 'レビューを送信しました！ありがとうございます！！')
        return redirect('top')


class ReviewListView(ListView):
    template_name = 'pages/item_review.html'
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = Item.objects.get(id=self.kwargs['pk'])
        context['reviews'] = Review.objects.filter(product=context['item'])       
        return context
    


