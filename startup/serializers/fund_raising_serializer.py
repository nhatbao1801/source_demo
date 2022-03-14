from rest_framework import serializers

# from models.fund_raising import FundRaising
from event.models.fund_raising import FundRaising

class FundRaisingSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0, required=False)
    team_id = serializers.IntegerField(min_value=0)
    funding_stage_id = serializers.IntegerField(min_value=0)
    security_type_id = serializers.IntegerField(min_value=0)
    privacy_setting_id = serializers.IntegerField(min_value=0)
    target_valuation = serializers.DecimalField(max_digits=40, decimal_places=3)
    amount_raising = serializers.DecimalField(max_digits=40, decimal_places=3)
    closing_date = serializers.DateTimeField()
    status = serializers.BooleanField(default=True)

    def create(self, validated_data):
        team_id = validated_data.get('team_id')
        funding_stage_id = validated_data.get('funding_stage_id')
        security_type_id = validated_data.get('security_type_id')
        privacy_setting_id = validated_data.get('privacy_setting_id')
        target_valuation = validated_data.get('target_valuation')
        amount_raising = validated_data.get('amount_raising')
        closing_date = validated_data.get('closing_date')
        status = validated_data.get('status')
        return FundRaising.objects.create(
            team_id=team_id, funding_stage_id=funding_stage_id,
            security_type_id=security_type_id, privacy_setting_id=privacy_setting_id,
            target_valuation=target_valuation, amount_raising=amount_raising, closing_date=closing_date,
            status=status
        )

    def update(self, instance, validated_data):
        instance.team_id = validated_data.get('team_id')
        instance.funding_stage_id = validated_data.get('funding_stage_id')
        instance.security_type_id = validated_data.get('security_type_id')
        instance.privacy_setting_id = validated_data.get('privacy_setting_id')
        instance.target_valuation = validated_data.get('target_valuation')
        instance.amount_raising = validated_data.get('amount_raising')
        instance.closing_date = validated_data.get('closing_date')
        instance.status = validated_data.get('status')
        instance.save()
        return instance
