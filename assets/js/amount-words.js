function numberToIndianWords(value) {
    const amount = Math.round(Number(value) || 0);
    if (amount === 0) return "Zero Only";

    const ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
    const tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];

    function underThousand(number) {
        let words = "";
        if (number >= 100) {
            words += ones[Math.floor(number / 100)] + " hundred";
            number %= 100;
            if (number) words += " ";
        }
        if (number >= 20) {
            words += tens[Math.floor(number / 10)];
            if (number % 10) words += " " + ones[number % 10];
        } else if (number) {
            words += ones[number];
        }
        return words;
    }

    let words = "";
    const crore = Math.floor(amount / 10000000);
    const lakh = Math.floor((amount % 10000000) / 100000);
    const thousand = Math.floor((amount % 100000) / 1000);
    const remainder = amount % 1000;

    if (crore) words += underThousand(crore) + " crore ";
    if (lakh) words += underThousand(lakh) + " lakh ";
    if (thousand) words += underThousand(thousand) + " thousand ";
    if (remainder) words += underThousand(remainder);

    // "Only" is appended here, not "rupees only" — the caller decides whether
    // the leading "Rupees" belongs, so the same function stays reusable for
    // any currency-style prefix without producing a duplicated unit word.
    return words.trim().replace(/\b\w/g, letter => letter.toUpperCase()) + " Only";
}

function bindAmountInWords(inputId, outputId) {
    const input = document.getElementById(inputId);
    const output = document.getElementById(outputId);
    if (!input || !output) return;

    const update = () => {
        output.textContent = "Rupees " + numberToIndianWords(input.value);
    };
    input.addEventListener("input", update);
    update();
}
