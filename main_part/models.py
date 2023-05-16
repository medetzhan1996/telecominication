from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=250)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Equipment(models.Model):
    title = models.CharField(max_length=50)
    processor = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    disk_array = models.CharField(max_length=50)
    nic = models.CharField(max_length=50)
    video_card = models.CharField(max_length=50)
    operation_system = models.CharField(max_length=50)
    processor_clock = models.CharField(max_length=50)
    total_phisical_memory = models.CharField(max_length=50)
    ram_size = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Service(models.Model):
    cost_per_month = models.DecimalField(max_digits=10, decimal_places=0)
    service_type = models.CharField(max_length=250)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def __str__(self):
        return self.service_type

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Order(models.Model):
    STATUS_CHOICES = (
        (1, 'ожидание'),
        (2, 'выполнено'),
        (3, 'отменено')
    )
    date_start = models.DateField()
    date_end = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES)


class TechnicalSupport(models.Model):
    STATUS_CHOICES = (
        (1, 'в обработке'),
        (2, 'выполнено'),
        (3, 'отменено')
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.client} / {self.date}'








