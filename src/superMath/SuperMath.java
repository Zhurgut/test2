package superMath;
// a program which can calculate with numbers beyond the precision of built-in doubles :O

public class SuperMath {
	public static void main(String[] args) {
		SupNr testnr = new SupNr(452.999999);
		testnr.add(0.0001);
//		SupNr testnr2 = new SupNr(453.9998);
//		System.out.println(testnr.isBiggerThan(testnr2));
//		testnr.subt(testnr2);
		System.out.println(testnr);
//		System.out.println(testnr2);


	}
}
