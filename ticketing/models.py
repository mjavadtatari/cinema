from django.db import models


# Create your models here.
class Movie(models.Model):
    """
    A Short Description about this Modeling
    """

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'

    name = models.CharField(max_length=100, verbose_name='عنوان')
    director = models.CharField(max_length=50, verbose_name='کارگردان')
    year = models.IntegerField(verbose_name='سال تولید')
    length = models.IntegerField(verbose_name='مدت زمان')
    description = models.TextField(verbose_name='توضیحات')
    poster = models.ImageField('پوستر', upload_to='movie_poster/')

    def __str__(self):
        return self.name


class Cinema(models.Model):
    """
    A Short Description about this Modeling
    """

    class Meta:
        verbose_name = 'سینما'
        verbose_name_plural = 'سینما'

    cinema_code = models.IntegerField(primary_key=True, verbose_name='کد اختصاصی')
    name = models.CharField(max_length=50, verbose_name='نام')
    city = models.CharField(max_length=30, default='تهران', verbose_name='شهر')
    capacity = models.IntegerField(verbose_name='ظرفیت')
    phone_number = models.CharField(max_length=20, null=True, verbose_name='تلفن')
    address = models.TextField(verbose_name='آدرس')
    image = models.ImageField('تصویر', upload_to='cinema_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class ShowTime(models.Model):
    """
    A Short Description about this Modeling
    """

    class Meta:
        verbose_name = 'سانس'
        verbose_name_plural = 'سانس'

    # choices between PROTECT, CASCADE, SET_NULL, SET_DEFAULT, SET(), DO_NOTHING
    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='فیلم')
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name='سینما')

    start_time = models.DateTimeField(verbose_name='زمان شروع')
    price = models.IntegerField(verbose_name='قیمت')
    salable_seats = models.IntegerField(verbose_name='صندلی های قابل فروش')
    free_seats = models.IntegerField(verbose_name='صندلی های آزاد')

    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELED = 6
    status_choices = (
        (SALE_NOT_STARTED, 'فروش آغاز نشده است'),
        (SALE_OPEN, 'در حال فروش بلیت'),
        (TICKETS_SOLD, 'بلیت ها تمام شد'),
        (SALE_CLOSED, 'فروش بلیت بسته شد'),
        (MOVIE_PLAYED, 'فیلم پخش شد'),
        (SHOW_CANCELED, 'سانس لغو شد'),
    )
    status = models.IntegerField(choices=status_choices, verbose_name='وضعیت')

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return '{} تومان'.format(self.price)

    def reserve_seats(self, seat_count):
        """
        Reserves Seats for a customer
        :param seat_count: An Integer as the number of seats to be reserved
        :return:
        """
        assert isinstance(seat_count, int) and seat_count > 0, 'تعداد صندلی ها صحیح وارد نشده است'
        assert self.status == ShowTime.SALE_OPEN, 'فروش برای این سانس فعال نیست'
        assert self.free_seats >= seat_count, 'تعداد صندلی های خالی کافی نیست'
        self.free_seats -= seat_count
        if self.free_seats == 0:
            self.status = ShowTime.TICKETS_SOLD
        self.save()


class Ticket(models.Model):
    """
    Represents one or more tickets, bought by a user in an order
    """

    class Meta:
        verbose_name = 'بلیت'
        verbose_name_plural = 'بلیت'

    showtime = models.ForeignKey('ShowTime', on_delete=models.PROTECT, verbose_name='سانس')
    customer = models.ForeignKey('accounts.Profile', on_delete=models.PROTECT, verbose_name='خریدار')
    seat_counter = models.IntegerField(verbose_name='تعداد صندلی')
    order_time = models.DateTimeField(verbose_name='زمان خرید', auto_now_add=True)

    def __str__(self):
        return "{} بلیت به نام {} برای فیلم {}".format(self.seat_counter, self.customer, self.showtime.movie)
