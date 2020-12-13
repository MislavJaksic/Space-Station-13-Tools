import sys
import re

"""
/datum/bioEffect
	var/name = "" //Name of the effect.
	var/id = "goddamn_it"   //Internal ID of the effect.
	var/desc = "" //Visible description of the effect.
	var/researched_desc = null // You get this in mutation research if you've activated the effect
	var/datum/bioEffect/global_instance = null // bioeffectlist version of this effect
	var/datum/bioEffect/power/global_instance_power = null //just a power casted version of global instance
	var/research_level = EFFECT_RESEARCH_NONE
	var/research_finish_time = 0

	var/effectType = EFFECT_TYPE_DISABILITY //Used to categorize effects. Mostly used for MutantRaces to prevent the mob from getting more than one.
	var/mutantrace_option = null
	var/isBad = 0         //Is this a bad effect? Used to determine which effects to use for certain things (radiation etc).

	var/probability = 100 //The probability that this will be selected when building the effect pool. Works like the weights in pick()
	var/blockCount = 2    //Amount of blocks generated. More will make this take longer to activate.
	var/blockGaps = 2     //Amount of gaps in the sequence. More will make this more difficult to activate since it will require more guessing or cross-referencing.

	var/lockProb = 5    //How likely each block is to be locked when there's locks present
	var/lockedGaps = 1    //How many base pairs in this sequence will need unlocking
	var/lockedDiff = 2    //How many characters in the code?
	var/lockedTries = 3   //How many attempts before it rescrambles?
	var/list/lockedChars = list("G","C") // How many different characters are used

	var/occur_in_genepools = 1
	var/scanner_visibility = 1
	var/secret = 0 // requires a specific research tech to see in genepools
	var/list/mob_exclusion = list() // this bio-effect won't occur in the pools of mob types in this list
	var/mob_exclusive = null // bio-effect will only occur in this mob type

	var/mob/owner = null  //Mob that owns this effect.
	var/datum/bioHolder/holder = null //Holder that contains this effect.

	var/msgGain = "" //Message shown when effect is added.
	var/msgLose = "" //Message shown when effect is removed.

	var/timeLeft = -1//Time left for temporary effects.

	var/variant = 1  //For effects with different variants.
	var/cooldown = 0 //For effects that come with verbs
	var/can_reclaim = 1 // Can this gene be turned into mats with the reclaimer?
	var/can_scramble = 1 // Can this gene be scrambled with the emitter?
	var/can_copy = 1 //Is this gene copied over on bioHolder transfer (i.e. cloning?)
	var/can_research = 1 // If zero, it must be researched via brute force
	var/can_make_injector = 1 // Guess.
	var/req_mut_research = null // If set, need to research the mutation before you can do anything w/ this one
	var/reclaim_mats = 10 // Materials returned when this gene is reclaimed
	var/reclaim_fail = 5 // Chance % for a reclamation of this gene to fail
	var/curable_by_mutadone = 1
	var/stability_loss = 0
	var/activated_from_pool = 0
	var/altered = 0
	var/add_delay = 0
	var/wildcard = 0
	var/degrade_to = null // what this mutation turns into if stability is too low

	var/datum/dnaBlocks/dnaBlocks = null

	var/data = null //Should be used to hold custom user data or it might not be copied correctly with injectors and all these things.
	var/image/overlay_image = null
	var/acceptable_in_mutini = 1 // can this effect happen when someone drinks some mutini? we're gunna try this at

	var/removed = 0
"""

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

        self._parse()

    def _parse(self):
        self.code = self._extract_string("/datum/bioEffect/([a-zA-Z0-9_/]*)")
        self.name = self._extract_string('name = "(.*)"')
        self.desc = self._extract_string('desc = "(.*)"')
        self.id = self._extract_string('id = "(.*)"')
        self.effect_type = self._extract_string("effectType = (.*)")
        self.is_bad = self._extract_integer("isBad = ([0-9-]*)")
        self.probability = self._extract_integer("probability = ([0-9-]*)")
        self.reclaim_mats = self._extract_integer("reclaim_mats = ([0-9-]*)")
        self.curable_by_mutadone = self._extract_integer(
            "curable_by_mutadone = ([0-9-]*)"
        )
        self.msg_gain = self._extract_string('msgGain = "(.*)"')
        self.msg_lose = self._extract_string('msgLose = "(.*)"')
        self.stability_loss = self._extract_integer("stability_loss = ([0-9-]*)")
        self.secret = self._extract_integer("secret = ([0-9-]*)")
        self.occur_in_genepools = self._extract_integer(
            "occur_in_genepools = ([0-9-]*)"
        )
        self.degrade_to = self._extract_string("degrade_to = (.*)")

    def _extract_integer(self, expression):
        match = re.search(expression, self.text)
        if match:
            return match.group(1)
        return ""

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
        string += self.effect_type + "$"
        string += self.is_bad + "$"
        string += str(self.probability) + "$"
        string += str(self.reclaim_mats) + "$"
        string += str(self.curable_by_mutadone) + "$"
        string += self.msg_gain + "$"
        string += self.msg_lose + "$"
        string += str(self.stability_loss) + "$"
        string += str(self.secret) + "$"
        string += str(self.occur_in_genepools) + "$"
        string += self.degrade_to
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
            "source$code$name$desc$id$effect_type$is_bad$probability$reclaim_mats$curable_by_mutadone$msg_gain$msg_lose$stability_loss$secret$occur_in_genepools$degrade_to\n"
        )
        for filename in filenames:
            with open(filename, "r") as input:
                for text in get_bioeffect_text(input):
                    output.write(filename + "$" + str(BioEffect(text)) + "\n")


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
