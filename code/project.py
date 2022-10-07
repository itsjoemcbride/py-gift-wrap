"""
Gift wrap quoting system
Started 20191102

USAGE:
If cube selected, only one INTEGER side length required in the first box
If cuboid selected, three INTEGER side lengths required in each box
If cylinder selected, INTEGER height required in the first box, and INTEGER radius in the second.
--> Invoice outputs dimensions of the paper required, but not package dimensions, as this is not relevant to what the customer has purchased.

Gift tag message box is ignored in pricing, if gift tag is not required.

Note to self: Ensure comments are located where necessary, but not excessive
"""

import tkinter as tk
import math  # used exclusively for pi when calculating surface area of a cylinder
import os  # only used to open invoice on close

global price, totalPrice, userColour, itemNo

price = '%.2f' % 0
totalPrice = '%.2f' % 0.0
userColour = "purple"
itemNo = 0

f = open("invoice.txt", "w")
f.write("INVOICE: \n")
f.close()

#
# All functions are called by the 'main' function
def main():
    gui()

# This enables or disables dimension boxes depending on the shape selection
def toggleDims(throwAwayVariable):
    if str(shape.get()) == "Cube Shaped":  # User has selected cube: only one box needed
        length = tk.Entry(master, width=15, textvariable=lengthDef, state='normal').grid(sticky="W", row=2, column=1)
        width = tk.Entry(master, width=15, textvariable=widthDef, state='disabled').grid(sticky="W", row=2, column=2)
        height = tk.Entry(master, width=15, textvariable=heightDef, state='disabled').grid(sticky="W", row=2, column=3)
    elif str(shape.get()) == "Cuboid Shaped":  # User has selected cuboid: three boxes needed
        length = tk.Entry(master, width=15, textvariable=lengthDef, state='normal').grid(sticky="W", row=2, column=1)
        width = tk.Entry(master, width=15, textvariable=widthDef, state='normal').grid(sticky="W", row=2, column=2)
        height = tk.Entry(master, width=15, textvariable=heightDef, state='normal').grid(sticky="W", row=2, column=3)
    elif shape.get() == "Cylinder Shaped":  # User has selected cylinder shape: two boxes needed
        length = tk.Entry(master, width=15, textvariable=lengthDef, state='normal').grid(sticky="W", row=2, column=1)
        width = tk.Entry(master, width=15, textvariable=widthDef, state='normal').grid(sticky="W", row=2, column=2)
        height = tk.Entry(master, width=15, textvariable=heightDef, state='disabled').grid(sticky="W", row=2, column=3)
    else:
        print("CRITICAL ERROR: Shape choice not valid.")

def completeOrder():
    global f, master

    totalPriceVat = (float(totalPrice) * 1.2)
    totalPriceVat = '%.2f' % totalPriceVat

    f = open("invoice.txt", "a")
    f.write("Total: £{0} \nTotal including VAT: £{1}".format(totalPrice, totalPriceVat))
    f.close()
    master.destroy()
    os.system("notepad.exe invoice.txt")


def outputToInvoice():
    global f, itemNo, requiredPaperX, requiredPaperY

    itemNo += 1
    f = open("invoice.txt", "a")

    # Get Required information in usable state for invoice:
    # Shape, Dimensions, Colour, Paper Choice, Bow, Gift tag, Message (if applicable), Costs (with new total)
    outShape = str(shape.get())
    outDim1 = str(lengthDef.get())
    outDim2 = str(widthDef.get())
    outDim3 = str(heightDef.get())
    if str(paperChoice.get()) == "0":
        outPaper = 6
    else:
        outPaper = 8
    if str(bow.get()) == "0":
        outBow = "No"
    else:
        outBow = "Yes"
    if str(giftTag.get()) == "0":
        outTag = "No"
    else:
        outTag = "Yes"
    outPriceVat = (float(price) * 1.2)
    outPriceVat = '%.2f' % outPriceVat
    outMsg = str(giftTagMsg.get())

    # Write to invoice | Package dimensions not relevant, but the dimensions for the paper used to wrap the package will be
    if outTag == "Yes":
        f.write(
            "{0}. Shape: {1}, Paper Required: {10} x {2}cm, Colour: {3}, Paper: {4}, Bow: {5}, Gift Tag: {6}, Message: \"{9}\" \nCost: £{7}, Cost including VAT: £{8} \n \n".format(itemNo, outShape, int(requiredPaperY), userColour, outPaper, outBow, outTag, price, outPriceVat, outMsg, int(requiredPaperX)))
    else:
        f.write("{0}. Shape: {1}, Paper Required: {9} x {2}cm, Colour: {3}, Paper: {4}, Bow: {5}, Gift Tag: {6}. \nCost: £{7}, Cost including VAT: £{8} \n \n".format(itemNo, outShape, int(requiredPaperY), userColour, outPaper, outBow, outTag, price, outPriceVat, int(requiredPaperX)))

    f.close()


def calculatePaper():
    global requiredPaperX, requiredPaperY

    # Calculate the amount of paper required for cuboid  (I have not done the cylinder maths)
    if str(shape.get()) == "Cube Shaped":  # User has selected cube: do cube equation
        side = lengthDef.get()  # Only need 1 side, as all sides are the same.
        requiredPaperX = ((4 * side) + 6)
        requiredPaperY = ((3 * side) + 6)
        requiredPaper = requiredPaperX * requiredPaperY
    elif str(shape.get()) == "Cuboid Shaped":  # User has selected cuboid: do cuboid equation
        length = lengthDef.get()  # Need 3 side lengths
        width = widthDef.get()
        height = heightDef.get()
        requiredPaperX = ((2 * length) + (2 * height) + 6)
        requiredPaperY = ((height * 2) + width + 6)
        requiredPaper = requiredPaperX * requiredPaperY

    elif shape.get() == "Cylinder Shaped":  # User has selected cylinder shape: do cylinder equation
        height = lengthDef.get()  # Need two parameters
        radius = widthDef.get()
        requiredPaperX = ((4 * radius) + height + 6)
        requiredPaperY = (2 * math.pi * radius + 6)
        requiredPaper = requiredPaperX * requiredPaperY
    else:
        print("CRITICAL ERROR: Shape choice not valid.")
    return requiredPaper


# Calculates price based on user choices
def calculatePrice():
    global price
    price = 0

    # Calculate total cost of the paper
    if str(paperChoice.get()) == "0":
        price += 0.004 * calculatePaper()
    elif str(paperChoice.get()) == "1":
        price += 0.0075 * calculatePaper()
    else:
        print("CRITICAL ERROR: Paper choice not valid.")

    # Calculate total cost of the bow
    if str(bow.get()) == "0":
        price += 0  # No bow, so no additional cost
    elif str(bow.get()) == "1":
        price += 1.5  # a bow costs £1.50
    else:
        print("CRITICAL ERROR: Bow choice not valid.")

    # Calculate total cost of the gift tag
    if str(giftTag.get()) == "0":
        price += 0  # No gift tag, so no additional cost
    elif str(giftTag.get()) == "1":
        giftMsgLen = len(giftTagMsg.get())
        price += 0.5 + (0.02 * giftMsgLen)  # Gift tag costs 50p, plus 2p per letter.
    else:
        print("CRITICAL ERROR: Gift tag choice not valid.")

    return price


# Renders/Draws the canvas based on user choice
def paperRender():
    global paperPreview
    if paperChoice.get() == 0:  # This is choice 6
        shift = 0

        paperPreview.create_rectangle(0, 0, 200, 200, fill='white')  # White square to 'clear' the canvas
        for i in range(2):
            paperPreview.create_rectangle(0 + shift, 0 + shift, 40 + shift, 40 + shift, fill=userColour)  # Start of top left portion moving to center
            paperPreview.create_rectangle(20 + shift, 20 + shift, 60 + shift, 60 + shift, fill='white', outline=userColour)
            paperPreview.create_rectangle(200 - shift, 200 - shift, 160 - shift, 160 - shift, fill=userColour)  # Start of bottom right portion moving to center
            paperPreview.create_rectangle(180 - shift, 180 - shift, 140 - shift, 140 - shift, fill='white', outline=userColour)
            paperPreview.create_rectangle(0 + shift, 200 - shift, 40 + shift, 160 - shift, fill=userColour)  # Start of bottom left portion moving to center
            paperPreview.create_rectangle(20 + shift, 180 - shift, 60 + shift, 140 - shift, fill='white', outline=userColour)
            paperPreview.create_rectangle(200 - shift, 0 + shift, 160 - shift, 40 + shift, fill=userColour)  # Start of top right portion moving to center
            paperPreview.create_rectangle(180 - shift, 20 + shift, 140 - shift, 60 + shift, fill='white', outline=userColour)

            shift += 40
        paperPreview.create_rectangle(80, 80, 120, 120, fill=userColour)  # Centre square


    else:  # This is choice 8
        x = 0

        paperPreview.create_rectangle(0, 0, 200, 200, fill=userColour)  # Canvas BG is now userColour

        for i in range(4):
            paperPreview.create_rectangle(0, 200, 100 - x, 100 + x, fill='white', outline='black')  # Start of the bottom left squares
            paperPreview.create_rectangle(0, 200, 80 - x, 120 + x, fill=userColour, outline='black')
            paperPreview.create_rectangle(200, 0, 100 + x, 100 - x, fill='white', outline='black')  # Start of the top right squares
            paperPreview.create_rectangle(200, 0, 120 + x, 80 - x, fill=userColour, outline='black')

            x += 40


# This function is called when the user presses the 'Update Preview' button. Updates unit price and image.
def updatePreview(throwawayVar):
    global price, userColour

    userColour = str(colour.get())
    paperRender()

    price = '%.2f' % calculatePrice()
    priceLabel = tk.Label(text="    Unit Price: £" + price, font=("Arial", 15)).grid(sticky="E", row=6, column=4)
    priceVat = float(price) * 1.2
    priceVat = '%.2f' % priceVat
    priceVatLabel = tk.Label(text="   incl VAT: £" + str(priceVat), font=("Arial", 15)).grid(sticky="E", row=6, column=5)


# This function is called when the user presses the 'Add to Invoice' button. Writes to file and updates total price
def addToInvoice():
    global totalPrice
    totalPrice = float(totalPrice) + float(price)
    totalPrice = '%.2f' % totalPrice
    totalPriceLabel = tk.Label(text="    Total Price: £" + str(totalPrice), font=("Arial", 15)).grid(sticky="E", row=7, column=4)
    totalPriceVat = float(totalPrice) * 1.2
    totalPriceVat = '%.2f' % totalPriceVat
    totalPriceVatLabel = tk.Label(text="   incl VAT: £" + str(totalPriceVat), font=("Arial", 15)).grid(sticky="E", row=7, column=5)
    outputToInvoice()


# This function is responsible for the main gui (tkinter) widgets
def gui():
    global master
    # Create master window
    master = tk.Tk()
    master.title("Gift wrap quote generator")

    # Widgets here:

    # These widgets are the labels
    # title
    titleLabel = tk.Label(master, text="Gift wrap quote generator", font=("Arial", 30)).grid(sticky="W", row=0, column=0, columnspan=3)
    # shape
    shapeMenuLabel = tk.Label(master, text="Shape: ", font=("Arial", 15)).grid(sticky="W", row=1, column=0)

    # dimensions
    DimLabel = tk.Label(master, text="Dimensions (cm): ", font=("Arial", 15)).grid(sticky="W", row=2, column=0)

    # colour
    colourMenuLabel = tk.Label(master, text="Colour: ", font=("Arial", 15)).grid(sticky="W", row=3, column=0)

    # paper
    paperLabel = tk.Label(text="Paper:", font=("Arial", 15)).grid(sticky="W", row=4, column=0)

    # Bow
    bowLabel = tk.Label(text="Bow?", font=("Arial", 15)).grid(sticky="W", row=6, column=0)

    # Gift Tag
    giftTagLabel = tk.Label(text="Gift tag?", font=("Arial", 15)).grid(sticky="W", row=7, column=0)

    # Gift Tag message
    giftTagMsgLabel = tk.Label(text="Gift tag message?", font=("Arial", 15)).grid(sticky="W", row=8, column=0)

    # Error outputter  # This is on a line on it's own. Deliberate design choice.
    errorLabel = tk.Label(text="").grid(sticky="W", row=9, column=0, columnspan=6)

    # These are the various widgets associated with each label
    # This widget is for the shape of present dropdown
    global shape
    shape = tk.StringVar(master)
    shape.set("Cube Shaped")  # default value
    shapeMenu = tk.OptionMenu(master, shape, "Cube Shaped", "Cuboid Shaped", "Cylinder Shaped")
    shapeMenu.grid(sticky="W", row=1, column=1, columnspan=3)
    shapeMenu.bind("<Configure>", toggleDims)

    #
    # Entry box for dimensions (*length*)
    global lengthDef, length
    lengthDef = tk.IntVar()
    length = tk.Entry(master, width=15, textvariable=lengthDef).grid(sticky="W", row=2, column=1)
    lengthDef.set(14)  # Default entry for box
    lengthDef.set(14)  # Default entry for box

    # Entry box for dimensions (width)
    global widthDef, width
    widthDef = tk.IntVar()
    width = tk.Entry(master, width=15, textvariable=widthDef).grid(sticky="W", row=2, column=2)
    widthDef.set(9)  # Default entry for box

    # Entry box for dimensions (height)
    global heightDef, height
    heightDef = tk.IntVar()
    height = tk.Entry(master, width=15, textvariable=heightDef).grid(sticky="W", row=2, column=3)
    heightDef.set(4)  # Default entry for box

    #
    # This widget is for the colour of present dropdown
    global colour
    colour = tk.StringVar(master)
    colour.set("purple")  # default value
    colourMenu = tk.OptionMenu(master, colour, "purple", "DarkSlateGray4", "deep sky blue", "light sea green", "VioletRed2", "gold")
    colourMenu.grid(sticky="W", row=3, column=1)
    colourMenu.bind("<Configure>", updatePreview)

    # This is the paper radiomenu
    global paperChoice
    paperChoice = tk.IntVar()
    tk.Radiobutton(master, text="Choice 6", variable=paperChoice, value=0, command=paperRender).grid(sticky="W", row=4, column=1)
    tk.Radiobutton(master, text="Choice 8", variable=paperChoice, value=1, command=paperRender).grid(sticky="W", row=5, column=1)

    # bow checkbox
    global bow
    bow = tk.IntVar()
    bowBox = tk.Checkbutton(master, variable=bow).grid(sticky="W", row=6, column=1)

    # gift tag checkbox
    global giftTag
    giftTag = tk.IntVar()
    giftTagBox = tk.Checkbutton(master, variable=giftTag).grid(sticky="W", row=7, column=1)

    # gift tag message
    global giftTagMsg
    giftTagMsg = tk.StringVar()
    msg = tk.Entry(master, width=60, textvariable=giftTagMsg).grid(sticky="W", row=8, column=1, columnspan=3)
    giftTagMsg.set("Your message here!")

    # The following widgets sit in the third, fourth columns
    # Image (Create canvas)
    global paperPreview
    paperPreview = tk.Canvas(master, width=200, height=200)
    paperPreview.grid(row=1, column=4, rowspan=5, columnspan=3)

    # Draw on canvas
    paperPreview.create_rectangle(0, 0, 200, 200, fill='white')

    # Price
    priceLabel = tk.Label(text="    Unit Price: £" + price, font=("Arial", 15)).grid(sticky="E", row=6, column=4)
    totalPriceLabel = tk.Label(text="    Total Price: £" + totalPrice, font=("Arial", 15)).grid(sticky="E", row=7, column=4)

    priceVatLabel = tk.Label(text="    incl. VAT: £" + price, font=("Arial", 15)).grid(sticky="E", row=6, column=5)
    totalPriceVatLabel = tk.Label(text="    incl. VAT: £" + totalPrice, font=("Arial", 15)).grid(sticky="E", row=7, column=5)

    # Update Preview button
    calculateButton = tk.Button(master, text="Update Price")
    calculateButton.grid(row=8, column=4)
    calculateButton.bind("<1>", updatePreview)

    # Add to Invoice button
    saveButton = tk.Button(master, text="Add to Invoice", command=addToInvoice).grid(row=8, column=5, sticky='e')

    # Close program button
    closeButton = tk.Button(master, text="Complete Order", command=completeOrder).grid(row=0, column=5, sticky="E")

    ''' Automatic Updates
    # This is an EXPERIMENTAL feature. It is UNSTABLE. I have opted not to remove it, should I wish to enable it and bug
     # fix it in the future.
    # Automatically updates the price and display without needing to press "Update Preview"
    while 1:
        master.update()
        updatePreview()
    '''

    # This is mainloop
    tk.mainloop()


main()
