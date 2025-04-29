"""from rest_framework import serializers
from ...models import Task
# from accounts.models import Profile

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id','name')

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    task_name = serializers.CharField(max_length=200)

class TaskSerializer(serializers.ModelSerializer):
    ''' Different methods of limiting some fields and defining specific fields '''
    # content = serializers.CharField(read_only=True)
    # content = serializers.ReadOnlyField()
    ''' because get_snippet & get_absolute_api_url have not parameters then relate to request object
        they define in the model class '''
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url',read_only=True)

    ''' because get_absolute_url have parameters that relate to request object
        they define in the serializer class itself '''
    absolute_url = serializers.SerializerMethodField()
    ''' Custom naming for methods '''
    # absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')

    ''' (PUT),(POST) نمایش نام فیلد رابطه دار در زمان ارسال اطلاعات '''
    # category = serializers.SlugRelatedField(many=False, slug_field='name', queryset=Category.objects.all())

    ''' نمایش اطلاعات منتخب فیلد رابطه دار صرفاً در بخش نمایش دادهها '''
    # category = CategorySerializer()

    class Meta:
        model = Task
        # fields = '__all__'
        fields = ('user','task_name','completed','created_at','updated_at')
        read_only_fields = ('user',)

    # def get_abs_url(self,obj):
    def get_absolute_url(self,obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    ''' بازنویسی مناسب این تابع برای نمایش مشخصات فیلدهای رابطه دار در بخش نمایش دادهها
       بهمراه امکان استفاده از مشخصه فیلد رابطه دار در فرم ارسال بسیار مفید است  '''
    def to_representation(self, instance):
        req = self.context.get('request')
        represent = super().to_representation(instance)

        # برای تشخیص اینکه درخواست درحالت تکی است و یا لیست است
        if req.parser_context.get('kwargs').get('pk'):    # درخواست بصورت تک آیتم
            # حذف برخی از فیلدهای غیر ضروری در بخش نمایش اطلاعات
            represent.pop('snippet',None)
            represent.pop('relative_url',None)
            represent.pop('absolute_url',None)
        else:   #  درخواست بصورت لیست
            represent.pop('task_name',None)
        # represent['category'] = CategorySerializer(instance.category).data
        return represent
    def create(self,validated_data):
        # تشکیل زنجیره درخواست میان جداول مرتبط
        # Post(author)= ->Profile(user)->User(id)
        validated_data['user'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)
"""

from rest_framework import serializers
from ...models import Task

# class TaskSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     task_name = serializers.CharField(max_length=200)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ["id", "task_name", "completed", "created_at", "user"]
