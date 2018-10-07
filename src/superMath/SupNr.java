
import java.text.DecimalFormat;
import java.util.*;


public class SupNr {
	private static int precision = 100; //must be at least 22
	private static int nrsBeforePoint = 50; // (always index of first digit after decimal point)
	int[] number = new int[precision]; //the array storing the decimal nr,
	int posOrNeg = 1;

	/* constructors:
			SupNr(double),
			SupNr(SupNr)-> create a copy
			SupNr(double, double), (double, double, double) -> composes a number out of multiple 10 digit integers
				(they get appended after each other starting after the decimal point)
		utility:
			toString()
			calcPi()-> return an approxmation of PI
		Advanced Math:

		Methods for addition:
			this.add(SupNr), (double)
			this.add(SupNr, SupNr), (double, double) -> adds two numbers in one step
		Methods for subtraction:
			this.subt(SupNr), (double)
			this.isBiggerThan(SupNr), (double), -> returns true <=> this > parameter
		Methods for multiplication:
			this.power10(int)-> multiplies this with 10^parameter (shifts digits)
			this.multOneDig(int)-> multiplies this by a one digit integer
			this.mult(SupNr), (double)
		Methods for division:
			reciprocal(SupNr) -> returns the reciprocal of positive numbers
			this.div(SupNr), (double)


	*/

//constructors ---------------------------------------------------------------------------------
	public SupNr() {
		this.number = new int[precision];
	}

	public SupNr(SupNr origin) {
		this.posOrNeg = origin.posOrNeg;
		for (int i = 0; i < precision; i++) {
			this.number[i] = origin.number[i];
		}
	}

	public SupNr(double inputnr) {
		if (inputnr < 0) {
			inputnr *= -1;
			posOrNeg = -1;
		}
		DecimalFormat df = new DecimalFormat("#");
        df.setMaximumFractionDigits(precision - nrsBeforePoint);
		String strVersion = "" + df.format(inputnr);
		//System.out.println(strVersion);
		int decimalPtIndex = strVersion.length();
		for (int i = 0; i < strVersion.length(); i++) {
			if (strVersion.charAt(i) == '.') {
				decimalPtIndex = i;
				//System.out.println(decimalPtIndex);
				break;
			}
		}
		for (int j = 0; j < nrsBeforePoint - decimalPtIndex; j++) {
			strVersion = "0" + strVersion;
		}
		for (int i = 0; i < nrsBeforePoint; i++) {
			number[i] = (int) strVersion.charAt(i) - 48;
		}
		for (int i = nrsBeforePoint + 1; i < strVersion.length(); i++) {
			number[i - 1] = (int) strVersion.charAt(i) - 48;
		}
	}

	public SupNr(double one, double two) {
		SupNr first = new SupNr(one);
		SupNr second = new SupNr(two);
		first.power10(-10);
		second.power10(-20);
		first.add(second);
		this.number = first.number;
	}

	public SupNr(double one, double two, double three) {
		SupNr first = new SupNr(one);
		SupNr second = new SupNr(two);
		SupNr third = new SupNr(three);
		first.power10(-10);
		second.power10(-20);
		third.power10(-30);
		first.add(second, third);
		this.number = first.number;
	}

// utility -------------------------------------------------------------------------------------------------------------
	public String toString() {
		String result = "SupNr: ";
		// System.out.println(this.posOrNeg);
		if (this.posOrNeg == 1) {
			result += "+ ";
		} else {
			result += "- ";
		}
		for (int i = 0; i < nrsBeforePoint; i++) {
			result += number[i];
		}
		result += " . ";
		for (int i = nrsBeforePoint; i < precision; i++) {
			result += number[i];
		}
		return result;
	}

	public static SupNr calcPi() {
		SupNr PI = new SupNr();
		SupNr four;
		SupNr next;
		int plusminus = 1;
		int nexto;
		for (int i = 1; i < 100000; i += 2) {
			four = new SupNr(4);
			nexto = i * plusminus;
			next = new SupNr(nexto);
			plusminus *= -1;
			four.div(next);
			PI.add(four);
		}
		return PI;
	}

// Advanced Maths -------------------------------------------------------------------------------
	public void power(int power) {
		SupNr multi = new SupNr(this);
		for (int i = 1; i < power; i++) {
			this.mult(multi);
		}
	}

// methods for addition --------------------------------------------------------------------------------------
	public void add(SupNr adder) { // increases abs value or call subtract method
		if (this.posOrNeg == adder.posOrNeg) { // the abs value of two summands is increased if both are pos or both neg
			// System.out.println("he says both positive");
			int carry = 0;
			int newDigit;
			for (int i = precision - 1; i >= 0; i--) { // adds the values appropriately
				newDigit = this.number[i] + adder.number[i] + carry;
				carry = newDigit / 10;
				newDigit = newDigit % 10;
				number[i] = newDigit;
			}
		} else if (this.posOrNeg == 1) { //positiv + negative -- this + adder
			adder.posOrNeg = 1;
			if (this.isBiggerThan(adder)) { // this - adder
				this.number = subt(this, adder).number; // happy case 12 + -5
			} else { // 5 + -12
				this.number = subt(adder, this).number; // so we have to 12 - 5 and set posorneg to -1
				this.posOrNeg = -1;
			}
			adder.posOrNeg = -1;
		} else { //negative + positive  (this is negative) this + adder
			this.posOrNeg = 1;
			if (this.isBiggerThan(adder)) { // -15 + 4
				this.number = subt(this, adder).number; // so we do 15 - 4 and change posorneg to -1
				this.posOrNeg = -1;
			} else { // -4 + 15
				this.number = subt(adder, this).number; // so we do 15 - 4 and leave posorneg set as 1
			}
		}
	}

	public void add(double addy) {
		SupNr adder = new SupNr(addy);
		this.add(adder);
	}

	public void add(SupNr one, SupNr two) {
		this.add(one);
		this.add(two);
	}

	public void add(double one, double two) {
		SupNr first = new SupNr(one);
		SupNr second = new SupNr(two);
		this.add(first, second);
	}

//everything to do the subtract stuff ---------------------------------------------------------------------------------------
	private boolean biggerComparer(SupNr bigger, SupNr that) { // algorithem that returns true if
		// the first non-different digit of bigger is bigger than the one in thanThat:
		int i = 0;
		while (bigger.number[i] == that.number[i]) { // find the index of first non different digit
			i++;
		}
		//System.out.println("index of first different: " + i);
		if (bigger.number[i] > that.number[i]) {
			return true;
		}
		return false;
	}

	public boolean isBiggerThan(SupNr compare) { // tells us if this. is bigger than another number
		if (this.posOrNeg != compare.posOrNeg) { // if this is positive and compare negative, we know
			if (this.posOrNeg == 1) {
				return true;
			} else { // we also know if the opposite is the case
				return false;
			}
		}
		// what if posOrNeg are the same?
		if (Arrays.equals(this.number, compare.number)) {
			//System.out.println("I am working, the numbers are the same");
			return false;
		}
		if (this.posOrNeg == 1) { //if we are dealing with positive numbers
			return biggerComparer(this, compare);
		} else { // else...
			return biggerComparer(compare, this);
		}
	}

	public boolean isBiggerThan(double squee) {
		SupNr compare = new SupNr(squee);
		return this.isBiggerThan(compare);
	}

	private boolean isBiggerThanOrEqual(double squee) {
		SupNr compare = new SupNr(squee);
		return this.isBiggerThan(compare) || Arrays.equals(this.number, compare.number);
	}

	public void subt(double subby) {
		SupNr subber = new SupNr(subby);
		this.subt(subber);
	}

	private SupNr subt(SupNr subbi, SupNr subber) { //takes two positive numbers only (subbi > subber) hence private...
		SupNr result = new SupNr(subbi);
		int carrier = 0;
		int nextCarrier = 0;
		for (int i = precision - 1; i >= 0; i--) { // subtract each digit
			if (result.number[i] < subber.number[i] + carrier) {
				nextCarrier = 1;
				result.number[i] += 10;
			}
			result.number[i] = result.number[i] - subber.number[i] - carrier;
			carrier = nextCarrier;
			nextCarrier = 0;
		}
		return result;
	}


	public void subt(SupNr subber) {
		if (this.posOrNeg != subber.posOrNeg) { // absolute value increases so we add()
			subber.posOrNeg *= -1;
			this.add(subber);
			subber.posOrNeg *= -1;
		 // now we need to actually perform subtraction :(
			//we only subtract two positive numbers from each other and always bigger - smaller
			// here the different operations that need to be performed
			//we always want (need) to have a big number minus a smaller number
			//bigger therefore always represent the positive version in the final line of each case
			//1, both are positive, bigger - smaller as we want it
			//2, both are positive, but we have to smaller - bigger 5-8 = (-1) * (8-5)
			// the result will be(-1) * (bigger - smaller)
			//3 both are negative, bigger - smaller (-3 - -14 = -3 + 14 = 14 - 3)
			// the result is therefore (-1) * (smaller - bigger)
			//4 both are negative, smaller - bigger (-14 - -3 = -14 + 3 = (-1) * (14-3)
			// the result being ( bigger is already negative) -> (bigger - smaller);

		} else if (this.posOrNeg == 1) { //positiv - positiv)
			if (this.isBiggerThan(subber)) { // this - subber
				this.number = subt(this, subber).number; // case nr 1
			} else {
				this.number = subt(subber, this).number; // case nr 2
				this.posOrNeg = -1;
			}
		} else { //negative - negative
			if (this.isBiggerThan(subber)) { // -4 - -15
				this.number = subt(subber, this).number; // case nr 3
				this.posOrNeg = 1;
			} else { // -14 - -5 -- this - subber
				this.number = subt(this, subber).number; // case nr 4
			}
		}
	}

// method for multiplication----------------------------------------------------------------------------------------
	public void div10() {
		for (int i = precision - 1; i > 0; i--) {
			this.number[i] = this.number[i - 1];
		}
		this.number[0] = 0;
	}

	public void mult10() {
		for (int i = 0; i <= precision - 2; i++) {
			this.number[i] = this.number[i + 1];
		}
		this.number[precision - 1] = 0;

	}

	public void power10(int power) {
		if (power >= 0) {
			for (int i = 0; i < power; i++) {
				this.mult10();
			}
		} else {
			for (int i = 0; i > power; i--) {
				this.div10();
			}
		}
	}

	private void crudeMult(int multor) { // multiplies by one-digit positive integer
		int carry = 0;
		for (int i = precision - 1; i >= 0; i--) {
			this.number[i] = this.number[i] * multor + carry;
			carry = this.number[i] / 10;
			this.number[i] = this.number[i] % 10;
		}
	}

	public void multOneDig(int multor) { // multiplies by a one-digit integer
		if (multor < 0) {
			this.posOrNeg *= -1;
			multor *= -1;
		}
		this.crudeMult(multor);
	}

	public void mult(SupNr multor) {
		SupNr safeCopy = new SupNr(this);
		safeCopy.posOrNeg = 1;
		this.posOrNeg *= multor.posOrNeg;
		int safePosOrNeg = this.posOrNeg;
		this.posOrNeg = 1;
		this.number = new int[precision];
		for (int i = 0; i < precision; i++) {
			SupNr nextToAdd = new SupNr(safeCopy);
			int nextMultor = multor.number[i];
			if (nextMultor != 0) { // maybe check later wether this decreases or increases performance
				nextToAdd.power10(nrsBeforePoint - i - 1);
				nextToAdd.crudeMult(nextMultor);
				this.add(nextToAdd);
			}
		}
		this.posOrNeg = safePosOrNeg;
	}

	public void mult(double multor) {
		SupNr multy = new SupNr(multor);
		this.mult(multy);
	}

//methods for division --------------------------------------------------------------------------------------
	public static SupNr reciprocal(SupNr dude) { // dude is positive when coming from the divide method,
		//must allllllllways be positive
		SupNr orig = new SupNr(dude);
		// System.out.println("orig dude " + orig);
		SupNr result = new SupNr();
		SupNr one = new SupNr(1);
		int startingIndex = nrsBeforePoint - 1;
		if (orig.isBiggerThan(1)) {
			do {
				orig.power10(-1);
				startingIndex += 1;
			} while (orig.isBiggerThan(1));
		} else { // it is smaller than one (e.g. 0.000002)
			while (!orig.isBiggerThan(1)) {
				// System.out.println("smaller than 1");
				orig.power10(1);
				startingIndex -= 1;
				if (startingIndex < -1) {
					System.out.println("DIVISION BY ZERO! :/");
					for (int i = 0; i < precision; i++) {
						result.number[i] = 9;
					}
					return result;
				}
			}
			orig.power10(-1);
			startingIndex += 1;
			// System.out.println(" thats the number " + orig);
		} // now every number is of the form 0.xxxx... , the index of the first non-zero number in the result is stored in startingIndex
		boolean stopIdiot;
		for (int i = startingIndex; i < precision; i++) {
			stopIdiot = false;
			int nextNewDigit = 0;
			while (one.isBiggerThanOrEqual(0) && !stopIdiot) {
				one.subt(orig);
				// System.out.println("new one " + one);
				// System.out.println(orig);
				nextNewDigit += 1;
				if (nextNewDigit > 11) {
					nextNewDigit = 1;
					stopIdiot = true;
				}
			}

			one.add(orig); //we remedy what we overshot
			if (nextNewDigit > 10) { // We needed 11 subts to overshoot (10 was exactly = 0)
				// System.out.println("bigger than 10");
				result.number[i-1] += 1;
				result.number[i] = 0;
				break;
			} else {
				nextNewDigit -= 1;
				result.number[i] = nextNewDigit;
			}
			// System.out.println("result " + result);
			orig.power10(-1);
			// System.out.println("the next orig --- " + orig);
		}
		return result;
	}

	public void div(SupNr divisor) {
		int safeThis = this.posOrNeg *= divisor.posOrNeg;
		this.posOrNeg = 1;
		int safePos = divisor.posOrNeg;
		divisor.posOrNeg = 1;
		divisor = reciprocal(divisor);
		// System.out.println(divisor);
		this.mult(divisor);
		divisor.posOrNeg = safePos;
		this.posOrNeg = safeThis;
	}

	public void div(double divisor) {
		SupNr squee = new SupNr(divisor);
		this.div(squee);
	}

}
