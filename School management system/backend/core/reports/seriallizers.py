from rest_framework import serializers

class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    
    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    "Start date cannot be after end date"
                )
        return data

class ExportFormatSerializer(serializers.Serializer):
    format = serializers.ChoiceField(choices=['csv', 'pdf', 'excel'], default='csv')
    report_type = serializers.ChoiceField(
        choices=['student', 'attendance', 'finance', 'exam', 'library']
    )
    date_range = DateRangeSerializer(required=False)
    filters = serializers.DictField(required=False)

class DashboardStatsSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    total_classes = serializers.IntegerField()
    today_present = serializers.IntegerField()
    today_absent = serializers.IntegerField()
    monthly_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    monthly_expenses = serializers.DecimalField(max_digits=15, decimal_places=2)
    pending_fees = serializers.DecimalField(max_digits=15, decimal_places=2)
    upcoming_events = serializers.IntegerField()
    
class ChartDataSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    datasets = serializers.ListField(child=serializers.DictField())