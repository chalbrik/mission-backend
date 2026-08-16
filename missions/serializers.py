from rest_framework import serializers

from missions.models import Role, Goal, Block


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name', 'note', 'points']
        read_only_fields = ['points']


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ['id', 'target_outcome', 'role', 'created_at']

    def validate_role(self, role):
        if role.user != self.context['request'].user:
            raise serializers.ValidationError('Nie masz dostępu do tej roli.')
        return role


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = ['id', 'name', 'difficulty', 'goal', 'created_at']

    def validate_goal(self, goal):
        if goal.role.user != self.context['request'].user:
            raise serializers.ValidationError('Nie masz dostępu do tego celu.')
        return goal

