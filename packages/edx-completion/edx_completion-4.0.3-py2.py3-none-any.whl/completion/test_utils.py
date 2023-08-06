"""
Common functionality to support writing tests around completion.
"""


from contextlib import contextmanager
from datetime import datetime

from django.contrib import auth
from edx_toggles.toggles.testutils import override_waffle_switch
import factory
from factory.django import DjangoModelFactory
from opaque_keys.edx.keys import UsageKey
from pytz import UTC

from . import waffle
from .models import BlockCompletion

User = auth.get_user_model()


def submit_completions_for_testing(user, block_keys):
    '''
    Allows tests to submit completion data for a given user and
    list of block_keys. The method completes the "block_keys" by adding them
    to the BlockCompletion model.
    '''
    for idx, block_key in enumerate(block_keys):
        BlockCompletion.objects.submit_completion(
            user=user,
            block_key=block_key,
            completion=1.0 - (0.2 * idx),
        )


class UserFactory(DjangoModelFactory):
    """
    A Factory for User objects.
    """
    class Meta:
        model = User
        django_get_or_create = ('email', 'username')

    _DEFAULT_PASSWORD = 'test'

    username = factory.Sequence('robot{}'.format)
    email = factory.Sequence('robot+test+{}@edx.org'.format)
    password = factory.PostGenerationMethodCall('set_password', _DEFAULT_PASSWORD)
    first_name = factory.Sequence('Robot{}'.format)
    last_name = 'Test'
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = datetime(2012, 1, 1, tzinfo=UTC)
    date_joined = datetime(2011, 1, 1, tzinfo=UTC)


class CompletionWaffleTestMixin:
    """
    Mixin to provide waffle switch overriding ability to child TestCase classes.
    """

    def override_waffle_switch(self, override):
        """
        Override the setting of the ENABLE_COMPLETION_TRACKING waffle switch
        for the course of the test.
        Parameters:
            override (bool): True if tracking should be enabled.
        """
        _waffle_overrider = override_waffle_switch(
            waffle.ENABLE_COMPLETION_TRACKING_SWITCH, override
        )
        _waffle_overrider.__enter__()
        self.addCleanup(_waffle_overrider.__exit__, None, None, None)


class CompletionSetUpMixin:
    """
    Mixin to provide set_up_completion() function to child TestCase classes.
    """

    COMPLETION_SWITCH_ENABLED = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.waffle_patcher = override_waffle_switch(
            waffle.ENABLE_COMPLETION_TRACKING_SWITCH, cls.COMPLETION_SWITCH_ENABLED
        )
        cls.waffle_patcher.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.waffle_patcher.__exit__(None, None, None)

    def setUp(self):
        super().setUp()
        self.block_key = UsageKey.from_string('block-v1:edx+test+run+type@video+block@doggos')
        self.context_key = self.block_key.context_key
        self.user = UserFactory()

    def set_up_completion(self):
        """
        Creates a stub completion record for a (user, course, block).
        """
        self.completion = BlockCompletion.objects.create(
            user=self.user,
            context_key=self.block_key.context_key,
            block_type=self.block_key.block_type,
            block_key=self.block_key,
            completion=0.5,
        )

    @contextmanager
    def override_completion_switch(self, enabled):
        """
        Overrides the completion-enabled waffle switch value within a context.
        """
        with override_waffle_switch(waffle.ENABLE_COMPLETION_TRACKING_SWITCH, enabled):
            yield
