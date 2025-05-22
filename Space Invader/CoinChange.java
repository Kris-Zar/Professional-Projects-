import java.util.ArrayList;
import java.util.List;

public class CoinChangeRecursive {
    public static void main(String[] args) {
        int[] coins = {1, 2, 5};
        int amount = 5;
        List<String> combinations = new ArrayList<>();

        findCombinations(coins, amount, 0, new ArrayList<>(), combinations);

        
        System.out.println(combinations);
    }

    private static void findCombinations(int[] coins, int amount, int index, List<Integer> current, List<String> combinations) {
        if (amount == 0) {
            combinations.add(current.toString());
            return;
        }

        if (amount < 0 || index >= coins.length) {
            return;
        }

        
        current.add(coins[index]);
        findCombinations(coins, amount - coins[index], index, current, combinations);
        current.remove(current.size() - 1);

        
        findCombinations(coins, amount, index + 1, current, combinations);
    }
}