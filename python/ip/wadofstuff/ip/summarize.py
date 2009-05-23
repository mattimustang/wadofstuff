#!/usr/local/bin/python
# Copyright (c) 2007-2009, Matthew Flanagan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the project nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
"""
Reduce a range of IP Addresses, e.g. 192.168.1.0 to 192.168.1.50, to 
a group of networks. e.g. 192.168.1.0/27, 192.168.1.32/28, 192.168.1.48/31,
192.168.1.50.
"""
__version__ = '1.0.0'

from IPy import IP, _ipVersionToLen
import sys

def usage():
    "Print usage and exit."
    print "usage: %s start end" % sys.argv[0]
    sys.exit(2)

def get_prefix_length(number1, number2, bits):
    """Get the number of leading bits that are same for two numbers.

    >>> from IPy import IP
    >>> get_prefix_length(IP('0.0.0.0').int(), IP('192.168.1.7').int(), 32)
    0
    >>> get_prefix_length(IP('0.0.0.0').int(), IP('1.0.0.0').int(), 32)
    7
    >>> get_prefix_length(IP('192.168.1.0').int(), IP('192.168.1.7').int(), 32)
    29
    >>> get_prefix_length(IP('192.168.1.0').int(), IP('192.168.1.8').int(), 32)
    28
    >>> get_prefix_length(IP('192.168.1.0').int(), IP('192.168.1.15').int(), 32)
    28
    >>> get_prefix_length(IP('192.168.1.0').int(), IP('192.168.1.255').int(), 32)
    24
    >>> get_prefix_length(IP('192.168.1.0').int(), IP('192.168.1.254').int(), 32)
    24
    """
    for i in range(bits):
        if number1 >> i == number2 >> i:
            return bits - i
    return 0

def count_righthand_zero_bits(integer, bits):
    """Count the number of zero bits on the right hand side.

    >>> from IPy import IP
    >>> count_righthand_zero_bits(IP('192.168.1.1').int(), 32)
    0
    >>> count_righthand_zero_bits(IP('192.168.1.0').int(), 32)
    8
    >>> count_righthand_zero_bits(IP('192.168.0.0').int(), 32)
    19
    >>> count_righthand_zero_bits(IP('192.0.0.0').int(), 32)
    30
    >>> count_righthand_zero_bits(IP('1.0.0.0').int(), 32)
    24
    """
    if integer == 0:
        return bits
    for i in range(bits):
        if (integer >> i) % 2:
            return i

def summarize(first, last):
    """Summarize a network range given a first and last IP addresses.

    >>> summarize('192.168.1.0', '192.168.0.0')
    Traceback (most recent call last):
    ...
    ValueError: Last IP address must be greater than first.
    >>> summarize('::', '192.168.1.1')
    Traceback (most recent call last):
    ...
    ValueError: IP addresses must be same version.
    >>> summarize('192.168.1.0', '192.168.1.50')
    ['192.168.1.0/27', '192.168.1.32/28', '192.168.1.48/31', '192.168.1.50']
    >>> summarize('192.168.0.1', '192.168.2.255')
    ['192.168.0.1', '192.168.0.2/31', '192.168.0.4/30', '192.168.0.8/29', '192.168.0.16/28', '192.168.0.32/27', '192.168.0.64/26', '192.168.0.128/25', '192.168.1.0/24', '192.168.2.0/24']
    >>> summarize('192.168.0.1', '192.168.2.254')
    ['192.168.0.1', '192.168.0.2/31', '192.168.0.4/30', '192.168.0.8/29', '192.168.0.16/28', '192.168.0.32/27', '192.168.0.64/26', '192.168.0.128/25', '192.168.1.0/24', '192.168.2.0/25', '192.168.2.128/26', '192.168.2.192/27', '192.168.2.224/28', '192.168.2.240/29', '192.168.2.248/30', '192.168.2.252/31', '192.168.2.254']
    >>> summarize('192.168.0.0', '192.168.5.253')
    ['192.168.0.0/22', '192.168.4.0/24', '192.168.5.0/25', '192.168.5.128/26', '192.168.5.192/27', '192.168.5.224/28', '192.168.5.240/29', '192.168.5.248/30', '192.168.5.252/31']
    >>> summarize('192.168.0.0', '192.168.255.254')
    ['192.168.0.0/17', '192.168.128.0/18', '192.168.192.0/19', '192.168.224.0/20', '192.168.240.0/21', '192.168.248.0/22', '192.168.252.0/23', '192.168.254.0/24', '192.168.255.0/25', '192.168.255.128/26', '192.168.255.192/27', '192.168.255.224/28', '192.168.255.240/29', '192.168.255.248/30', '192.168.255.252/31', '192.168.255.254']
    >>> summarize('::', '1::fffe')
    ['::/16', '1::/113', '1::8000/114', '1::c000/115', '1::e000/116', '1::f000/117', '1::f800/118', '1::fc00/119', '1::fe00/120', '1::ff00/121', '1::ff80/122', '1::ffc0/123', '1::ffe0/124', '1::fff0/125', '1::fff8/126', '1::fffc/127', '1::fffe']
    
    Worst case:
    >>> summarize('0.0.0.0', '255.255.255.254')
    ['0.0.0.0/1', '128.0.0.0/2', '192.0.0.0/3', '224.0.0.0/4', '240.0.0.0/5', '248.0.0.0/6', '252.0.0.0/7', '254.0.0.0/8', '255.0.0.0/9', '255.128.0.0/10', '255.192.0.0/11', '255.224.0.0/12', '255.240.0.0/13', '255.248.0.0/14', '255.252.0.0/15', '255.254.0.0/16', '255.255.0.0/17', '255.255.128.0/18', '255.255.192.0/19', '255.255.224.0/20', '255.255.240.0/21', '255.255.248.0/22', '255.255.252.0/23', '255.255.254.0/24', '255.255.255.0/25', '255.255.255.128/26', '255.255.255.192/27', '255.255.255.224/28', '255.255.255.240/29', '255.255.255.248/30', '255.255.255.252/31', '255.255.255.254']
    """
    first = IP(first)
    last = IP(last)
    if first.version() != last.version():
        raise ValueError, "IP addresses must be same version."
    if first > last:
        raise ValueError, "Last IP address must be greater than first."
    net_list = []
    try:
        # see if the range is on a byte boundary
        net = IP("%s-%s" % (first, last))
        net_list.append(net.strCompressed(1))
    except ValueError:
        ip_bits = _ipVersionToLen(first.version())
        all_ones = 2**ip_bits - 1
        while first <= last:
            nbits = count_righthand_zero_bits(first.int(), ip_bits)
            current = None
            while True:
                addend = 2**nbits - 1
                current = first.int() + addend
                nbits -= 1
                if IP(current) <= last:
                    break
            prefix = get_prefix_length(first.int(), current, ip_bits)
            net_list.append(IP('%s/%s' % (first, prefix)).strCompressed(1))
            first = IP(current + 1)
            if current == all_ones:
                break
    return net_list

def main():
    """
    Parse command line arguments and pass them to summarize().
    """
    result_list = []
    try:
        result_list = summarize(sys.argv[1], sys.argv[2])
    except IndexError:
        usage()
    for i in result_list:
        print "%s" % i

if __name__ == "__main__":
    try:
        if sys.argv[1] == '--test':
            import doctest
            doctest.testmod()
        else:
            main()
    except IndexError:
        print "usage: summarize.py --test | ip1 ip2"
        sys.exit(2)

# vim: ai ts=4 sts=4 et sw=4
