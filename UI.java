package lickteig;

import java.util.Scanner;

/**
 * Utility class for interacting with the user
 *
 * @author Timothy Lickteig
 * @date 2019-03-29
 * @modified 2020-03-26
 */
public class UI {

    /**
     * Get a user input and returned
     *
     * @param prompt The prompt to be shown on the screen
     * @return The user input
     */
    public static String getUserInput(String prompt) {

        //Create scanner object and input variable
        Scanner console = new Scanner(System.in);
        String input;

        //Print the prompt and grab user input
        System.out.print(prompt);
        input = console.nextLine().trim();

        //Return the user input
        return input;
    }

    /**
     * Get a boolean value from the user
     *
     * @param prompt The user prompt to be displayed
     * @param yes The character to be entered to result in true
     * @return true or false
     */
    public static boolean getUserBool(String prompt, String yes) {

        //Create new scanner object and other variables
        String input;
        boolean result = false;
        Scanner console = new Scanner(System.in);

        //Print the prompt and get user input
        System.out.print(prompt);
        input = console.nextLine();

        //Convert to upper case
        input = input.toUpperCase();
        yes = yes.toUpperCase();

        //Decide whether true or false and return
        result = input.equals(yes);
        return result;
    }

    /**
     * Display a prompt and get user integer
     *
     * @param prompt The user prompt to be displayed
     * @return The integer entered by the user
     */
    public static int userInt(String prompt) {

        //Declare variables
        String input;
        int result = 0;
        boolean needed = true;
        Scanner in = new Scanner(System.in);

        //Loop until a correct answer has been entered
        while (needed) {

            //Print the prompt
            System.out.print("");
            System.out.print(prompt);

            //Get user input
            try {
                input = in.nextLine();
                result = Integer.parseInt(input);
                needed = false;
            } catch (Exception e) {
                System.out.println("Not a valid input");
            }

        }
        return result;

    }
    
    /**
     * Display a prompt and get user double
     *
     * @param prompt The user prompt to be displayed
     * @return The double entered by the user
     */
    public static double userDouble(String prompt) {

        //Declare variables
        String input;
        double result = 0;
        boolean needed = true;
        Scanner in = new Scanner(System.in);

        //Loop until a correct answer has been entered
        while (needed) {

            //Print the prompt
            System.out.print("");
            System.out.print(prompt);

            //Get user input
            try {
                input = in.nextLine();
                result = Double.parseDouble(input);
                needed = false;
            } catch (Exception e) {
                System.out.println("Not a valid input");
            }

        }
        return result;

    }

    /**
     * Display a menu and get user input
     *
     * @param options OPtions to be displayed onscreem
     * @param title The title of the menu
     * @param prompt The user prompt
     * @return The user selected option
     */
    public static String showUserMenu(String[] options, String title, String prompt) {

        String input;

        //Print the title
        System.out.println("");
        System.out.println("*** " + title + " ***");

        //Print all the options
        for (String option : options) {

            System.out.println(option);

        }

        //Display the prompt and get the user input
        input = getUserInput(prompt);
        System.out.println("");

        //Return the selected option
        return input;

    }
    
    /**
     * Displays a properly formatted error message
     * @param message The message to display
     */
    public static void showErrorMessage(String message) {
    
        System.out.println("ERROR: " + message);
        UI.pressEnterToContinue();
        
    }

    /**
     * Prompts the user to press enter and pauses the program
     */
    public static void pressEnterToContinue() {
        
        System.out.print("Press Enter to continue");
        Scanner in = new Scanner(System.in);
        in.nextLine();
        
    }
    
    /**
    * Displays a title for a new section of the host application
    * @param title The title to display
    */
    public static void sectionTitle(String title) {
    
        System.out.println("");
        System.out.println(title);
        System.out.println("");
        
    }

}
