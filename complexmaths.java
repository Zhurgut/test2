
// a program to check my homework on complex numbers Yeah Woohoo

// Enter either Complex(angel, distance, 'p') (angle in radians from 0 - 2PI) for polar form
// or Complex(real, imag, 'c') for cartesian form
// variables are .real, .imag, .angle, .distance
// methods: .add(C, C) (C = Complex)
// .multiply(scalar, C) or .multiply(C, C)
// .divide(C1, C2) divides C1 by C2
// .print(C, 'p') prints polar form, .print(C, 'c') cartesian form
// .conjugate(C) returns C's conjugate

public class complexmaths {
    public static void main(String[] args) {

        Complex u = new Complex(1, 3, 'c');
        Complex v = new Complex(2, -1, 'c');
        Complex w = new Complex(1, 4, 'c');
        Complex nr = new Complex(Math.PI * 4 / 3, 2, 'p');
        Complex added = Complex.add(u, v);
        Complex added2 = Complex.add(added, w);
        Complex mult = Complex.multiply(w, v);
        Complex divided = Complex.divide(v, u);
        Complex polared = new Complex(Math.PI / 2, 5, 'p');
        Complex nr1 = new Complex(-2, 1, 'c');
        // Complex.print(comp1, 'c');
        // Complex.print(Complex.multiply(comp1, comp1), 'p');
        // Complex.print(Complex.multiply(comp1, Complex.multiply(comp1, comp1)), 'p');
        // Complex carl = Complex.multiply(comp1, Complex.multiply(comp1, comp1));
        // Complex.print(Complex.multiply(60, carl), 'c');
        // Complex.print(Complex.multiply(carl, carl), 'p');
        //System.out.println(Math.sin(Math.PI / 4) % (Math.PI * 2));
        Complex.print(nr, 'c');

        System.out.print("Distance " + Complex.absolute(nr));

    }
}
