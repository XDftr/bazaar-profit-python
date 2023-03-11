from data.execute import Execute
from data.bin_data import BinData

"""
Kasulik teada:
items.txt - kõik võimalikud itemite nimed, nt raw_salmon asemel raw_fish:1, teisi eripärisuse võib veel olla
items_to_flip.txt - crafting_materials: mida läheb craftimiseks vaja ja kogus, sell_item: item mida craftid ja kogus
best_flip.txt - profiti järgi järjestatud itemid

run.update_data() - uuendab marketi andmed
run.run(x) - uuendab andmed flippimise andmed ja salvestab failidesse, x - mitme itemi kohta profit, default 1
run.find_item("ITEM_NAME") - leiab selle itemi kohta andmed data file'ist.

RAW_FISH:1 - salmon
RAW_FISH:2 - clownfish
RAW_FISH:3 - pupperfish
LOG - OAK WOOD
LOG:1 - SPRUCE WOOD
LOG:2 - BIRCH WOOD
LOG:3 - JUNGLE WOOD
"""
if __name__ == '__main__':

    search = "auction"  # "bazaar" or "auction" or "both"
    arg = 1
    search_type = "count"  # "count" or "count"
    bool_bin = False # False | True - Should we update bin data? Takes 1-3 minutes.

    run = Execute(search, search_type, arg, False)

    # run.create_classes()
    # run.test()
    # run.find_item("LOG")
    # run.find_item("LOG:1")
    # run.find_item("LOG:2")
    # run.find_item("LOG:3")
    # run.find_item("SPOOKY_BAIT")
