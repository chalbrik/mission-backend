from rest_framework.routers import DefaultRouter

from missions.views import RoleViewSet, GoalViewSet, BlockViewSet

router = DefaultRouter()
router.register('roles', RoleViewSet, basename='role')
router.register('goals', GoalViewSet, basename='goal')
router.register('blocks', BlockViewSet, basename='block')

urlpatterns = router.urls