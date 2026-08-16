from django.db import transaction
from django.db.models import F
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from missions.models import Role, Goal, Block
from missions.serializers import RoleSerializer, GoalSerializer, BlockSerializer


# Create your views here.

class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer

    def get_queryset(self):
        return Role.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer

    def get_queryset(self):
        queryset = Goal.objects.filter(role__user=self.request.user)
        role_id = self.request.query_params.get('role')
        if role_id:
            queryset = queryset.filter(role_id=role_id)
        return queryset

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        goal = self.get_object()
        role_id = goal.role_id

        with transaction.atomic():
            Role.objects.filter(pk=role_id).update(points=F('points') + 1)
            goal.delete()

        points = Role.objects.values_list('points', flat=True).get(pk=role_id)
        return Response({'role': role_id, 'points': points})


class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer

    def get_queryset(self):
        queryset = Block.objects.filter(goal__role__user=self.request.user)
        goal_id = self.request.query_params.get('goal')
        if goal_id:
            queryset = queryset.filter(goal_id=goal_id)
        return queryset
