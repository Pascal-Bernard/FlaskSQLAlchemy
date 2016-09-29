# -*- coding: utf-8 -*-

__author__ = 'hubian'


class SunnycloudFactory:
    def __init__(self, allow_replace=False):
        """Create a new factory

        :param allow_replace: whether to replace existing provider with same feature. AssertionException will be raised it's
        False and more than one providers with same key(feature) are provided
        """
        self.providers = {}
        self.allow_replace = allow_replace

    def set_allow_replace(self, allow_replace):
        """Set the value of allow_replace"""
        self.allow_replace = allow_replace

    def provide(self, feature, provider, *args, **kwargs):
        """Add a provider to factory

        :type feature: str|unicode
        :param feature: key to store and get the object into/from the factory

        :type provider: object | callable
        :param provider: the object to be added.

        :Example:
            from *** import VMManager
            factory.provide("vm_manager", VMManager)
            factory.provide("vm_manager", VMManager, *init_args, **init_kwargs)

            # or:
            vmm = VMManager
            factory.provide("user_manager", vmm)

        """
        if not self.allow_replace:
            assert not self.providers.has_key(feature), "Duplicate feature: %r" % feature
        if callable(provider):
            def call():
                return provider(*args, **kwargs)
        else:
            def call():
                return provider
        self.providers[feature] = call

    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            raise KeyError, "Unknown feature named %r" % feature
        return provider()


factory = SunnycloudFactory()


def NoAssertion(obj):
    return True


class RequiredFeature(object):
    def __init__(self, feature, assertion=NoAssertion):
        """Create instance of RequiredFeature.

        Will get the actual target from factory upon the first call.

        :type feature: str|unicode
        :param feature: the key to get object from factory

        :Example:
            inst = RequiredFeature("user_manager")
            inst.some_method() # where user_manager.some_method will be called

        :raise:
            KeyError if feature doesn't exist in factory.
        """
        self.feature = feature
        self.assertion = assertion

    def __get__(self, obj, T):
        return self.result  # <-- will request the feature upon first call

    def __getattr__(self, name):
        self.result = self.request()
        if name == "result":
            return self.result
        else:
            return getattr(self.result, name)

    def request(self):
        obj = factory[self.feature]
        assert self.assertion(obj), \
            "The value %r of %r does not match the specified criteria" \
            % (obj, self.feature)
        return obj
