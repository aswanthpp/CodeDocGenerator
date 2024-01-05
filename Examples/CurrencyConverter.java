import java.util.Scanner;

public class CurrencyConverter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter the amount to convert:");
        double amount = scanner.nextDouble();

        System.out.println("Enter the source currency (e.g., USD, EUR, JPY):");
        String sourceCurrency = scanner.next().toUpperCase();

        System.out.println("Enter the target currency (e.g., USD, EUR, JPY):");
        String targetCurrency = scanner.next().toUpperCase();

        // Replace these rates with actual exchange rates
        double usdToEurRate = 0.85;
        double usdToJpyRate = 110.0;

        double convertedAmount;

        if (sourceCurrency.equals("USD") && targetCurrency.equals("EUR")) {
            convertedAmount = amount * usdToEurRate;
        } else if (sourceCurrency.equals("USD") && targetCurrency.equals("JPY")) {
            convertedAmount = amount * usdToJpyRate;
        } else {
            System.out.println("Unsupported currency pair");
            return;
        }

        System.out.println("Converted amount: " + convertedAmount + " " + targetCurrency);

        scanner.close();
    }
}
