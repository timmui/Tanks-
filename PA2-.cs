// -------------------------------------------------------------------
// Department of Electrical and Computer Engineering
// University of Waterloo
//
// Student Name: Timothy Chee Tim Mui
// Userid: tctmui
//
// Assignment: Programming Assignment #2
// Submission Date: Oct. 1, 2014
//
// I declare that, other than the acknowledgements listed below,
// this program is my original work.
//
// Acknowledgements:
// -------------------------------------------------------------------

using System;

class Binaryencoder
{
    static void Main()
    {
		string rawInput;
		uint input;
		
        Console.WriteLine("Binary encoder");
        Console.WriteLine();
        Console.Write ("Enter an unsigned integer number: ");
        rawInput = Console.ReadLine();

        if (uint.TryParse(rawInput, out input)){
			input = uint.Parse(rawInput);
			Converter(input);
			binaryconversion (input);
		}

        else {
            Console.WriteLine ("Sorry, that was not a valid input.");
        }
    }
	
	static void Converter (uint number){
	
		if (number < 2){
			Console.Write(number % 2);
		}
		
		else {
			Console.Write(number % 2);
			Converter (number/2);
			
		}
		
	}
	
	static uint binaryconversion(uint num)
    {
        uint bin;
        if (num != 0)
        {
            bin = (num % 2) + 10 * binaryconversion(num / 2);
            Console.Write(bin);
            return 0;
        }
        else
        {
            return 0;
        }
 
    }
	
}