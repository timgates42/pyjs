var object = {};
type.__base__ = object;
type.__bases__ = [object];
type.__mro__ = [type, object];

object.__name__ = "object";
object.__bases__ = [];
object.__mro__ = [object];
object.__class__ = type;
object.$__id__ = get_hash_id();
object.__doc__ = "The most base type";

object.toString = function() {
    return "<class '"+this.__name__+"'>";
}

object.__getattribute__ = function(self, attr) {
    return self[attr];
}

object.__setattr__ = function(self, attr, val) {
    self[attr] = val;
}

// instantiates types (instances of classes)
object.__new__ = function(cls) {

    var __dict__ = {};

    function Instance() {
        return cls.get('__call__')(Instance, arguments)
    }
    Instance.__class__ = cls;
    Instance.__dict__ = __dict__;

    // inst.x -> inst.get('x');
    Instance.get = function(attr) {
        if (Instance.hasOwnProperty(attr)) {
            return Instance[attr];
        }
        return cls.get(attr);
    }

    // inst.x = 1 -> inst.set('x', 1);
    Instance.set = function(attr, value) {
        Instance[attr] = value;
    }

    return Instance;
}

object.__init__ = function() {}

object.$chainBuilder = function() { return object; }
