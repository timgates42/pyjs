var hash_id = 0;
function get_hash_id() {
    return ++hash_id;
}

function createClass(data, proto) {
    var c = Object.create(proto);
    for (var prop in data) {
        c[prop] = data[prop];
    }
    c.$__id__ = get_hash_id();
    return c;
}

function type(name, bases, dict) {

    if (arguments.length == 1) {
        return name.__class__;
    }

    if (bases.length === 0) {
        bases.push(object);
    }

    function Class() {
        var instance = cls.__new__(Class);
        cls.__init__(instance, arguments);
        return instance;
    }

    Class.__name__ = name;
    Class.__bases__ = bases;
    Class.__dict__ = dict;

    if (!dict.hasOwnProperty('__module__')) {
        // look in globals()
        dict.__module__ = '__main__';
    }

    Class.__class__ = type;
    Class.$__id__ = get_hash_id();

    Class.toString = function() {
        if (typeof Class.__dict__.__module__ === "string") {
            return "<class '"+Class.__dict__.__module__+"."+Class.__name__+"'>";
        } else {
            return "<class '"+Class.__name__+"'>";
        }
    }

    // Class.x -> Class.get('x');
    Class.get = function(attr) {

        if (attr === '__doc__') {
            return Class.__dict__.__doc__;
        }

        if (attr === '__module__') {
            return Class.__dict__.__module__;
        }

        if (attr === '__class__') {
            return Class.__class__;
        }

        if (attr === '__dict__') {
            return Class.__dict__;
        }

        if (attr === '__name__') {
            return Class.__name__;
        }

        if (attr === '__bases__') {
            return Class.__bases__;
        }

        if (attr === '__mro__') {
            return Class.__mro__;
        }

        // check metaclass for descriptors
        var metaattr = null;
        if (Class.__class__.hasOwnProperty(attr)) {
            metaattr = null; /* set it to any matches */
            /* check if match is descriptor if yes call and return result */
            return Class.__class__[attr];
        }

        // check own __dict__
        if (Class.__dict__.hasOwnProperty(attr)) {
            return Class.__dict__[attr];
        }

        // check bases
        if (attr in cls) {
            return cls[attr];
        }

        // check metaclass for ordinary attributes
        if (metaattr !== null) {
            return Class.__class__[attr];
        }

        throw AttributeError("type object '"+Class.__name__+"' has no attribute '"+attr+"'");
    }

    // Class.x = 1 -> Class.set('x', 1);
    Class.set = function(attr, value) {

        if (attr === '__mro__' || attr === '__id__') {
            throw 'TypeError: readonly attribute';
        }

        // __name__ && __bases__ are not visible in instances/lookups
        // so we return; after setting them on Class without
        // updating __dict__
        if (attr === '__name__') {
            Class.__name__ = value;
            return;
        }

        if (attr === '__bases__') {
            Class.__bases__ = value;
            Class.$setupMRO();
            return;
        }

        Class.__dict__[attr] = value;
        for (var prototype in prototypes) {
            prototypes[prototype][attr] = value;
        }

    }

    // cls is the initial chained prototype, it's used
    // when instantiating this class directly
    var cls = null;

    // prototypes is a registry of all copies of this class
    // that have different parent prototypes, these are used
    // for subclasses of this class, note that cls is in this
    // registry as well
    var prototypes = {};

    // this is used to notify subclasses when __bases__ changes
    var subclasses = [];

    // recurses through the MRO creating a prototype chain
    //   - the first time this is called it will be to
    //     boostrap the cls variable
    //   - on subsequence calls (when subclasses build up their prototypes)
    //     - if a chain link between this class and the super class
    //       already exists in the registry of prototypes then it
    //       will be returned
    //     - otherwise this class will be duplicated and its prototype
    //       will be set to the next class in the MRO chain
    Class.$chainBuilder = function(_mro) {

        // recurse to the end and work backwards
        var next = _mro.shift().$chainBuilder(_mro);

        // this will always be true in simple class hierarchies (single inheritance)
        if (cls !== null && cls.prototype === next) {
            return cls;

        // if chain path was already created before, return it
        } else if (prototypes.hasOwnProperty(next.$__id__)) {
            return prototypes[next.$__id__];

        }

        proto = createClass(dict, next);
        prototypes[next.$__id__] = proto;
        return proto;
    }

    // called when class is first created and anytime
    // the bases of this class or its super classes changes
    Class.$setupMRO = function() {

        Class.__mro__ = type.mro(Class);

        cls = Class.$chainBuilder(Class.__mro__.slice(1));

        for (var i = 0; i < subclasses.length; i++) {
            subclasses.$setupMRO();
        }
    }

    Class.$setupMRO();

    return Class;
}

type.$__id__ = get_hash_id();
type.__class__ = type;
type.__name__ = 'type';
type.__module__ = 'builtins';

type.toString = function() {
    return "<class '"+this.__name__+"'>";
}
