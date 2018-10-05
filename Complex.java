public class Complex {
    public static void main(String[] args) {

    }

    double real;
    double imag;
    double angle;
    double distance;

    Complex(double rearg, double imdist, char form) {
        if (form == 'c') {
            real = rearg;
            imag = imdist;
            distance = Math.sqrt(rearg * rearg + imdist * imdist);
            if (real >= 0 && imag >= 0) { //first quadrant
                angle = Math.asin(imdist / distance);
            } else if (real < 0 && imag >= 0) { //second (i think)
                angle = Math.acos(rearg / distance);
            } else if (real < 0 && imag < 0) { //third
                angle = Math.acos(-rearg / distance) + Math.PI;
            } else { //the fourth and final
                angle = Math.asin(imdist / distance) + Math.PI * 2 + 0.000001;
            }
            angle = angle % (Math.PI * 2);
        } else  if (form == 'p') {
            angle = rearg % (Math.PI * 2);
            distance = imdist;
            real = Math.cos(angle) * imdist;
            imag = Math.sin(angle) * imdist;
        }
    }

    public static Complex add(Complex nr1, Complex nr2) {
        double nre = nr1.real + nr2.real;
        double nim = nr1.imag + nr2.imag;
        Complex result = new Complex(nre, nim, 'c');
        return result;
    }

    public static Complex multiply(double scalar, Complex nr2) {
        Complex result = new Complex(scalar * nr2.real, scalar * nr2.imag, 'c');
        return result;
    }

    public static Complex multiply(Complex nr1, Complex nr2) {
        double nre = nr1.real * nr2.real - nr1.imag * nr2.imag;
        double nim = nr1.real * nr2.imag + nr1.imag * nr2.real;
        Complex result = new Complex(nre, nim, 'c');
        return result;
    }

    public static Complex conjugate(Complex normal) {
        Complex result = new Complex(normal.real, -normal.imag, 'c');
        return result;
    }

    public static Complex divide(Complex nr1, Complex nr2) {
        Complex numerator = multiply(nr1, conjugate(nr2));
        double denominator = multiply(nr2, conjugate(nr2)).real;
        double resultreal = numerator.real / denominator;
        double resultimag = numerator.imag / denominator;
        Complex result = new Complex(resultreal, resultimag, 'c');
        return result;
    }

    public static double absolute(Complex nr1) {
        return Math.sqrt(multiply(nr1, conjugate(nr1)).real);
    }

    public static void print(Complex number, char form) { //print cartesian form
        if (form == 'c') {
            double realround = Math.round(number.real * 10000) / 10000.0;
            System.out.print(realround + " ");
            double imagi = Math.round(number.imag * 10000) / 10000.0;
            if (imagi >= 0) {
                System.out.print("+ ");
            }
            System.out.println(imagi + "i");
        } else if (form == 'p') {
            double r = Math.round(number.distance * 10000) / 10000.0;
            double angulus = Math.round(number.angle * 10000) / 10000.0;
            System.out.println(r + " * e^" + angulus + "i");
        }
    }
}
