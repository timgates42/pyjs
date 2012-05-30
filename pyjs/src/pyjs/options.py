from optparse import SUPPRESS_HELP, NO_DEFAULT

#-----------------------------------------------------------( group namespace )

class Groups(object):

    DEFAULT    = ('default', True)
    NODEFAULT  = ('default', False)
    DEBUG      = ('debug',   True)
    NODEBUG    = ('debug',   False)
    SPEED      = ('speed',   True)
    NOSPEED    = ('speed',   False)
    STRICT     = ('strict',  True)
    NOSTRICT   = ('strict',  False)

#----------------------------------------------------------( option container )

class Mappings(object):

    class Defaults(object):

        def __init__(self, mappings, *grps):
            self._mappings = mappings
            self._groups = set(grps) & set(mappings._groups_cache.keys())

        def __iter__(self):
            for grp in self._groups:
                for dest in self._mappings._groups_cache[grp]:
                    yield dest

        def __getitem__(self, key, exc=KeyError):
            for grp in self._groups:
                if key in self._mappings._groups_cache[grp]:
                    return grp[1]
            raise exc(key)

        __getattr__ = lambda k: self.__getitem__(k, exc=AttributeError)

        def iteritems(self):
            for o in self:
                yield (o, self[o])

        def items(self):
            return list(self.iteritems())

        def keys(self):
            return list(self)

        def get(self, key, *args):
            try:
                return self[key]
            except KeyError:
                if args:
                    return args[0]
                raise

    _opt_sig = ('names', 'aliases', 'groups', 'spec')
    _grp_sig = ('names', 'aliases', 'spec')
    _opt_sig_hash = set(_opt_sig)
    _grp_sig_hash = set(_grp_sig)

    def __init__(self):
        groups = {}
        for n, g in Groups.__dict__.iteritems():
            if not n.startswith('_'):
                groups[g] = set()
        super(self.__class__, self).__setattr__('_cache', dict())
        super(self.__class__, self).__setattr__('_groups', dict())
        super(self.__class__, self).__setattr__('_groups_cache', groups)

    def __iter__(self):
        for k in self._cache:
            yield k

    def __contains__(self, key):
        return key in self._cache

    def __getitem__(self, key, exc=KeyError):
        try:
            return self._cache[key]
        except KeyError:
            raise exc(key)

    def __setitem__(self, key, kwds):
        if not key:
            raise TypeError('Malformed name.')
        n = 'opt'
        if key.isupper():
            n = 'grp'
        new = '_%s' % n
        sig = '_%s_sig' % n
        sig_hash = '_%s_sig_hash' % n
        try:
            None in kwds
        except TypeError:
            raise TypeError('Must pass list or dict.')
        else:
            try:
                kwds[None]
            except TypeError:
                kwds= dict(zip(getattr(self, sig), kwds))
            except KeyError:
                pass
        if set(kwds.keys()) != getattr(self, sig_hash):
            raise TypeError('Malformed signature.')
        getattr(self, new)(key, **kwds)

    __getattr__ = lambda k: self.__getitem__(k, exc=AttributeError)
    __setattr__ = __setitem__

    def _opt(self, dest, **kwds):
        if not dest or set(kwds.keys()) != self._opt_sig_hash:
            raise TypeError('Malformed option signature.')
        spec = kwds['spec']
        spec['dest'] = dest
        if len(set(['action', 'callback', 'choices']) & set(spec.keys())) == 0:
            spec['action'] = 'store_true'
        for g in kwds['groups']:
            self._groups_cache[g].add(dest)
        if spec['default'] is True:
            self._groups_cache[Groups.DEFAULT].add(dest)
        elif spec['default'] is False:
            self._groups_cache[Groups.NODEFAULT].add(dest)
        no = kwds['nonames'] = set()
        if spec['default'] in (True, False):
            for n in kwds['names'] + kwds['aliases']:
                for repl in [('--with', '--without', 1),
                             ('--enable', '--disable', 1),
                             ('--', '--no-', 1)]:
                    rev = n.replace(*repl)
                    if rev != n:
                        no.add(rev)
        kwds['nonames'] = list(no)
        self._cache[dest] = kwds

    def _grp(self, dest, **kwds):
        if not dest or set(kwds.keys()) != self._grp_sig_hash:
            raise TypeError('Malformed group signature.')
        dest = getattr(Groups, dest)
        spec = kwds['spec']
        spec['action'] = 'callback'
        spec['callback'] = self._grp_set
        spec['callback_kwargs'] = {'_group': dest}
        no = kwds['nonames'] = set()
        for n in kwds['names'] + kwds['aliases']:
            for repl in [('--with', '--without', 1),
                         ('--enable', '--disable', 1),
                         ('--', '--no-', 1)]:
                rev = n.replace(*repl)
                if rev != n:
                    no.add(rev)
        kwds['nonames'] = list(no)
        self._groups[dest] = kwds

    def _grp_set(self, inst, opt, value, parser, *args, **kwds):
        no = False
        name, flag = kwds['_group']
        props = self._groups[name, flag]
        if opt in props['nonames']:
            no = True
        for f in (flag, not flag):
            flag_o = f
            if no:
                flag_o = not flag_o
            for dest in self._groups_cache[name, f]:
                setattr(parser.values, dest, flag_o)

    def iteritems(self):
        for o in self:
            yield (o, self[o])

    def items(self):
        return list(self.iteritems())

    def keys(self):
        return list(self)

    def get(self, key, *args):
        try:
            return self[key]
        except KeyError:
            if args:
                return args[0]
            raise

    def defaults(self, *grps):
        return self.Defaults(self, *grps)

    def bind(self, parser):
        opts = self._cache
        grps = self._groups
        ordered = []
        props = []
        for k, v in grps.iteritems():
            props.append(v)
        for k, v in opts.iteritems():
            ordered.append((v['names'][0], k))
        for k, v in sorted(ordered):
            props.append(opts[v])
        for p in props:
            variants = [(p['names'], {})]
            if p['aliases']:
                variants.append((p['aliases'], {'help': SUPPRESS_HELP}))
            if p['nonames']:
                vspec = {'help': SUPPRESS_HELP}
                if p['spec']['action'] == 'store_true':
                    vspec.update({'default': NO_DEFAULT,
                                  'action': 'store_false'})
                variants.append((p['nonames'], vspec))
            for args, updates in variants:
                spec = {}
                spec.update(p['spec'])
                spec.update(updates)
                parser.add_option(*args,
                                  **spec)

    def link(self, options):
        ret = {}
        for k in self:
            ret[k] = getattr(options, k)
        return ret

#----------------------------------------------------------( mapping instance )

all_compile_options = Mappings()

#---------------------------------------------------------( group definitions )

all_compile_options.DEFAULT = (
    ['--enable-default', '-D'],
    [],
    dict(help='(group) enable DEFAULT options')
)
all_compile_options.DEBUG = (
    ['--enable-debug', '-d'],
    ['--debug'],
    dict(help='(group) enable DEBUG options')
)
all_compile_options.SPEED = (
    ['--enable-speed', '-O'],
    [],
    dict(help='(group) enable SPEED options, degrade STRICT')
)
all_compile_options.STRICT = (
    ['--enable-strict', '-S'],
    ['--strict'],
    dict(help='(group) enable STRICT options, degrade SPEED')
)

#--------------------------------------------------------( option definitions )

all_compile_options.debug = (
    ['--enable-wrap-calls'],
    ['--debug-wrap'],
    [Groups.DEBUG, Groups.NOSPEED],
    dict(help='enable call site debugging [%default]',
         default=False)
)
all_compile_options.print_statements = (
    ['--enable-print-statements'],
    ['--print-statements'],
    [Groups.NOSPEED],
    dict(help='enable printing to console [%default]',
         default=True)
)
all_compile_options.function_argument_checking = (
    ['--enable-check-args'],
    ['--function-argument-checking'],
    [Groups.STRICT, Groups.NOSPEED],
    dict(help='enable function argument validation [%default]',
         default=False)
)
all_compile_options.attribute_checking = (
    ['--enable-check-attrs'],
    ['--attribute-checking'],
    [Groups.STRICT, Groups.NOSPEED],
    dict(help='enable attribute validation [%default]',
         default=False)
)
all_compile_options.getattr_support = (
    ['--enable-accessor-proto'],
    ['--getattr-support'],
    [Groups.STRICT, Groups.NOSPEED],
    dict(help='enable __get/set/delattr__() accessor protocol [%default]',
         default=True)
)
all_compile_options.bound_methods = (
    ['--enable-bound-methods'],
    ['--bound-methods'],
    [Groups.STRICT, Groups.NOSPEED],
    dict(help='enable proper method binding [%default]',
         default=True)
)
all_compile_options.descriptors = (
    ['--enable-descriptor-proto'],
    ['--descriptors'],
    [Groups.STRICT, Groups.NOSPEED],
    dict(help='enable __get/set/del__ descriptor protocol [%default]',
         default=False)
)
all_compile_options.source_tracking = (
    ['--enable-track-sources'],
    ['--source-tracking'],
    [Groups.DEBUG, Groups.STRICT, Groups.NOSPEED],
    dict(help='enable tracking original sources [%default]',
         default=False)
)
all_compile_options.line_tracking = (
    ['--enable-track-lines'],
    ['--line-tracking'],
    [Groups.DEBUG, Groups.STRICT],
    dict(help='enable tracking original sources: every line [%default]',
         default=False)
)
all_compile_options.store_source = (
    ['--enable-store-sources'],
    ['--store-source'],
    [Groups.DEBUG, Groups.STRICT],
    dict(help='enable storing original sources in javascript [%default]',
         default=False)
)
all_compile_options.inline_code = (
    ['--enable-inline-code'],
    ['--inline-code'],
    [Groups.SPEED],
    dict(help='enable bool/eq/len inlining [%default]',
         default=False)
)
all_compile_options.operator_funcs = (
    ['--enable-operator-funcs'],
    ['--operator-funcs'],
    [Groups.STRICT, Groups.NOSPEED],
    dict(help='enable operators-as-functions [%default]',
         default=True)
)
all_compile_options.number_classes = (
    ['--enable-number-classes'],
    ['--number-classes'],
    [Groups.STRICT, Groups.NOSPEED],
    dict(help='enable float/int/long as classes [%default]',
         default=False)
)
all_compile_options.create_locals = (
    ['--enable-locals'],
    ['--create-locals'],
    [],
    dict(help='enable locals() [%default]',
         default=False)
)
all_compile_options.stupid_mode = (
    ['--enable-stupid-mode'],
    ['--stupid-mode'],
    [],
    dict(help='enable minimalism by relying on javascript-isms [%default]',
         default=False)
)
all_compile_options.translator = (
    ['--use-translator'],
    ['--translator'],
    [],
    dict(help='override translator [%default]',
         action='store',
         choices=['proto', 'dict'],
         default='proto')
)
#all_compile_options.internal_ast = (
#    ['--enable-internal-ast'],
#    ['--internal-ast'],
#    [],
#    dict(help='enable internal AST parsing',
#         default=True)
#)

#----------------------------------------------------------( public interface )

get_compile_options = all_compile_options.link
add_compile_options = all_compile_options.bind


debug_options = all_compile_options.defaults(Groups.DEBUG, Groups.NODEBUG)
speed_options = all_compile_options.defaults(Groups.SPEED, Groups.NOSPEED)
pythonic_options = all_compile_options.defaults(Groups.STRICT, Groups.NOSTRICT)
