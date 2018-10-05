
// a program to check my work on complex numbers Yeah Woohoo

// Enter either Complex(angel, distance, 'p') (angle in radians from 0 - 2PI) for polar form
// or Complex(real, imag, 'c') for cartesian form
// variables are .real, .imag, .angle, .distance
// methods: .add(C, C) (C = Complex)
// .multiply(scalar, C) or .multiply(C, C)
// .divide(C1, C2) divides C1 by C2
// .print(C, 'p') prints polar form, .print(C, 'c') cartesian form
// .conjugate(C) returns C's conjugate
// .absolute(C) returns the absolute value (i.e. its distance from the origin)

public class complexmaths {
    public static void main(String[] args) {

<<<<<<< HEAD
        Complex comp1 = new Complex(0, 1, 'c');
        Complex comp2 = new Complex(0, -1, 'c');
        Complex comp3 = new Complex(0, 1, 'c');
        Complex comp4 = new Complex(0, 1, 'c');
        Complex comp5 = new Complex(0, 1, 'c');

        Complex added = Complex.add(comp1, comp2);
        Complex divided = Complex.divide(comp2, comp1);
        Complex multiplied = Complex.multiply(comp1, comp2);

        Complex.print(multiplied, 'p');

=======
        Complex u = new Complex(1, 3, 'c');
        Complex v = new Complex(2, -1, 'c');
        Complex w = new Complex(1, 4, 'c');
        Complex added = Complex.add(u, v);
        Complex added2 = Complex.add(added, w);
        Complex divided = Complex.divide(comp2, added);
        Complex polared = new Complex(Math.PI / 2, 5, 'p');
        Complex nr1 = new Complex(-2, 1, 'c');
        // Complex.print(comp1, 'c');
>>>>>>> 7ac70e10259ccea287cc141e9cce5960d3b077dd
        // Complex.print(Complex.multiply(comp1, comp1), 'p');
        // Complex.print(Complex.multiply(comp1, Complex.multiply(comp1, comp1)), 'p');
        // Complex carl = Complex.multiply(comp1, Complex.multiply(comp1, comp1));
        // Complex.print(Complex.multiply(60, carl), 'c');
        // Complex.print(Complex.multiply(carl, carl), 'p');
<<<<<<< HEAD
        // Complex.print(nr1, 'c');
        // System.out.print("Distance " + Complex.absolute(nr1));
=======
        Complex.print(added2, 'c');
        System.out.print("Distance " + Complex.absolute(nr1));
>>>>>>> 7ac70e10259ccea287cc141e9cce5960d3b077dd

    }
}
