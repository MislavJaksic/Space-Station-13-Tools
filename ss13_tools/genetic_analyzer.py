import sys
import re

"""
geneticsResearch.dm
/datum/geneticsResearchEntry
	var/name = "HERF" //Name of the research entry
	var/desc = "DERF" //Description
	var/finishTime = 0 //Internal. No need to mess with this.
	var/researchTime = 0 //How long this takes to research in 1/10ths of a second.
	var/tier = 0 //Tier of research. Tier 0 does not show up in the available research - this is intentional. It is used for "hidden" research.
	var/list/requiredResearch = list() // You need to research everything in this list before this one will show up
	var/list/requiredMutRes = list() // Need to have researched these mutations first - list of requisite IDs.
	var/requiredTotalMutRes = 0 // Need to have researched this many mutations total
	var/isResearched = 0 //Has this been researched? I.e. are we done with it? 0 = not researched, 1 = researched, -1 = currently researching.
	var/researchCost = 10 //Cost in research materials for this entry.
	var/hidden = 0 // Is this one accessible by players?
	var/htmlIcon = null
"""


class BioEffect(object):
    def __init__(self, text):
        self.text = text

        self.code = None
        self.name = None
        self.desc = None
        self.id = None
        self.probability = None
        self.reclaim_mats = None
        self.curable_by_mutadone = None
        self.stability_loss = None
        self.secret = None
        self.occur_in_genepools = None

        self._parse()

    def _parse(self):
        self.code = self._extract_string("/datum/bioEffect/(.*)")
        self.name = self._extract_string('name = "(.*)"')
        self.desc = self._extract_string('desc = "(.*)"')
        self.id = self._extract_string('id = "(.*)"')
        self.probability = self._extract_integer("probability = (.*)")
        self.reclaim_mats = self._extract_integer("reclaim_mats = (.*)")
        self.curable_by_mutadone = self._extract_integer("curable_by_mutadone = (.*)")
        self.stability_loss = self._extract_integer("stability_loss = (.*)")
        self.secret = self._extract_integer("secret = (.*)")
        self.occur_in_genepools = self._extract_integer("occur_in_genepools = (.*)")

    def _extract_integer(self, expression):
        match = re.search(expression, self.text)
        if match:
            return match.group(1)
        return -12345

    def _extract_string(self, expression):
        match = re.search(expression, self.text)
        if match:
            return match.group(1)
        return ""

    def __str__(self):
        string = ""
        string += self.code + "$"
        string += self.name + "$"
        string += self.desc + "$"
        string += self.id + "$"
        string += str(self.probability) + "$"
        string += str(self.reclaim_mats) + "$"
        string += str(self.curable_by_mutadone) + "$"
        string += str(self.stability_loss) + "$"
        string += str(self.secret) + "$"
        string += str(self.occur_in_genepools)
        return string


def get_bioeffect_text(file):
    text = ""
    for line in file:
        if line == "\n":
            if "/datum/bioEffect" in text:
                yield text.strip()
            text = ""
        text += line


filenames = [
    "data/beneficial.dm",
    "data/harmful.dm",
    "data/hemochromia.dm",
    "data/meta.dm",
    "data/mutantrace.dm",
    "data/non_genetic.dm",
    "data/powers.dm",
    "data/speech.dm",
    "data/useless.dm",
]


def main(args):
    """main() will be run if you run this script directly"""

    with open("output.csv", "w") as output:
        output.write(
            "code$name$desc$id$probability$reclaim_mats$curable_by_mutadone$stability_loss$secret$occur_in_genepools\n"
        )
        for filename in filenames:
            with open(filename, "r") as input:
                for text in get_bioeffect_text(input):
                    output.write(str(BioEffect(text)) + "\n")


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
