package superMath;
import java.text.DecimalFormat;
import java.util.*;


public class SupNr {
	private static int precision = 50; //must be at least 22
	private static int nrsBeforePoint = 20;
	int[] number = new int[precision]; //the array storing the decimal nr,
	int posOrNeg;

	public SupNr(SupNr origin) {
		this.posOrNeg = origin.posOrNeg;
		for (int i = 0; i < precision; i++) {
			this.number[i] = origin.number[i];
		}
	}

	public SupNr(double inputnr) {
		posOrNeg = 1;
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


	public String toString() {
		String result = "SupNr: ";
		if (posOrNeg == 1) {
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

// method for adding and subtracting
	public void add(SupNr adder) { // increases abs value or call subtract method
		if (this.posOrNeg == adder.posOrNeg) { // the abs value of two summands is increased if both are pos or both neg
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

//everything to do the subtract stuff
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
		} else {
			return biggerComparer(compare, this);
		}
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




}
