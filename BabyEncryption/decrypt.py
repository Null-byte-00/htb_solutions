import string
import binascii

text = "6e0a9372ec49a3f6930ed8723f9df6f6720ed8d89dc4937222ec7214d89d1e0e352ce0aa6ec82bf622227bb70e7fb7352249b7d893c493d8539dec8fb7935d490e7f9d22ec89b7a322ec8fd80e7f8921"
text_list = list(binascii.unhexlify(text))


char_list = string.printable

hex_dict = {}

for char in char_list:
    hex_dict[(123 * ord(char) + 18) % 256] = char


final_text = ""

for num in text_list:
    final_text = final_text + hex_dict[num]

print(final_text)
