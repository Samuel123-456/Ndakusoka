from django.urls import path
from controls.views import (
      signout,
      signin,
      signup,
)

urlpatterns = [
    path('signout/', signout, name='signout'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
]
