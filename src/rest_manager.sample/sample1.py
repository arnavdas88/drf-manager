# Import the base router class
from rest_framework import routers

# Import the Manager
from rest_manager.APIManager import APIManager

# Assuming 2 models exists, say `Organization` & `User`
# and Organization has either a "Foreign Key" or a "ManyToMany
# Relation" with the `User` model,
from core.models.organization import Organization
from core.models.management.user import User


# We can define a Manager for the `User` model
user_manager = APIManager(User.objects.all())

# Set default fieldset to use
user_manager.fields = ['id', 'username', 'first_name']

# Explicitly defining fieldsets for POST and RETRIEVE
user_manager.fields_mapping['create'] = '__all__'
user_manager.fields_mapping['retrieve'] = '__all__'

# Explicitly defining the fields to exclude, from all fieldsets
user_manager.exclude = ['password']

# Building the entire structure, and getting back the router
user_router = user_manager()


# We can define a Manager for the `Organization` model
organization_manager = APIManager(Organization.objects.all())

# Set default fieldset to use
organization_manager.fields = ['id', 'name', 'description', 'users', 'last_updated_on']

# Explicitly defining fieldsets for POST and RETRIEVE
organization_manager.fields_mapping['retrieve'] = '__all__'

# Bringing Predefined Serializer from User Manager
# to be used in the Sub-Field `users`, explicitly for GET and RETRIEVE
organization_manager.nested_serializer['list']['users'] = user_manager.serializer_mapping['list']
organization_manager.nested_serializer['retrieve']['users'] = user_manager.serializer_mapping['list']

# Building the entire structure, and getting back the router
organization_router = organization_manager()

# Combining both the routers, to get the final route
router = routers.DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(organization_router.registry)