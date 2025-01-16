from django.db import models


class TelegramChanell(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    now_parsing = models.BooleanField(default=False)
    frequency = models.BigIntegerField(default=30*60) #freq of updating

class LastMessages(models.Model):
    channel = models.ForeignKey(TelegramChanell, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField()
    media_url = models.TextField(blank=True, null=True)
    is_add = models.BooleanField(default=False)

    def __str__(self):
        return f"Last message from {self.channel.name}"

class FinalMessages(models.Model):
    title = models.CharField()
    message = models.TextField()
    last_messages = models.ManyToManyField(LastMessages, verbose_name=("Из каких сообщений был составлен пост"))
    date = models.DateTimeField()

    def __str__(self) -> str:
        return f"Final message {self.date}"
