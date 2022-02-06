from django.test import TestCase

# Create your tests here.

# Projekt: CreateView mit overriding schreiben

class SmalladCreateView(LoginRequiredMixin, View):
    template_name = 'smallads/smallad_form.html'
    success_url = reverse_lazy('smallads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        category = request.GET.get('category')
        if category != '':
            ctx = {'form': form}
        else:
            ctx = {'form': form}
        return render(request, self.template_name, ctx)


        '''
                mit der folgenden Zeile Code werden nur die Zeilen für die kleinen FK-Tabellen befüllt
                This is meant as a shortcut to boilerplatish code. For example:

                try:
                    obj = Person.objects.get(first_name='John', last_name='Lennon')
                except Person.DoesNotExist:
                    obj = Person(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
                    obj.save()
                This pattern gets quite unwieldy as the number of fields in a model goes up. The above example can be rewritten using get_or_create() like so:

                obj, created = Person.objects.get_or_create(first_name='John', last_name='Lennon',
                                  defaults={'birthday': date(1940, 10, 9)})
        '''

    def post(self, request, pk=None):
        data = request.POST

        '''
        if data['category'] != 'none':
            category = SmalladCategory.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = SmalladCategory.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        smallad = Smallad.objects.create(
                title = data['title']
                price = data['price']
                category=category,
                description=data['description'],
                image=data['image']
            )

        return redirect('smallads:all')

    ctx = {'categories': categories}
    return render(request, self.template_name, ctx)
        '''
        #data = request.POST.get('category_new') #das ist alles, was in der html unter name='' steht
        #if data = '':
            #form = CreateForm(request.POST, request.FILES or None)
        if data['category'] == '':

            #category = SmalladCategory.objects.get(id=data['category'])
            category = SmalladCategory(name=data['category_new'])
            category.save()

        elif data['category_new'] == '':
            category = SmalladCategory.objects.get(id=data['category'])
            #category, created = SmalladCategory.objects.get_or_create(
                #name=data['category_new'])

        else:
            return category

        # name ist das Feld aus dem Model SmalladCategory, 'category_new' kommt aus der smallad_create.html - NEIN ;-)
        #c, created = SmalladCategory.objects.get_or_create(name=data)
        # wie kommt denn jetzt c in die form???
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        smallad = form.save(commit=False)
        smallad.owner = self.request.user
        # funzt die nächste Zeile - skeptisch hmmm - neee Fehlermeldung
        # Cannot assign "'Strandbilder 2'": "Smallad.category" must be a "SmalladCategory" instance.
        #new_category_to_show = request.POST.get('category_new')
        #smallad.category.name
        smallad.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()    # Add this
        return redirect(self.success_url)