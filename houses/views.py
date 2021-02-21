from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import TemplateView, ListView, DetailView, View, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import models
from django.contrib.auth.models import User
from .models import House, Comment
from .forms import CommentForm


'''
    house_list 
    HouseCreate
    HouseUpdate
    HouseDelete
    HouseDetail # <-- display house detail page + create comment
    HouseUpdateComment # <-- display house detail page + update comment
    HouseDetailComment # <-- display delete comment page + redirect to house detail page
'''


def house_list(request):
    house_list = House.objects.all()
    paginator = Paginator(house_list, 5)
    page = request.GET.get('page')

    try:
        house_list = paginator.page(page)
    except PageNotAnInteger: 
        house_list = paginator.page(1) # deliver the first page
    except EmptyPage:
        if request.is_ajax(): # the page is out of range 
            return HttpResponse('') # return an empty page
        house_list = paginator.page(paginator.num_pages) # range deliver last page 

    if request.is_ajax():
        print('ajax request')
        return render(request, 'houses/house/house_list_ajax.html', {'house_list': house_list})

    return render(request, 'houses/house/house_list.html', {'house_list': house_list})


class HouseCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create house 
    model = House
    initial = {'description': 'beaultiful house'}
    template_name = 'houses/house/house_form_create.html' 
    fields = ['description', 'main_picture', 'price', 'location', 'phonenumber', 'email']
    success_message = "house was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class HouseUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update house 
    model = House
    template_name = 'houses/house/house_form_update.html' 
    fields = ['description', 'main_picture', 'price', 'location', 'phonenumber', 'email']
    success_message = "house was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")

# delete house 
class HouseDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = House
    template_name = 'houses/house/house_confirm_delete.html' 
    success_message = "house was deleted successfully"
    success_url = reverse_lazy('house:house_list')

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


# ************* create comment ************* 
class HouseDetail(SingleObjectMixin, View): 
    model = House

    # display detail page with house instance and comment_form
    def get(self, request, *args, **kwargs):
        house = self.get_object()
        comment_form = CommentForm()
        context = {'house': house, 'comment_form': comment_form}
        return render(request, 'houses/house/house_detail.html', context)

    # save comment form and redisplay detail page with house instance and comment_form
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        house = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.created_by = request.user
            comment_form.instance.house = house
            comment_form.save()
        context = {'house': house, 'comment_form': comment_form}
        return render(request, 'houses/house/house_detail.html', context)


# ************* update comment ************* 
class HouseUpdateComment(SingleObjectMixin, View): 
    model = House

    # display detail page with house instance and comment_form
    def get(self, request, *args, **kwargs):
        house = self.get_object()
        current_comment = get_object_or_404(Comment, house=house, pk=kwargs['comment_pk'])
        comment_form = CommentForm(instance=current_comment)
        context = {'house': house, 'comment_form': comment_form, 'update_form': True}
        return render(request, 'houses/house/house_detail.html', context)

    # update comment and redisplay detail page with house instance and comment_form
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        house = self.get_object()
        current_comment = get_object_or_404(Comment, house=house, pk=kwargs['comment_pk'])
        comment_form = CommentForm(request.POST, instance=current_comment)
        if comment_form.is_valid():
            # update comment manually
            new_content = comment_form.cleaned_data['content']
            current_comment.content = new_content 
            current_comment.save()
        context = {'house': house, 'comment_form': comment_form}
        return render(request, 'houses/house/house_detail.html', context)


# ************* delete comment ************* 
class HouseDeleteComment(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = House
    template_name = 'houses/house/comment_confirm_delete.html' 
    success_message = "comment was deleted successfully"

    def get_success_url(self):
        # redirect to house detail
        return reverse('houses:house_detail', kwargs={'pk': self.object.house.pk})

    def get_object(self):
        house = super().get_object()
        current_comment = get_object_or_404(Comment, house=house, pk=self.kwargs['comment_pk'])
        return current_comment

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


