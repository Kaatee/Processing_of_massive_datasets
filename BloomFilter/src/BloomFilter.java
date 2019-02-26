import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashSet;
import java.util.Random;
import java.math.BigInteger;

public class BloomFilter {

    int size = 0;
    int n = 0;
    int k = 0;
    int prime;
    int range;
    BitSet vector;
    ArrayList<HashFunction> functions = new ArrayList<>();

    public BloomFilter(int size, int n, int k,int range) {

        this.size = size;
        this.n = n;
        this.k = k;
        this.range = range;
        this.vector = new BitSet(size);
        this.prime = new BigInteger(String.valueOf(this.range)).nextProbablePrime().intValue();

        Random rand = new Random(0);

        for(int i = 1; i <= this.k; ++i) {
            int a = rand.nextInt(this.prime - 1) + 1;
            int b = rand.nextInt(this.prime);
            HashFunction hashFunction = new HashFunction(a, b);
            this.functions.add(hashFunction);
        }


    }

    public void add(int key) {
        //calculate k hash functions and make k bites true
        for(HashFunction function : this.functions) {
            int position = (int)(function.hash(key, this.prime) % this.size);
            this.vector.set(position);
        }
    }

    public Boolean contains(int key) {
        //calculate k hash functions and if at least one of calculated elements is false , then element doesnt cpntains
        boolean found = true;
        for(HashFunction function : this.functions) {
            int position = (int)(function.hash(key, this.prime) % this.size);
            if (!this.vector.get(position)) {
                found = false;
                break;
            }
        }
        return found;
    }

    public static void main(String[] args) {

        int n = 5_000;
        int range = 100_000_000;
        double factor = 8;
        int size = (int) Math.round(factor * n);
        int k = 10;

        Random random = new Random(0);

        BloomFilter bf = new BloomFilter(size, n, k,  range);

        HashSet<Integer> set = new HashSet<Integer>(n);

        while(set.size() < n) {
            set.add(random.nextInt(range));
        }

        for(int item : set) {
            bf.add(item);
        }

        int TP = 0, FP = 0, TN = 0, FN = 0 ;

        for(int i = 0; i < range; i++) {
            int key = i; //random.nextInt(range);
            Boolean containsBF = bf.contains(key);
            Boolean containsHS = set.contains(key);

            if(containsBF && containsHS) {
                TP++;
            } else if(!containsBF && !containsHS) {
                TN++;
            } else if(!containsBF && containsHS) {
                FN++;
            }  else if(containsBF && !containsHS) {
                FP++;
            }
        }

        System.out.println("TP = " + String.format("%6d", TP) + "\tTPR = " + String.format("%1.4f", (double) TP/ (double) n));
        System.out.println("TN = " + String.format("%6d", TN) + "\tTNR = " + String.format("%1.4f", (double) TN/ (double) (range-n)));
        System.out.println("FN = " + String.format("%6d", FN) + "\tFNR = " + String.format("%1.4f", (double) FN/ (double) (n)));
        System.out.println("FP = " + String.format("%6d", FP) + "\tFPR = " + String.format("%1.4f", (double) FP/ (double) (range-n)));


        //Now test membership of an element that is not in the set. Each of the k array positions computed by the hash functions
        //is 1 with a probability as above. The probability of all of them being 1, which would cause the algorithm
        //to erroneously claim that the element is in the set, is often given as  [1-(e^(-kn/m)] ^ k
        double x = Math.pow(1 - Math.exp(-k * (double)n / size),k);
        System.out.println("FPR = " + String.format("%1.4f", x));
    }


}
