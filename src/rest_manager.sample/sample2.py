from rest_framework import routers

from rest_manager.APIManager import APIManager
from rest_manager.SerializerDefinition import Serializer

from core.models.organization import Organization
from core.models.management.user import User

user_serializer = Serializer(User)
user_serializer.fields = ['id', 'username', 'first_name']
user_serializer.exclude = [ 'password' ]
user_serializer.create.fields = '__all__'
user_serializer.retrieve.fields = '__all__'

user_manager = APIManager(User.objects.all(), user_serializer)
user_router = user_manager()



organization_serializer = Serializer(Organization)
organization_serializer.fields = ['id', 'name', 'description', 'users', 'last_updated_on']
organization_serializer.create.fields = '__all__'
organization_serializer.create.retrieve = '__all__'

organization_serializer.list.define_serializer("users", user_serializer.list)
organization_serializer.retrieve.define_serializer("users", user_serializer.retrieve)
organization_manager = APIManager(Organization.objects.all(), organization_serializer)

organization_router = organization_manager()


router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(organization_router.registry)