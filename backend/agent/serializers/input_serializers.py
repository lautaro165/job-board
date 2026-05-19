from rest_framework import serializers

class ResumeAnalysisSerializer(serializers.Serializer):
    resume = serializers.FileField(required=True)
        
class JobSearchHumanInputSerializer(serializers.Serializer):
    text = serializers.CharField(min_lenght=5)