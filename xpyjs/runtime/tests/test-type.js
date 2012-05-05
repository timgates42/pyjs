function testTypeToString() {
    assertEqual("<class 'type'>", type.toString());
    assertEqual("<class 'type'>", type.__class__.toString());
    assertEqual("<class 'type'>", type(type).toString());
}

function testTypeID() {
    assertEqual(1, id(type));
}

function testTypeDIR() {
    assertEqual(['__class__','__name__','__module__','__base__','__bases__','mro'], dir(type));
}
function testTypeMRO() {
    assertEqual([type, object], type.__mro__);
}

function testBasicNewType() {
    var A = type('A', [], {});

    assertEqual("<class '__main__.A'>", A.toString());
    assertEqual("<class 'type'>", type(A).toString());

    assertEqual("A", A.__name__);
    assertEqual("A", A.get('__name__'));

    assertEqual(null, A.__doc__);
    assertEqual(null, A.get('__doc__'));

    assertEqual("__main__", A.__dict__.__module__);
    assertEqual("__main__", A.get('__module__'));

    assertEqual([object], A.__bases__);
    assertEqual([object], A.get('__bases__'));

    assertEqual([A, object], A.__mro__);
    assertEqual([A, object], A.get('__mro__'));
}

var Animal = type(
        'Animal', [object], {
            "move": function() { return "generic movement"; },
            "live": function() { return "alive!"; }
        }
);

var Fish = type(
        'Fish', [Animal], {
            "move": function() { return "swimming"; }
        }
);

var Mammal = type(
        'Mammal', [Animal], {
        }
);

var Dog = type(
        'Dog', [Mammal], {
            "speak": function() { return "bark!"; },
            "move": function() { return "running"; }
        }
);
var Cat = type(
        'Cat', [Mammal], {
            "speak": function() { return "meow!"; },
            "move": function() { return "climbing"; },
            "__call__": function() { return "calling all cats"; }
        }
);

var Pet = type('Pet', [object],{
            "__name__": 'it',
            "__module__": 'other',
            "feed": function() { return "feeding pet"; },
            "move": function() { return "rolling on back"; }
        }
);

var Crazy = type('Crazy', [],{
            "do_stuff": function() { return "doing crazy stuff"; }
        }
);

var PetCat = type(
        'PetCat', [Cat, Pet], {
            'speak': function() { return "purrr..."; }
        }
);

function testBasesModification() {
    assertEqual([Cat, Pet], PetCat.__bases__);
    assertEqual([PetCat, Cat, Mammal, Animal, Pet, object], PetCat.get('__mro__'));
    assertEqual(Cat.__dict__.move, PetCat.get('move'));
    assertRaisesJSError(function() {PetCat.get('do_stuff')});

    PetCat.set('__bases__', [Pet, Cat, Crazy])

    assertEqual([Pet, Cat, Crazy], PetCat.__bases__);
    assertEqual([PetCat, Pet, Cat, Mammal, Animal, Crazy, object], PetCat.get('__mro__'));
    assertEqual(Pet.__dict__.move, PetCat.get('move'));
    assertEqual(Crazy.__dict__.do_stuff, PetCat.get('do_stuff'));
}

function testComplexNewType() {
    assertEqual("<class 'type'>", type(PetCat).toString());

    assertEqual(null, PetCat.__doc__);
    assertEqual(null, PetCat.get('__doc__'));

    assertEqual([Cat, Pet], PetCat.__bases__);
    assertEqual([Cat, Pet], PetCat.get('__bases__'));

    assertEqual([PetCat, Cat, Mammal, Animal, Pet, object], PetCat.__mro__);
    assertEqual([PetCat, Cat, Mammal, Animal, Pet, object], PetCat.get('__mro__'));

    assertEqual(PetCat.__dict__.speak, PetCat.get('speak'));
    assertEqual(Cat.__dict__.move, PetCat.get('move'));
    assertEqual(Animal.__dict__.live, PetCat.get('live'));
    assertEqual(Pet.__dict__.feed, PetCat.get('feed'));
}

function testName() {
    assertEqual("PetCat", PetCat.__name__);
    assertEqual("PetCat", PetCat.get('__name__'));
    assertEqual("<class '__main__.PetCat'>", PetCat.toString());

    // overriding __name__ in class declaration only affects instances
    assertEqual("Pet", Pet.__name__);
    assertEqual("Pet", Pet.get('__name__'));
    assertEqual("<class 'other.Pet'>", Pet.toString());

    Pet.set('__name__', 'that');

    assertEqual("that", Pet.__name__);
    assertEqual("that", Pet.get('__name__'));
    assertEqual("<class 'other.that'>", Pet.toString());
}

function testModule() {
    assertEqual("__main__", PetCat.__dict__.__module__);
    assertEqual("__main__", PetCat.get('__module__'));

    assertEqual("other", Pet.__dict__.__module__);
    assertEqual("other", Pet.get('__module__'));
    assertEqual("<class 'other.Pet'>", Pet.toString());

    Pet.set('__module__', 'that');

    assertEqual("that", Pet.__dict__.__module__);
    assertEqual("that", Pet.get('__module__'));
    assertEqual("<class 'that.Pet'>", Pet.toString());
}

