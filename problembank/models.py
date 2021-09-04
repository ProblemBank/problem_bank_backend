from _typeshed import Self

from django.db.models.deletion import SET_NULL
from Game.models import Problem
from django.db import models
from Account.models import User
from model_utils.managers import InheritanceManager
from django.utils import timezone

class Source(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=30, verbose_name='عنوان')
    
    # sub_tags
    def __str__(self):
        return self.name


class SubTopic(models.Model):
    title = models.CharField(max_length=30, verbose_name='عنوان')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='موضوع')

    def __str__(self):
        return self.name



class Problem(models.Model):
    class Difficulty(models.TextChoices):
        VeryEasy = 'VeryEasy'
        Easy = 'Easy'
        Medium = 'Medium'
        Hard = 'Hard'
        VeryHard = 'VeryHard'

    
    class Grade(models.TextChoices):
        First = 1
        Second = 2
        Third = 3
        Forth = 4
        Fifth = 5
        Sixth = 6
        Seventh = 7
        Eight = 8
        Ninth = 9
        Tenth = 10
        Eleventh = 11
        Twelfth = 12

    title = models.CharField(max_length=100, verbose_name='عنوان')
    
    topics = models.ManyToManyField(Topic, verbose_name='موضوع(ها)', blank=True, related_name='problems')
    sub_topics = models.ManyToManyField(SubTopic, verbose_name='زیر موضوع(ها)', blank=True, related_name='problems')
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='منبع')
    
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, verbose_name='سختی',
                                  default=Difficulty.MEDIUM)
    suitable_for_over = models.IntegerField(
        choices=Grade.choices,
        default=Grade.First,
        verbose_name='پایین ترین پایه مناسب'
    )
    suitable_for_under  = models.IntegerField(
        choices=Grade.choices,
        default=Grade.Twelfth,
        verbose_name='بالاترین پایه مناسب'
    )
    is_checked = models.BooleanField(default=False, verbose_name='آیا بررسی شده؟')



class ProblemInstance(models.Model):
    class Type(models.TextChoices):
        ShortAnswer = 'ShortAnswer'
        Descriptive = 'Descriptive'
        MultiChoice = 'MultiChoice'
    
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problems', verbose_name='مسئله')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.Descriptive, verbose_name='نوع')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    
    text = models.TextField(verbose_name='متن')
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان انتشار')
    last_change_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان آخرین تغییر')

    priority = models.IntegerField(default=1, null=True, blank=True)    
    # cost = models.IntegerField(default=0, verbose_name='هزینه‌ی دریافت') 
    # reward = models.IntegerField(default=0, verbose_name='پاداش حل‌کردن')
    # answer = models.TextField(null=True, blank=True, verbose_name='پاسخ (اختیاری)')

    is_private = models.BooleanField(default=True, verbose_name='آیا خصوصی است؟')
    
    def __str__(self):
        return f'{self.title} ({self.type}، ' \
               f'{self.problem.difficulty})'

    class Meta:
        abstract = True


class ShortAnswerProblemInstance(ProblemInstance):
    answer = models.OneToOneField('ShortAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='problem')
class DescriptiveProblemInstance(ProblemInstance):
    answer = models.OneToOneField('DescriptiveAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='problem')
class MultiChoiceProblemInstance(ProblemInstance):
    answer = models.OneToOneField('MultiChoiceAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='problem')

class Answer(models.Model):
    class Type(models.TextChoices):
        ShortAnswer = 'ShortAnswer'
        Descriptive = 'Descriptive'
        MultiChoice = 'MultiChoice'

    type = models.CharField(max_length=20, choices=Type.choices, default=Type.Descriptive, verbose_name='نوع')
    objects = InheritanceManager()


class ShortAnswer(Answer):
    text = models.TextField(verbose_name='متن')

class DescriptiveAnswer(Answer):
    text = models.TextField(verbose_name='متن')


class MultiChoiceAnswer(Answer):
    text = models.IntegerField()


class UploadFileAnswer(Answer):
    answer_file = models.FileField(upload_to='AnswerFile', max_length=4000, blank=False)
    file_name = models.CharField(max_length=50)

class BaseSubmit(models.Model):
    class Status(models.TextChoices):
        Received = 'Received'
        Delivered = 'Delivered'
        Judged = 'Judged'

    problem = models.ForeignKey(ProblemInstance, on_delete=models.CASCADE, verbose_name='مسئله')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    received_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default=Status.Received,
                                     choices=Status.choices)
    delivered_at = models.DateTimeField(null=True)
    judged_at = models.DateTimeField(null=True)
    mark = models.IntegerField(default=0, verbose_name='نمره')

    class Meta:
        abstract = True

    def __str__(self):
        return 'Submit from %s for problem %s with status %s' % (
            self.author.username, self.problem.title, self.status
        )

    
class ShortAnswerSubmit(BaseSubmit):
    answer = models.OneToOneField('ShortAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='submit_answer')
    
    def check_answer(self):
        pass
        # is_correct = False
        # try:
        #     is_correct = self.answer.text == self.problem.answer.text
            
        # except ValueError:
        #     logger.warn('Type mismatch for %s' % self) #is it true log?
        # selfstatus = BaseSubmit.Status. if is_correct else BaseSubmit.SubmitStatus.Wrong
        # self.judged_at = timezone.now()
        # self.save()


class JudgeableSubmit(BaseSubmit):
    answer = models.OneToOneField('UploadFileAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='submit_answer')
    judge_note = models.CharField(max_length=200, null=True, blank=True)

    judged_by = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True)

    def save(self, *args, **kwargs):
        pass
        # # LONG TODO: fix here so not change every time
        # # Call standard save
        # super(JudgeableSubmit, self).save(*args, **kwargs)

        # if not settings.TESTING and self.submitted_answer and len(self.submitted_answer.name) < 40:
        #     initial_path = self.submitted_answer.path

        #     # New path in the form eg '/images/uploadmodel/1/image.jpg'
        #     dt = timezone.now()
        #     r = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        #     new_n = '-'.join([r, dt.strftime('%H-%M-%S-%f'), os.path.basename(initial_path)])
        #     new_name = 'answers/' + new_n
        #     new_path = os.path.join(settings.MEDIA_ROOT, 'answers', new_n)

        #     # Create dir if necessary and move file
        #     if not os.path.exists(os.path.dirname(new_path)):
        #         os.makedirs(os.path.dirname(new_path))

        #     os.rename(initial_path, new_path)

        #     # Update the image_file field
        #     self.submitted_answer.name = new_name

        #     # Save changes
        #     super(JudgeableSubmit, self).save(*args, **kwargs)



class Guidance(models.Model):
    problem = models.ForeignKey(ProblemInstance, on_delete=models.CASCADE, verbose_name='مسئله')
    text = models.TextField(verbose_name='متن')



class Comment(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='comments', verbose_name='مسئله')
    text = models.TextField(verbose_name='متن')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان انتشار')
    def __str__(self):
        return f'{self.writer.first_name} {self.writer.last_name} | {self.problem.title}'

class ProblemCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    problems = models.ManyToManyField(ProblemInstance, verbose_name='مسئله(ها)', blank=True) #maby many to one

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='صاحب')
    mentors = models.ManyToManyField(ProblemInstance, verbose_name='همیار(ها)', blank=True)
    # viewers = models.ManyToManyField(ProblemInstance, verbose_name='بیننده(ها)', blank=True)
    #roles    


#handle related names   
#handle events
