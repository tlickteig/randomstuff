func returnString() -> String {
    return "Hello World!2"
}

func printString(input: String) {
    print(input)
}

class IOClass {
    var numberOfLines = 5
    var doubleSpaced = false
    var itemToPrint = ""

    func printSingleLine() {
        print(itemToPrint)
    }

    func printMultipleLines() {
        for x in 1...numberOfLines {
            print(itemToPrint)
            if doubleSpaced == true {
                print("")
            }
        }
    }
}

var ioClass1 = IOClass()
ioClass1.itemToPrint = "Printing single line"
ioClass1.printSingleLine()

printString(input: "")

var ioClass2 = IOClass()
ioClass2.itemToPrint = "Printing multiple lines 5 times"
ioClass2.printMultipleLines()

printString(input: "")

var ioClass3 = IOClass()
ioClass3.itemToPrint = "Printing multiple lines 7 times"
ioClass3.numberOfLines = 7
ioClass3.printMultipleLines()

printString(input: "")

var ioClass4 = IOClass()
ioClass4.itemToPrint = "Printing multiple lines 3 times double spaced"
ioClass4.numberOfLines = 3
ioClass4.doubleSpaced = true
ioClass4.printMultipleLines()