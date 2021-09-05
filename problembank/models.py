from _typeshed import Self
from karsoogh.settings.base import rel

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
    
    def __str__(self):
        return self.title


class Subtopic(models.Model):
    title = models.CharField(max_length=30, verbose_name='عنوان')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='موضوع', related_name='subtopics')

    def __str__(self):
        return f'{self.topic.title} - {self.title}'



class BaseProblem(models.Model):
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
    subtopics = models.ManyToManyField(Subtopic, verbose_name='زیر موضوع(ها)', blank=True, related_name='problems')
    source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.SET_NULL,
                                verbose_name='منبع', related_name='problems')
    
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, verbose_name='سختی',
                                  default=Difficulty.Medium)
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
    upvoteCount = models.IntegerField(default=0, verbose_name='تعداد آرای مثبت')
    is_checked = models.BooleanField(default=False, verbose_name='آیا بررسی شده؟')
    


class Problem(models.Model):
    class Type(models.TextChoices):
        ShortAnswer = 'ShortAnswer'
        Descriptive = 'Descriptive'
        MultiChoice = 'MultiChoice'
    
    base_problem = models.ForeignKey(BaseProblem, on_delete=models.CASCADE, related_name='problems', verbose_name='مسئله')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.Descriptive, verbose_name='نوع')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', related_name='problems')
    
    text = models.TextField(verbose_name='متن')
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان انتشار')
    last_change_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان آخرین تغییر')

    priority = models.IntegerField(default=1, null=True, blank=True, verbose_name='اولویت')    
    is_private = models.BooleanField(default=True, verbose_name='آیا خصوصی است؟')
    # cost = models.IntegerField(default=0, verbose_name='هزینه‌ی دریافت') 
    # reward = models.IntegerField(default=0, verbose_name='پاداش حل‌کردن')

    def __str__(self):
        return f'{self.title} ({self.type}، ' \
               f'{self.problem.difficulty})'

    objects = InheritanceManager()

    class Meta:
        abstract = True


class ShortAnswerProblem(Problem):
    answer = models.OneToOneField('ShortAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='problem', verbose_name='پاسخ صحیح')
class DescriptiveProblem(Problem):
    answer = models.OneToOneField('DescriptiveAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='problem', verbose_name='پاسخ صحیح')
class MultiChoiceProblem(Problem):
    answer = models.OneToOneField('MultiChoiceAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='problem', verbose_name='پاسخ صحیح')

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
    text = models.IntegerField(verbose_name='شماره گزینه')


class UploadFileAnswer(Answer):
    answer_file = models.FileField(upload_to='AnswerFile', max_length=4000, blank=False)
    file_name = models.CharField(max_length=50, verbose_name='نام فایل')


class Guidance(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name='مسئله', related_name='guidances')
    text = models.TextField(verbose_name='متن')
    priority = models.IntegerField(default=1, null=True, blank=True, verbose_name='اولویت')    
    
class BaseSubmit(models.Model):
    class Status(models.TextChoices):
        Received = 'Received'
        Delivered = 'Delivered'
        Judged = 'Judged'

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name='مسئله', related_name='submissions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', related_name='submissions')
    received_at = models.DateTimeField(default=timezone.now, received_at='تاریخ دریافت مسئله')
    status = models.CharField(max_length=20, default=Status.Received,
                                     choices=Status.choices, verbose_name='وضعیت تصحیح')
    delivered_at = models.DateTimeField(null=True, verbose_name='تاریخ دریافت پاسخ')
    judged_at = models.DateTimeField(null=True, verbose_name='تاریخ تصحیح')
    mark = models.IntegerField(default=0, verbose_name='نمره')
    #event!!

    objects = InheritanceManager()

    def __str__(self):
        return 'Submit from %s for problem %s with status %s' % (
            self.author.username, self.problem.title, self.status
        )

    
class ShortAnswerSubmit(BaseSubmit):
    answer = models.OneToOneField('ShortAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='submit_answer', verbose_name='پاسخ')
    
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
    text_answer = models.OneToOneField('UploadFileAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='submit_answer', verbose_name='پاسخ متنی')
    upload_file_answer = models.OneToOneField('UploadFileAnswer', null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='submit_answer', verbose_name='پاسخ آپلودی')
    judge_note = models.CharField(max_length=200, null=True, blank=True, verbose_name='نظر مصحح')

    judged_by = models.ForeignKey(User,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True, related_name='judged_problems', verbose_name='مصحح')

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


class Comment(models.Model):
    base_problem = models.ForeignKey(BaseProblem, on_delete=models.CASCADE, related_name='comments', verbose_name='مسئله')
    text = models.TextField(verbose_name='متن')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', related_name='comments')
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='زمان انتشار')
    def __str__(self):
        return f'{self.writer.first_name} {self.writer.last_name} | {self.problem.title}'

class ProblemCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    problems = models.ManyToManyField(Problem, verbose_name='مسئله(ها)', blank=True, related_name='categories') #maby many to one

    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='صاحب', related_name='categories')
    mentors = models.ManyToManyField(Problem, verbose_name='همیار(ها)', blank=True, related_name='categories')
    # viewers = models.ManyToManyField(Problem, verbose_name='بیننده(ها)', blank=True)
    #roles    


#handle related names   
#handle events
