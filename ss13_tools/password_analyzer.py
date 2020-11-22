import sys
import re


class PasswordPool(object):
    def __init__(self, args, filename):
        self.args = args
        self.word_length = self._get_word_length()
        self.line = self._get_password_line(filename)

        self.lists_of_letters = self._line_to_letters()
        self._delete_lists_of_letters_not_matching_mystery_word()
        self._delete_lists_of_letters_with_chars_not_found()
        self.letter_frequency = self._get_frequency()

    def __str__(self):
        string = ""
        for list in self.lists_of_letters:
            string += "".join(list) + "\n"
        string += str(self.letter_frequency)
        return string

    def _get_password_line(self, filename):
        with open(filename, "r") as file:
            for i in range(self.word_length // 2 - 1):
                line = file.readline()
        return line

    def _get_word_length(self):
        return len(self.args[0])

    def _line_to_letters(self):
        letters = []
        words = self._line_to_words()
        return [list(word) for word in words]

    def _line_to_words(self):
        match = re.search("\@\=(.*)", self.line)
        if match:
            return match.group(1).split("@,")
        raise Exception("No leading characters in password file line!")

    def _get_frequency(self):
        freq = {}
        for list in self.lists_of_letters:
            for char in list:
                if freq.get(char):
                    freq[char] += 1
                else:
                    freq[char] = 1
        return self._sort_dict_by_value(freq)

    def _sort_dict_by_value(self, dict):
        return {
            k: v
            for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)
        }

    def _delete_lists_of_letters_not_matching_mystery_word(self):
        for i in range(self.word_length):
            letter = self._get_mystery_word()[i]
            if letter != "*":
                self.lists_of_letters = (
                    self._get_lists_of_letters_matching_letter_at_position(letter, i)
                )

    def _get_mystery_word(self):
        return list(self.args[0])

    def _get_lists_of_letters_matching_letter_at_position(self, letter, position):
        new_lists_of_letters = []
        for list in self.lists_of_letters:
            if letter == list[position]:
                new_lists_of_letters.append(list)
        return new_lists_of_letters

    def _delete_lists_of_letters_with_chars_not_found(self):
        for char in self._get_chars_not_found():
            new_lists_of_letters = []
            for list in self.lists_of_letters:
                if char not in list:
                    new_lists_of_letters.append(list)
            self.lists_of_letters = new_lists_of_letters

    def _get_chars_not_found(self):
        return self.args[1:]


password_pool_filename = "data/password_pool.txt"


def main(args):
    """main() will be run if you run this script directly"""
    password_pool = PasswordPool(args, password_pool_filename)

    print(password_pool)


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
