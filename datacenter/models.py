from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        if self.leaved_at:
            return self.leaved_at - self.entered_at
        return localtime() - self.entered_at

    def format_duration(self) -> str:
        seconds_in_hour = 3600
        seconds_in_minute = 60
        formatted_duration = ''
        td = self.get_duration()
        days, seconds = td.days, td.seconds
        if days:
            formatted_duration += f'{days:02d} д.'
        hours = seconds // seconds_in_hour
        minutes = (seconds % seconds_in_hour) // seconds_in_minute
        formatted_duration += f'{hours:02d} ч {minutes:02d} мин'
        return formatted_duration

    def is_long(self, minutes=60):
        seconds_limit = minutes * 60
        return self.get_duration().total_seconds() > seconds_limit
