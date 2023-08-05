"""


"""


class Context(object):
    def __init__(self, base=None):
        super(Context, self).__init__()
        self._base = base
        self._values = dict()
        self._deleted = set()

    def get(self, name, default=None):
        try:
            return self.__getitem__(name)
        except KeyError:
            return default

    def update(self, **values):
        # ! can't use self._values.update(values) here:
        # we need to iterate so that self._deleted
        # is updated accordingly !
        for k, v in values.items():
            self[k] = v

    def __getitem__(self, name):
        try:
            return self._values[name]
        except KeyError:
            if self._base is None or name in self._deleted:
                raise KeyError(name)
            return self._base[name]

    def __setitem__(self, name, value):
        try:
            self._deleted.remove(name)
        except KeyError:
            pass
        self._values[name] = value

    def __delitem__(self, name):
        if name in self._deleted:
            raise KeyError(
                'The name "{}" has already been deleted in this context.'.format(name)
            )
        try:
            del self._values[name]
        except KeyError:
            if self._base is not None:
                # Ensure their is something to delete
                try:
                    self._base[name]
                except KeyError:
                    raise
            else:
                raise
        self._deleted.add(name)

    def to_dict(self):
        d = {}
        if self._base is not None:
            d.update(self._base.to_dict())
        d.update(self._values)
        for key in self._deleted:
            del d[key]
        return d

    def edits(self):
        """
        Return a dict of added names, a dict of overridden names and a list of
        deleted names.
        """
        adds = dict()
        overs = dict()
        base = dict()
        if self._base is not None:
            base.update(self._base.to_dict())
        for k, v in self._values.items():
            try:
                base[k]
            except KeyError:
                adds[k] = v
            else:
                overs[k] = v
        return adds, overs, list(self._deleted)


class QAContext(Context):
    _KEY_ALLOW_AUTO_FIX = "SQARF::allow_auto_fix"
    _KEY_STOP_ON_FAIL = "SQARF::stop_on_fail"

    def stop_on_fail(self):
        return self.get(self._KEY_STOP_ON_FAIL, False)

    def set_stop_on_fail(self, stop_on_fail):
        """
        `stop_on_fail` can be True, False, or None for default behavior
        """
        if stop_on_fail is None:
            del self[self._KEY_STOP_ON_FAIL]
        else:
            self[self._KEY_STOP_ON_FAIL] = stop_on_fail

    def allow_auto_fix(self):
        return self.get(self._KEY_ALLOW_AUTO_FIX, False)

    def set_allow_auto_fix(self, allow_auto_fix):
        """
        `allow_auto_fix` can be True, False, or None for default behavior
        """
        if allow_auto_fix is None:
            del self[self._KEY_ALLOW_AUTO_FIX]
        else:
            self[self._KEY_ALLOW_AUTO_FIX] = allow_auto_fix
