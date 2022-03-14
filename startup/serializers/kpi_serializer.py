from rest_framework import serializers

# from main.models.kpi import KPI
from event.models.kpi import KPI

class KPISerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0, required=False)
    team_id = serializers.IntegerField(min_value=0)
    revenue = serializers.DecimalField(max_digits=20, decimal_places=3)
    private_setting_id = serializers.IntegerField(min_value=0)
    num_customer = serializers.IntegerField(min_value=0)
    amount_raised = serializers.DecimalField(max_digits=20, decimal_places=3)
    number_of_employee = serializers.IntegerField(min_value=0)
    total_funding = serializers.DecimalField(max_digits=20, decimal_places=3)
    cash_in_bank = serializers.DecimalField(max_digits=20, decimal_places=3)

    def create(self, validated_data):
        team_id = validated_data.get('team_id')
        revenue = validated_data.get('revenue')
        private_setting_id = validated_data.get('private_setting_id')
        num_customer = validated_data.get('num_customer')
        amount_raised = validated_data.get('amount_raised')
        number_of_employee = validated_data.get('number_of_employee')
        total_funding = validated_data.get('total_funding')
        cash_in_bank = validated_data.get('cash_in_bank')
        return KPI.objects.create(team_id=team_id, revenue=revenue, num_customer=num_customer,
                                  amount_raised=amount_raised, number_of_employee=number_of_employee,
                                  private_setting_id=private_setting_id,
                                  total_funding=total_funding, cash_in_bank=cash_in_bank
                                  )

    def update(self, instance, validated_data):
        instance.team.id = validated_data.get('team_id')
        instance.revenue = validated_data.get('revenue')
        instance.private_setting.id = validated_data.get('private_setting_id')
        instance.num_customer = validated_data.get('num_customer')
        instance.amount_raised = validated_data.get('amount_raised')
        instance.number_of_employee = validated_data.get('number_of_employee')
        instance.total_funding = validated_data.get('total_funding')
        instance.cash_in_bank = validated_data.get('cash_in_bank')
        instance.save()
        return instance
