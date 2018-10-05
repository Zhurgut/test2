
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

        Complex comp1 = new Complex(0, 1, 'c');
        Complex comp2 = new Complex(0, -1, 'c');
        Complex comp3 = new Complex(0, 1, 'c');
        Complex comp4 = new Complex(0, 1, 'c');
        Complex comp5 = new Complex(0, 1, 'c');

        Complex added = Complex.add(comp1, comp2);
        Complex divided = Complex.divide(comp2, comp1);
        Complex multiplied = Complex.multiply(comp1, comp2);

        Complex.print(multiplied, 'p');

        // Complex.print(Complex.multiply(comp1, comp1), 'p');
        // Complex.print(Complex.multiply(comp1, Complex.multiply(comp1, comp1)), 'p');
        // Complex carl = Complex.multiply(comp1, Complex.multiply(comp1, comp1));
        // Complex.print(Complex.multiply(60, carl), 'c');
        // Complex.print(Complex.multiply(carl, carl), 'p');
        // Complex.print(nr1, 'c');
        // System.out.print("Distance " + Complex.absolute(nr1));

    }
}
