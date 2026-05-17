import factory

from factory.django import DjangoModelFactory

from companies.models import Company

from tests.factories.users import CustomUserFactory


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company
        skip_postgeneration_save = True
    
    name = factory.Sequence(lambda n: f'Company {n}')
    owner = factory.SubFactory(CustomUserFactory)