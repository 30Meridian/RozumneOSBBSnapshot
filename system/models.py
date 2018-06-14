import string
import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators
from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_permanent.models import PermanentModel
from machina.core.db.models import get_model

from .settings import MEDIA_ROOT
from .validators import validate_file_extension

from django.contrib.auth.models import Group


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                ],
                                error_messages={
                                    'unique': _("A user with that username already exists."),
                                })
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    middle_name = models.CharField(max_length=64, verbose_name=_('middle name'))
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={
                                  'unique': _("A user with that email already exists."),
                              })
    phone = models.CharField(max_length=64, verbose_name=_('user phone'))

    condominiums = models.ManyToManyField('Condominium', verbose_name=_('user condominium'))
    owned = models.ManyToManyField('ObjectRegistry', verbose_name=_('owned'))


    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    objects = UserManager()

    # this stuff is needed to use this model with django auth as a custom user class
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_first_condominium(self):
        return self.condominiums.all()[0]

    @property
    def residential_premise(self):
        return CondominiumResidentialPremise.objects.filter(user=self).all()

    @property
    def non_residential_premise(self):
        return CondominiumNonResidentialPremise.objects.filter(user=self).all()

    @property
    def has_condominiums(self):
        return True if len(self.condominiums.all()) else False

    def is_manager(self):
        return Condominium.objects.filter(manager=self.id).values_list('slug', flat=True)

    def condominiums_list(self):
        return self.condominiums.all().values_list('id', flat=True)

    def is_editor(self):
        return True if 'editor' in self.groups.all().values_list('name', flat=True) else False

    def __str__(self):
        return self.last_name + ' ' + self.first_name + (' ' + self.middle_name if self.middle_name else '')

    class Meta:
        managed = True
        abstract = False
        db_table = 'auth_user'
        verbose_name = _('auth user')
        verbose_name_plural = _('auth user')


class City(models.Model):
    code = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=2)
    prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=256)
    specialized_name = models.CharField(max_length=256)
    is_residential = models.BooleanField()
    parent = models.ForeignKey('self', db_column='parent', null=True)

    def correct_name(self):
        lower_name = self.name.lower()
        spliced = lower_name.split(' ')
        res = ''

        if self.prefix:
            res += spliced[0]
            spliced = spliced[1:]
            for name_part in spliced:
                res += ' ' + string.capwords(name_part)
        else:
            if len(spliced) == 2:
                res = string.capwords(spliced[0]) + ' ' + spliced[1]
            else:
                res = string.capwords(lower_name)
        return res

    def __str__(self):
        return  self.correct_name() + (' ' + str(self.parent) if self.parent else '')

    class Meta:
        db_table = 'city'
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class ObjectTypes(models.Model):
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return '{}'.format(_(self.title))

    class Meta:
        unique_together = ('title', 'category')
        db_table = 'object_types'
        verbose_name = _('object type')
        verbose_name_plural = _('object types')


class ObjectRegistry(models.Model):
    title = models.CharField(max_length=64, null=True, blank=True, default='')
    condominium = models.ForeignKey('Condominium')
    type = models.ForeignKey(ObjectTypes, db_column='type')
    datetime_created = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey(User, db_column='user_created', related_name='created')
    datetime_changed = models.DateTimeField(auto_now_add=True)
    user_changed = models.ForeignKey(User, db_column='user_changed', related_name='changed')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        db_table = 'object_registry'
        verbose_name = _('object registry')
        verbose_name_plural = _('objects registry')


class ModulesManager(models.Manager):
    def get_queryset(self):
        return super(ModulesManager, self).get_queryset().filter(parent=None)


class Modules(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    icon = models.CharField(max_length=64, blank=True, null=True, default='fa fa-plus')
    parent = models.ForeignKey('self', null=True)

    objects = ModulesManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'modules'
        verbose_name = _('module')
        verbose_name_plural = _('modules')

    def __str__(self):
        return "{}".format(_(self.title))


def get_document_path(instance, filename):
    ext = os.path.splitext(filename)
    return os.path.join(os.path.join('statuts', instance.slug), 'statut' + ext[1])


class Condominium(PermanentModel):
    name = models.CharField(max_length=64, verbose_name=_('name condominium'))
    slug = models.CharField(max_length=64, unique=True, verbose_name=_('slug condominium'))
    city = models.ForeignKey(City, db_column='city', on_delete=models.CASCADE, verbose_name=_('city'))

    document = models.FileField(upload_to=get_document_path, validators=[validate_file_extension],
                                verbose_name=_('condominium constitution'), blank=True, default='')
    legal_address = models.CharField(max_length=128, verbose_name=_('legal address'))
    description = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('description condominium'))

    votes = models.IntegerField(default=10, verbose_name=_('votes condominium'))
    problem_days = models.IntegerField(default=7, verbose_name=_('problem condominium'))
    ideas_days = models.IntegerField(default=30, verbose_name=_('ideas_days condominium'))
    ideas_number_templ = models.CharField(max_length=64, blank=True, null=True, default='10/%s',
                                          verbose_name=_('ideas number condominium'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Registration date"))
    manager = models.ManyToManyField(User, verbose_name=_('manager condominium'))
    public_ideas = models.BooleanField(default=True, verbose_name=_('Public ideas'),
                                       help_text=_('Allows by default to view ideas for users from other condominiums '))
    public_news = models.BooleanField(default=True, verbose_name=_('Public news'),
                                      help_text=_('Allows by default to view news for users from other condominiums '))
    public_polls = models.BooleanField(default=True, verbose_name=_('Public polls'),
                                       help_text=_('Allows by default to view polls for users from other condominiums '))
    public_problems = models.BooleanField(default=True, verbose_name=_('Public problems'),
                                          help_text=_('Allows by default to view problems for users from other condominiums '))

    latitude = models.CharField(max_length=64, blank=True)
    longitude = models.CharField(max_length=64, blank=True)


    def __str__(self):
        return '{} ({} {})'.format(self.name, self.city.name, self.legal_address)


    class Meta:
        db_table = 'condominium'
        verbose_name = _('condominium')
        verbose_name_plural = _('condominiums')


class CondominiumPosition(models.Model):
    POSITIONS = (
        ('chairman', _('Сhairman')),
        ('vice-chairman', _('Vice-Chairman')),
        ('secretary', _('Secretary')),
        ('trustee', _('Trustee')),
        ('audit-member', _('Audit team member')),
        ('member', _('Member')),
        ('inhabitant', _('Inhabitant'))
    )

    user = models.ForeignKey(User, db_column='user', on_delete=models.CASCADE, verbose_name=_('user'))
    condominium = models.ForeignKey(Condominium, db_column='condominium', on_delete=models.CASCADE,
                                    verbose_name='condominium')
    position = models.CharField(max_length=16, choices=POSITIONS, verbose_name=_('position'))

    def __str__(self):
        return self.position

    class Meta:
        db_table = 'condominium_position'


class CondominiumModules(models.Model):
    condominium = models.ForeignKey(Condominium, verbose_name=_('condominium'), on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, verbose_name=_('module'), on_delete=models.CASCADE)
    use = models.BooleanField(verbose_name=_('use'))
    weight = models.IntegerField(verbose_name=_('weight'))

    def __str__(self):
        return str(self.condominium) + ' ' + str(self.module)

    class Meta:
        db_table = 'condominium_modules'
        verbose_name = _('condominium module')
        verbose_name_plural = _('condominium modules')


class CondominiumHouse(models.Model):
    condominium = models.ForeignKey(Condominium, db_column='condominium', on_delete=models.CASCADE,
                                    verbose_name=_('house condominium '))
    name = models.CharField(max_length=64, blank=True, verbose_name=_('house name '))
    address = models.CharField(max_length=128, db_column='address', verbose_name=_('house address '))
    area = models.FloatField(validators=[MinValueValidator(0.01)], verbose_name=_('house area '))
    residential_area = models.FloatField(validators=[MinValueValidator(0)],
                                         verbose_name = _('house residential area '))
    entrance_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_('house entrance count '))
    min_floors = models.IntegerField(validators=[MinValueValidator(1)], verbose_name=_('house min floors '))
    max_floors = models.IntegerField(validators=[MinValueValidator(1)], verbose_name=_('house max floors '))
    residential_count = models.IntegerField(validators=[MinValueValidator(0)],
                                            verbose_name=_('house residential count '))
    elevators_count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_('house elevators count '))
    object_registry = models.ForeignKey(ObjectRegistry, null=True, verbose_name=_('object_registry'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('house description '))

    class Meta:
        db_table = 'condominium_house'
        verbose_name = _('house')
        verbose_name_plural = _('houses')

    def __str__(self):
        return self.address + ' ' or ''


class CondominiumPorch(models.Model):
    house = models.ForeignKey(CondominiumHouse, db_column='house', on_delete=models.CASCADE,
                              verbose_name=_('porch house'))
    number = models.IntegerField(verbose_name=_('porch number'))
    name = models.CharField(max_length=64, blank=True, verbose_name=_('porch name'))
    floors_count = models.IntegerField(verbose_name=_('porch floors_count'))
    residential_count = models.IntegerField(verbose_name=_('porch residential_count'),blank=True, null=True)
    non_residential_count = models.IntegerField(default=0, verbose_name=_('porch non_residential_count'),blank=True, null=True)
    lighting_points = models.IntegerField(verbose_name=_('porch lighting_points'),blank=True, null=True)
    elevators_count = models.IntegerField(verbose_name=_('porch elevators_count'),blank=True, null=True)
    object_registry = models.ForeignKey(ObjectRegistry, null=True, verbose_name=_('object_registry'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('porch description'))

    class Meta:
        db_table = 'condominium_porch'
        verbose_name = _('porch')
        verbose_name_plural = _('porches')

    def __str__(self):
        return '{}, {} {}'.format(str(self.house), _('Porch'), (str(self.number) + ' ' or ''))


class CondominiumFloor(models.Model):
    porch = models.ForeignKey(CondominiumPorch, db_column='porch', on_delete=models.CASCADE,
                              verbose_name=_('floor porch'))
    type = models.ForeignKey(ObjectTypes, db_column='type', verbose_name=_('floor type'))
    number = models.IntegerField(verbose_name=_('floor number'))
    name = models.CharField(max_length=32, blank=True, verbose_name=_('floor name'))
    residential_count = models.IntegerField(verbose_name=_('floor residential_count'),blank=True, null=True)
    non_residential_count = models.IntegerField(default=0, verbose_name=_('floor non_residential_count'),blank=True, null=True)
    lighting_points = models.IntegerField(default=1, verbose_name=_('floor lighting_points'),blank=True, null=True)
    object_registry = models.ForeignKey(ObjectRegistry, null=True, verbose_name=_('object_registry'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('floor description'))

    class Meta:
        db_table = 'condominium_floor'
        verbose_name = _('floor')
        verbose_name_plural = _('floors')

    def __str__(self):
        return '{}, {} {}'.format(str(self.porch), _('Fl.'), (str(self.number) + ' ' or ''))


class CondominiumNonResidentialPremise(models.Model):
    user = models.ForeignKey(User, db_column='user', verbose_name=_('non residential owner'))
    house = models.ForeignKey(CondominiumHouse, db_column='house', verbose_name=_('non residental house'))
    floor = models.ForeignKey(CondominiumFloor, db_column='floor', verbose_name=_('non residental floor'))
    type = models.ForeignKey(ObjectTypes, db_column='type', verbose_name=_('non residental type'))
    number = models.CharField(max_length=32, blank=True, verbose_name=_('non residential number or name'))
    area = models.FloatField(verbose_name=_('non residental area'))
    object_registry = models.ForeignKey(ObjectRegistry, null=True, verbose_name=_('object_registry'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('non residental description'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.house = self.floor.porch.house
        super(CondominiumNonResidentialPremise, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'condominium_non_residential_premise'
        verbose_name = _('condominium non residential premise')
        verbose_name_plural = _('condominium non residential premises')

    def __str__(self):
        return '{}, {}, # {}'.format(str(self.floor), str(self.type) , str(self.number))


class CondominiumResidentialPremise(models.Model):
    user = models.ForeignKey(User, db_column='user', verbose_name=_('residential owner'))
    house = models.ForeignKey(CondominiumHouse, db_column='house', verbose_name=_('residental house'))
    floor = models.ForeignKey(CondominiumFloor, db_column='floor', verbose_name=_('residental floor'))
    type = models.ForeignKey(ObjectTypes, db_column='type', verbose_name=_('residental type '))
    number = models.CharField(max_length=32, blank=True, verbose_name=_('residential number or name'))
    area = models.FloatField(verbose_name=_('residental area '))
    residential_area = models.FloatField(verbose_name=_('residental residential area '))
    heating_area = models.FloatField(verbose_name=_('residental heating area '))
    rooms_count = models.IntegerField(verbose_name=_('residental rooms count '))
    residents_count = models.IntegerField(verbose_name=_('residental residents_count '))
    pets_count = models.IntegerField(verbose_name=_('residental pets count '))
    object_registry = models.ForeignKey(ObjectRegistry, null=True, verbose_name=_('object_registry'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('residental description '))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.house = self.floor.porch.house
        super(CondominiumResidentialPremise, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'condominium_residential_premise'
        verbose_name = _('condominium residential premise')
        verbose_name_plural = _('condominium residential premises')

    def __str__(self):
        return '{} {} {}'.format(str(self.floor), str(self.type) , str(self.number))


class EngineeringService(models.Model):
    condominium = models.ForeignKey(Condominium, db_column='condominium', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    # subcontractor
    subsidy = models.BooleanField(default=False)
    value = models.FloatField()
    measurement_units = models.CharField(max_length=64)
    determine = models.CharField(max_length=128)

    datetime_crated = models.DateTimeField(auto_now_add=True)
    datetime_changed = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'engineering_service'
        verbose_name = _('service')
        verbose_name_plural = _('services')

    def __str__(self):
        return self.name


class CondominiumConnectedUtility(models.Model):
    object_registry = models.ForeignKey(ObjectRegistry, db_column='object_registry', on_delete=models.CASCADE,
                                        verbose_name=_('object registry'))
    service = models.ForeignKey(EngineeringService, db_column='service', on_delete=models.CASCADE,
                                verbose_name=_('service'))
    subsidy = models.FloatField(default=0.0)
    start_value = models.FloatField(verbose_name=_('start value'))

    class Meta:
        db_table = 'condominium_connected_utilities'
        verbose_name = _('utilities')
        verbose_name_plural = _('utilities')

    def __str__(self):
        return '{}'.format(self.calculation_poins_count)


class CondominiumConnectedUtiliteLog(models.Model):
    utility = models.ForeignKey(CondominiumConnectedUtility, db_column='utilite', on_delete=models.CASCADE)
    current_value = models.FloatField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'condominium_connected_utilities_log'
        verbose_name = _('utility log')
        verbose_name_plural = _('utility logs')

    def __str__(self):
        return str(self.current_value)


class CondominiumCommonArea(models.Model):
    object_registry = models.ForeignKey(ObjectRegistry, db_column='object_registry', on_delete=models.CASCADE, verbose_name=_('object_registry'))
    type = models.ForeignKey(ObjectTypes, db_column='type', verbose_name=_('common area type'))
    area = models.FloatField(verbose_name=_('common area-area'))
    description = models.CharField(max_length=255, verbose_name=_('common area description'),blank=True)

    class Meta:
        db_table = 'condominium_common_area'
        verbose_name = _('Common area')
        verbose_name_plural = _('Common Areas')

    def __str__(self):
        return '{}'.format(self.description[:80])


class CondominiumInfrastructure(models.Model):
    object_registry = models.ForeignKey(ObjectRegistry, db_column='object_registry', on_delete=models.CASCADE, verbose_name=_('object_registry'))
    type = models.ForeignKey(ObjectTypes, db_column='type', verbose_name=_('infrastructure type'))
    area = models.FloatField(verbose_name=_('infrastructure area'))
    description = models.CharField(max_length=255,  verbose_name=_('infrastructure description'),  blank=True, null=True)

    class Meta:
        db_table = 'condominium_infrastructure'
        verbose_name = _('infrastructure')
        verbose_name_plural = _('infrastructures')

    def __str__(self):
        return '{}'.format(self.description[:80])

from condominium_management.models import ManagementPages

class ProxyManagementPages(ManagementPages):
    class Meta:
        proxy = True
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

# Models signals:

@receiver(post_save, sender=Condominium)
def on_condominium_create(sender, instance, created, **kwargs):
    if created:
        weight = 0
        for module in Modules.objects.all():
            weight += 1
            CondominiumModules.objects.create(condominium=instance, module=module, use=True, weight=weight)

        from condominium_management.models import ManagementPages
        ManagementPages.objects.create(condominium=instance, slug='tariffs', title=_('Tariffs'), content='')
        ManagementPages.objects.create(condominium=instance, slug='debtors', title=_('Debtors'), content='')
        ManagementPages.objects.create(condominium=instance, slug='ourmasters', title=_('Our masters'), content='')
        ManagementPages.objects.create(condominium=instance, slug='ourcontacts', title=_('Our contacts'), content='')

        directory = os.path.join(os.path.join(MEDIA_ROOT, 'documents'), str(instance.slug))
        if not os.path.exists(directory):
            os.makedirs(directory)

        Forum = get_model('forum', 'Forum')
        ForumPermission = get_model('forum_permission', 'ForumPermission')
        GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')

        Forum.objects.create(condominium = instance, type=0, name=_('Base users forum'),
                             description=_('Basic forum for our Condominium.'))

        perms = ForumPermission.objects.all()[:19]
        group_user = Group.objects.get(name='User')
        group_manager = Group.objects.get(name='manager')
        forum = Forum.objects.get(condominium=instance)
        if not GroupForumPermission.objects.filter(forum=forum):
            for perm in enumerate(perms):
                GroupForumPermission.objects.create(
                    permission=perm[1], forum=forum, group=group_manager)
                if perm[0] < 14:
                    GroupForumPermission.objects.create(
                        permission=perm[1], forum=forum, group=group_user)
