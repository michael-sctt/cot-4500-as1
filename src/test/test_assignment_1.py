# Michael Scott
# COT4500 Assignment 1

import numpy as np

def conv_doub_prec_to_dec(bin_string):
    # Binary String: 010000000111111010111001 (0's appended to 64 bits)
    # S = 0
    # c = 10000000111
    # f = 1110101110010000000000000000000000000000000000000000
    # Formula: (-1)^S * 2^(c-1023) * (1 + f)
    #          1 * 2^(1031 - 1023) * (1 + (/2 + /4 + /8 + /32 + /128 + /256 + /512 + /4096))
    #          2^8 * (1 + 0.9201660156)
    # Expected = 491.5625

    # First bit is sign bit
    sign_bit = bin_string[0]

    # Bits 2-13 (inclusive) is exponent
    exponent = bin_string[1:12]

    # Rest of number is mantissa
    mantissa = bin_string[12:]

    # Formula: (-1)^S * 2^(c-1023) * (1 + f)
    return (np.power(-1, int(sign_bit)) * np.power(2, convert_bin_to_dec(exponent) - 1023) * (1 + find_mantissa_val(mantissa)))

def convert_bin_to_dec(bin_num):
    val = 0
    for idx in range(len(bin_num) - 1, -1, -1):
        if (bin_num[idx] == "1"):
            val += np.power(2, len(bin_num) - idx - 1)

    return val

def find_mantissa_val(mantissa):
    val = 0
    denominator = 2
    for bit in mantissa:
        if (bit == "1"):
            val += 1 / denominator
        denominator *= 2

    return val

def dec_round(decimal, num_digits):
    num_ten_factors = 0
    while (decimal > 1):
        decimal /= 10
        num_ten_factors += 1
    
    decimal = np.round(decimal, decimals=num_digits)
    decimal *= np.power(10, num_ten_factors)

    # If rounded beyond decimal point, make it an integer
    if (decimal == np.trunc(decimal)):
        decimal = int(decimal)
    
    return decimal

def dec_trunc(decimal, num_digits):
    num_ten_factors = 0
    while (decimal > 1):
        decimal /= 10
        num_ten_factors += 1
    
    decimal *= np.power(10, num_digits)
    decimal = np.trunc(decimal)
    decimal /= np.power(10, num_digits)
    decimal *= np.power(10, num_ten_factors)

    # If rounded beyond decimal point, make it an integer
    if (decimal == np.trunc(decimal)):
        decimal = int(decimal)

    return decimal

def find_abs_error(exact, approx):
    # Formula: |exact - approx|
    error = np.abs(exact - approx)
    return error

def find_rel_error(exact, approx):
    # Formula: |exact - approx| / |exact|
    error = np.abs(exact - approx) / np.abs(exact)
    return error

def check_alternating(funct_str):
    if ("-1**k" in funct_str or "(-1)**k" in funct_str):
        return True

    return False

def check_decreasing(funct, x):
    # Reference: Funct = "(-1)**k * ((x**k)/(k**3))"
    k = 1
    start_val = np.abs(eval(funct))
    for k in range(2, 5000):
        new_val = np.abs(eval(funct))
        if (new_val > start_val):
            return False
    return True

def find_min_terms(funct_str, x, tol):
    num_terms = 0
    k = 1
    while (np.abs(eval(funct_str)) > tol):
        num_terms += 1
        k += 1

    return num_terms

def custom_funct(x):
    funct_str = "x**3 + 4*x**2 - 10"
    return eval(funct_str)

def funct_first_deriv(x):
    funct_drv_str = "3*x**2 + 8*x"
    return eval(funct_drv_str)

def bisection(tol):
    left = -4
    right = 7

    i = 0
    max_its = 50
    p = 0

    while (np.abs(right - left) > tol and i < max_its):
        i += 1
        p = (left + right) / 2

        if ((custom_funct(left) < 0 and custom_funct(p) > 0) or (custom_funct(left) > 0 and custom_funct(p) < 0)):
            right = p
        else:
            left = p

    return i

def newton_raphson(tol):
    p_prev = 7
    max_its = 50

    i = 0
    while (i < max_its):
        if (funct_first_deriv(p_prev) != 0):
            i += 1
            p_next = p_prev - (custom_funct(p_prev) / funct_first_deriv(p_prev))
            if (np.abs(p_next - p_prev) < tol):
                return i
            p_prev = p_next

        else:
            print("Method unsuccessful: Derivative is 0.")
            return "Method was unsuccessful."

if __name__ == "__main__":

    # Question 1
    # Define the binary number to be converted
    bin_string = "0100000001111110101110010000000000000000000000000000000000000000"
    decimal_val = conv_doub_prec_to_dec(bin_string)
    print(f"{decimal_val:.5f}")
    print()

    # Question 2
    # Using the same 'decimal_val' from Question 1
    decimal_val_chopped = dec_trunc(decimal_val, 3)
    print(decimal_val_chopped)
    print()

    # Question 3
    # Using the same 'decimal_val' from Question 1
    decimal_val_rounded = dec_round(decimal_val, 3)
    print(decimal_val_rounded)
    print()

    # Question 4
    # Using the same 'decimal_val' from Question 1
    abs_error = find_abs_error(decimal_val, decimal_val_rounded)
    rel_error = find_rel_error(decimal_val, decimal_val_rounded)
    print(abs_error)
    print(rel_error)
    print()

    # Question 5
    funct_str = "(-1**k) * ((x**k) / (k**3))"
    tolerance = 10**-4
    # Check if alternating and decreasing
    if (check_alternating(funct_str) and check_decreasing(funct_str, 1)):
        print(find_min_terms(funct_str, 1, tolerance))
    print()

    # Question 6
    tolerance = 10**-4
    print(bisection(tolerance))
    print(newton_raphson(tolerance))
