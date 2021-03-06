# Generated by Django 3.2.3 on 2021-09-08 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='None', max_length=30)),
                ('last_name', models.CharField(default='None', max_length=30)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=200)),
                ('position', models.CharField(choices=[('Admin', 'Admin'), ('Member', 'Member'), ('NotRegistered', 'Notregistered')], default='Member', max_length=20, verbose_name='جایگاه')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DescriptiveAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_type', models.CharField(choices=[('ShortAnswer', 'Shortanswer'), ('DescriptiveAnswer', 'Descriptiveanswer')], default='DescriptiveAnswer', max_length=20, verbose_name='نوع')),
                ('text', models.TextField(verbose_name='متن')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('mentors', models.ManyToManyField(blank=True, related_name='editable_events', to='problembank.BankAccount', verbose_name='همیار(ها)')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_events', to='problembank.bankaccount', verbose_name='صاحب')),
                ('prticipants', models.ManyToManyField(blank=True, related_name='participated_events', to='problembank.BankAccount', verbose_name='بیننده(ها)')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='بدون عنوان', max_length=100, verbose_name='عنوان')),
                ('difficulty', models.CharField(choices=[('VeryEasy', 'Veryeasy'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('VeryHard', 'Veryhard')], default='Medium', max_length=20, verbose_name='سختی')),
                ('grade', models.CharField(choices=[('ElementarySchoolFirstHalf', 'Elementaryschoolfirsthalf'), ('ElementarySchoolSecondHalf', 'Elementaryschoolsecondhalf'), ('HighSchoolFirstHalf', 'Highschoolfirsthalf'), ('HighSchoolSecondHalf', 'Highschoolsecondhalf')], default='HighSchoolSecondHalf', max_length=30, verbose_name='پایه تحصیلی')),
                ('is_checked', models.BooleanField(default=False, verbose_name='آیا بررسی شده؟')),
                ('problem_type', models.CharField(choices=[('ShortAnswerProblem', 'Shortanswerproblem'), ('DescriptiveProblem', 'Descriptiveproblem')], default='DescriptiveProblem', max_length=20, verbose_name='نوع')),
                ('text', models.TextField(verbose_name='متن')),
                ('publish_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='زمان انتشار')),
                ('last_change_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='زمان آخرین تغییر')),
                ('is_private', models.BooleanField(default=True, verbose_name='آیا خصوصی است؟')),
                ('upvote_count', models.IntegerField(default=0, verbose_name='تعداد آرای مثبت')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='problembank.bankaccount', verbose_name='نویسنده')),
                ('copied_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='copies', to='problembank.problem', verbose_name='کپی شده از')),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_type', models.CharField(choices=[('ShortAnswer', 'Shortanswer'), ('DescriptiveAnswer', 'Descriptiveanswer')], default='DescriptiveAnswer', max_length=20, verbose_name='نوع')),
                ('text', models.TextField(verbose_name='متن')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='عنوان')),
            ],
        ),
        migrations.CreateModel(
            name='UploadFileAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_type', models.CharField(choices=[('ShortAnswer', 'Shortanswer'), ('DescriptiveAnswer', 'Descriptiveanswer')], default='DescriptiveAnswer', max_length=20, verbose_name='نوع')),
                ('answer_file', models.FileField(max_length=4000, upload_to='AnswerFile')),
                ('file_name', models.CharField(max_length=50, verbose_name='نام فایل')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='عنوان')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtopics', to='problembank.topic', verbose_name='موضوع')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('is_visible', models.BooleanField(default=True, verbose_name='آیا قابل نمایش است؟')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_groups', to='problembank.event', verbose_name='رویداد')),
                ('problems', models.ManyToManyField(related_name='groups', to='problembank.Problem', verbose_name='مسئله(ها)')),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problems', to='problembank.source', verbose_name='منبع'),
        ),
        migrations.AddField(
            model_name='problem',
            name='subtopics',
            field=models.ManyToManyField(blank=True, related_name='problems', to='problembank.Subtopic', verbose_name='زیر موضوع(ها)'),
        ),
        migrations.AddField(
            model_name='problem',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='problems', to='problembank.Topic', verbose_name='موضوع(ها)'),
        ),
        migrations.CreateModel(
            name='JudgeableSubmit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ دریافت مسئله')),
                ('status', models.CharField(choices=[('Received', 'Received'), ('Delivered', 'Delivered'), ('Judged', 'Judged')], default='Received', max_length=20, verbose_name='وضعیت تصحیح')),
                ('delivered_at', models.DateTimeField(null=True, verbose_name='تاریخ دریافت پاسخ')),
                ('judged_at', models.DateTimeField(null=True, verbose_name='تاریخ تصحیح')),
                ('mark', models.IntegerField(default=0, verbose_name='نمره')),
                ('judge_note', models.CharField(blank=True, max_length=200, null=True, verbose_name='نظر مصحح')),
                ('judged_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='judged_problems', to='problembank.bankaccount', verbose_name='مصحح')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='judgeablesubmit', to='problembank.problem', verbose_name='مسئله')),
                ('problem_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='judgeablesubmit', to='problembank.problemgroup', verbose_name='دسته مسئله')),
                ('respondents', models.ManyToManyField(related_name='judgeablesubmit', to='problembank.BankAccount', verbose_name='پاسخ دهنده (ها)')),
                ('text_answer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submit_answer', to='problembank.descriptiveanswer', verbose_name='پاسخ متنی')),
                ('upload_file_answer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submit_answer', to='problembank.uploadfileanswer', verbose_name='پاسخ آپلودی')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Guidance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن')),
                ('priority', models.IntegerField(blank=True, default=1, null=True, verbose_name='اولویت')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guidances', to='problembank.problem', verbose_name='مسئله')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='متن')),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='problembank.bankaccount', verbose_name='نویسنده')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='problembank.problem', verbose_name='مسئله')),
            ],
        ),
        migrations.CreateModel(
            name='AutoCheckSubmit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ دریافت مسئله')),
                ('status', models.CharField(choices=[('Received', 'Received'), ('Delivered', 'Delivered'), ('Judged', 'Judged')], default='Received', max_length=20, verbose_name='وضعیت تصحیح')),
                ('delivered_at', models.DateTimeField(null=True, verbose_name='تاریخ دریافت پاسخ')),
                ('judged_at', models.DateTimeField(null=True, verbose_name='تاریخ تصحیح')),
                ('mark', models.IntegerField(default=0, verbose_name='نمره')),
                ('answer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submit_answer', to='problembank.shortanswer', verbose_name='پاسخ')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autochecksubmit', to='problembank.problem', verbose_name='مسئله')),
                ('problem_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='autochecksubmit', to='problembank.problemgroup', verbose_name='دسته مسئله')),
                ('respondents', models.ManyToManyField(related_name='autochecksubmit', to='problembank.BankAccount', verbose_name='پاسخ دهنده (ها)')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShortAnswerProblem',
            fields=[
                ('problem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='problembank.problem')),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='problem', to='problembank.shortanswer', verbose_name='پاسخ صحیح')),
            ],
            bases=('problembank.problem',),
        ),
        migrations.CreateModel(
            name='DescriptiveProblem',
            fields=[
                ('problem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='problembank.problem')),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='problem', to='problembank.descriptiveanswer', verbose_name='پاسخ صحیح')),
            ],
            bases=('problembank.problem',),
        ),
    ]
