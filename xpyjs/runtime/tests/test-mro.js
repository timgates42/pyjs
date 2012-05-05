// Examples taken from http://www.python.org/getit/releases/2.3/mro/

// makes assertion errors readable
Object.prototype.toString = function() { return this.name; }


var O = object; O.name = 'O';

function testObjectMRO() {
    assertEquals([O], O.__mro__);
}

//
// Example 1
//
//   >>> O = object
//   >>> class F(O): pass
//   >>> class E(O): pass
//   >>> class D(O): pass
//   >>> class C(D,F): pass
//   >>> class B(D,E): pass
//   >>> class A(B,C): pass
//   
//   
//                             6
//                            ---
//   Level 3                 | O |                  (more general)
//                         /  ---  \
//                        /    |    \                      |
//                       /     |     \                     |
//                      /      |      \                    |
//                     ---    ---    ---                   |
//   Level 2        3 | D | 4| E |  | F | 5                |
//                     ---    ---    ---                   |
//                      \  \ _ /       |                   |
//                       \    / \ _    |                   |
//                        \  /      \  |                   |
//                         ---      ---                    |
//   Level 1            1 | B |    | C | 2                 |
//                         ---      ---                    |
//                           \      /                      |
//                            \    /                      \ /
//                              ---
//   Level 0                 0 | A |                (more specialized)
//                              ---
//   

function testExample1() {
    var F = {}; F.name='F';
    F.__bases__ = [O];
    F.__mro__ = type.mro(F);
    assertEquals([F,O], F.__mro__);

    var E = {}; E.name='E';
    E.__bases__ = [O];
    E.__mro__ = type.mro(E);
    assertEquals([E,O], E.__mro__);

    var D = {}; D.name='D';
    D.__bases__ = [O];
    D.__mro__ = type.mro(D);
    assertEquals([D,O], D.__mro__);

    var C = {}; C.name='C';
    C.__bases__ = [D,F];
    C.__mro__ = type.mro(C);
    assertEquals([C,D,F,O], C.__mro__);

    var B = {}; B.name='B';
    B.__bases__ = [D,E];
    B.__mro__ = type.mro(B);
    assertEquals([B,D,E,O], B.__mro__);

    var A = {}; A.name='A';
    A.__bases__ = [B,C];
    A.__mro__ = type.mro(A);
    assertEquals([A,B,C,D,E,F,O], A.__mro__);
}

//
// Example 2
//
//   >>> O = object
//   >>> class F(O): pass
//   >>> class E(O): pass
//   >>> class D(O): pass
//   >>> class C(D,F): pass
//   >>> class B(E,D): pass
//   >>> class A(B,C): pass
//   
//   
//                              6
//                             ---
//   Level 3                  | O |                  (more general)
//                          /  ---  \
//                         /    |    \                     |
//                        /     |     \                    |
//                       /      |      \                   |
//                     ---     ---     ---                 |
//   Level 2        2 | E | 4 | D |   | F | 5              |
//                     ---     ---     ---                 |
//                      \      / \     /                   |
//                       \    /   \   /                    |
//                        \  /     \ /                     |
//                         ---     ---                     |
//   Level 1            1 | B |   | C | 3                  |
//                         ---     ---                     |
//                           \      /                      |
//                            \    /                      \ /
//                              ---
//   Level 0                 0 | A |                (more specialized)
//                              ---
//   

function testExample2() {
    var F = {}; F.name='F';
    F.__bases__ = [O];
    F.__mro__ = type.mro(F);
    assertEquals([F,O], F.__mro__);

    var E = {}; E.name='E';
    E.__bases__ = [O];
    E.__mro__ = type.mro(E);
    assertEquals([E,O], E.__mro__);

    var D = {}; D.name='D';
    D.__bases__ = [O];
    D.__mro__ = type.mro(D);
    assertEquals([D,O], D.__mro__);

    var C = {}; C.name='C';
    C.__bases__ = [D,F];
    C.__mro__ = type.mro(C);
    assertEquals([C,D,F,O], C.__mro__);

    var B = {}; B.name='B';
    B.__bases__ = [E,D];
    B.__mro__ = type.mro(B);
    assertEquals([B,E,D,O], B.__mro__);

    var A = {}; A.name='A';
    A.__bases__ = [B,C];
    A.__mro__ = type.mro(A);
    assertEquals([A,B,E,C,D,F,O], A.__mro__);
}
