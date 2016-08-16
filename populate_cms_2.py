import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from cms.models import Category, Artist, Identification, Production, Location, Usage, Description, Item, Entry, Exit, LoanIn, LoanOut

def populate():

#### Add Catalogue here ####
    prints = add_cat('Prints')
    sculptures = add_cat('Sculptures')
    accessories = add_cat('Accessories')
    clothing = add_cat('Clothing')

#### Add Artist here ####
    katsushika_hokusai = add_artist('Katsushika Hokusai', 1760, 1849, "Katsushika Hokusai (1760-1849) is perhaps Japan's most famous artist. He is best known for his designs for prints and printed books, although later in life he focused increasingly on paintings.")
    kubo_shunman = add_artist('Kubo Shunman', 1757, 1820, "Shunman (1757-1820) was a celebrated painter, print-maker and author of the Edo period (1615-1868). As a print-maker, he specialised in surimono.")
    muneyoshi = add_artist('Muneyoshi Yamada Chozaburo', 0, 0, "")
    kohosai = add_artist('Kohosai', 0, 0, "")
    aorenraju = add_artist('Aorenraju', 1920, 0, "")

#### Add Item info from here ####
    #### One Chunk of info for an item ####
    pri001 = add_item("PRI001",
                      add_identification("The Great Wave; In the Hollow of a Wave off the Coast at Kanagawa", "",
                                         "Thirty-six Views of Mount Fuji", prints, 1),
                      add_production(katsushika_hokusai, 1831, "Japan", "Colour print from wood blocks, on paper"),
                      add_location("Prints & Drawings", "2017-12-30"),
                      add_usage("DP"),
                      add_description(37.2, 25.9, 0, 0, "Scar on the right top", "Wave",
                                      "This print is from Hokusai's ground-breaking series Thirty-six Views of "
                                      "Mount Fuji, the first to exist exclusively of large-format prints of landscapes. " \
                                      "It also made plentiful use of Prussian blue, a pigment which had only " \
                                      "recently been introduced to Japan and was both expensive and rare. " \
                                      "Colour print from wood blocks by Katsushika Hokusai (1760-1849) from " \
                                      "the series Thirty-six Views of Mount Fuji. In the hollow of a wave off " \
                                      "the coast at Kanagawa (Kanagawa oki nami ura). Often referred to as 'The Great Wave'. " \
                                      "This print is the most celebrated of the series, and indeed of all " \
                                      "Japanese prints. In it, Mount Fuji is pictured through the hollow of a " \
                                      "giant wave which threatens to engulf the boats below. The chaos of the " \
                                      "scene at sea contrasts with the stately serenity of Fuji in the background.")
                      )
    add_entry(pri001, "0001", "2000-12-31", "Misses Alexander", "")
    #### End of the chunk ####


    pri002 = add_item("PRI002",
                      add_identification("Owl on a Flowering Magnolia Branch", "", "", prints, 1),
                      add_production(kubo_shunman, 1800, "Japan", "Colour print from wood blocks, on paper"),
                      add_location("Prints & Drawings", "9999-12-31"),
                      add_usage("SR"),
                      add_description(17.9, 21.1, 0, 0, "", "Birds",
                                  "This is an exquisite example of one of Kubo Shunman's surimono, a privately-produced and limited-edition print often commissioned to mark a special occasion. Surimono usually feature poems, often composed by the people who ordered them, and are typified by the intimate relationship between text and image. Here, the poem is delicately rendered to the upper right of the owl, which perches on the branch of a flowering magnolia.")
                      )


    obj001 = add_item("OBJ001",
                      add_identification("Two bear cubs at play", "", "", sculptures, 1),
                      add_production(muneyoshi, 1909, "Japan", "Hammered iron"),
                      add_location("room 45", "9999-12-31"),
                      add_usage("LO"),
                      add_description(23, 19.3, 21, 0.88, "", "Bears",
                                      "Representational sculpture of animals and insects had been known in Japan from "
                                      "the middle of the Edo period (1600-1868), when bronze figures had been made for "
                                      "display in the tokonoma, the alcove in a Japanese house where works of art were "
                                      "displayed. These items were produced by traditional armour makers, or by those "
                                      "who made the decorative fittings for swords.With the fall of the Tokugawa "
                                      "Shogunate and the restoration of the Meiji Emperor in 1868 there came a ban in "
                                      "1876 on the wearing of swords by non-military personnel. This edict resulted in "
                                      "metalworkers seeking new outlets for their traditional crafts. They found a new "
                                      "expression in ornamental works, which they began to produce in considerable "
                                      "numbers for export to the West. "
                                      "Another technique that was used to even greater effect was repoussé work. "
                                      "This method of tooling sheet metal from the back is well demonstrated in this "
                                      "small hammered iron study of two bear cubs at play by Muneyoshi. "
                                      "The technique that usually involved hammering the design over two pitch moulds "
                                      "and then soldering or welding the two halves together with an almost invisible "
                                      "seam has been abandoned for this study. The bears have been hammered from a "
                                      "single piece of iron, carefully worked to produce a sensitively detailed "
                                      "naturalistic study. They were exhibited at the 1910 Anglo-Japanese Exhibition at "
                                      "White City, London. Interestingly, the V&A also has an unfinished, almost "
                                      "unrecognisable, preparatory study for these bears. Muneyoshi claimed lineage from "
                                      "the Myochin family, traditional armour makers since the Muromachi period. "
                                      "Writing in 1911, Professor Jiro Harada refers to Muneyoshi as being the ninth of "
                                      "the line, and calls him 'the greatest artist in hammered metalwork that Japan "
                                      "has seen in recent times'. Certainly some of his other works, notably a large "
                                      "study of an eagle now in the Tokyo National Museum, justify this title. There "
                                      "are also descriptions of a sculpture of a pair of lions, over 120 cm in height "
                                      "and hammered from a single piece of iron, which were also exhibited "
                                      "at the Anglo-Japanese exhibition of 1910.")
                      )
    add_entry(obj001, "0002", "2015-11-04", "Dr W.L. Hildburgh FSA", "")
    add_loan_out(obj001, "OUT0001", "2016-04-30", "Smithonian", "2018-04-30", "Royal Mail Ref: 193755437")
    add_loan_out(obj001, "OUT0002", "2018-05-01", "Guggenhaim", "2019-05-01", "")


    obj002 = add_item("OBJ002",
                      add_identification("Netsuke", "", "", accessories, 1),
                      add_production(kohosai, 1869, "Japan", "Carved ivory"),
                      add_location("room 45", "2017-01-30"),
                      add_usage("EX"),
                      add_description(0, 5, 0, 0, "", "People",
                                      "The netsuke is a toggle. Japanese men used netsuke to suspend various pouches and "
                                      "containers from their sashes by a silk cord. Netsuke had to be small and not too "
                                      "heavy, yet bulky enough to do the job. They needed to be compact with no sharp "
                                      "protruding edges, yet also strong and hardwearing. Above all they had to have the "
                                      "means of attaching the cord. Netsuke were made in a variety of forms. This is an "
                                      "example of the manju type. Manju netsuke were shaped and named after a type of "
                                      "rounded sweet dumpling filled with bean paste. They are usually a solid oval, "
                                      "rectangular or square shape and these compact forms were well suited to being worn "
                                      "next to the body. "
                                      "This ivory netsuke depicts Yoshitsune and Benkei fighting on the Gojo Bridge."
                                      "The bridge is shown on the reverse. The two figures of the heroic warriors stand "
                                      "proud of the surface and are are shown in dramatic close-up. Heroic warriors were "
                                      "also a popular subject for Ukiyoe (floating world) woodblock prints of the time.")
                      )
    add_entry(obj002, "0003", "9999-12-31", "Mr. Saito", "")
    add_exit(obj002, "0001", "2016-07-01", "Owner", "Royal Mail Ref: 19375682")


    obj003 = add_item("OBJ003",
                      add_identification("Kimono", "", "", clothing, 1),
                      add_production(aorenraju, 1937, "Japan", "Printed wool"),
                      add_location("room 46", "2017-02-28"),
                      add_usage("DP"),
                      add_description(78, 25, 0, 0, "", "London; Bridge; Flags; Aeroplane; Mount Fuji",
                                      "In the 1930s kimono for young boys, such as this example, were often patterned "
                                      "with highly graphic propaganda images. Unusually, this kimono commemorates an "
                                      "actual event, the first aeroplane flight from Japan to Europe. The plane, "
                                      "called the 'kamikaze-go' flew from Tokyo to London, landing at Croydon airport "
                                      "on April 9th 1937 making its pilot, Masaaki Iinuma, a hero. The kimono is "
                                      "decorated with images of the plane and, in circles, Mount Fuji, Tower Bridge "
                                      "and the route of the flight, together with the British and French flags. "
                                      "The design also features block letters, in white on grey, which read '1937 "
                                      "Aorenraku 15000'. Aorenraku roughly translates to 'connections across the blue' "
                                      "and 15000 is the distance of the journey in kilometres.")
                      )
    add_entry(obj003, "0004", "2016-11-30", "Aorenraju", "")
    add_exit(obj003, "0002", "2017-03-01", "Owner", "")
    add_loan_in(obj003, "IN0001", "2016-11-30", "Aorenraju", "2017-11-30", "Royal Mail Ref: 19375324")


    # Print out what we have added to the user.

    for j in Category.objects.all():
        print(j)

    for k in Artist.objects.all():
        print(k)

    for l in Identification.objects.all():
        print(l)

    for m in Item.objects.all():
        print("Entry: ")
        for n in Entry.objects.filter(item_id=m):
            print("- {0} - {1}".format(str(m), str(n)))
        print("Exit: ")
        for o in Exit.objects.filter(item_id=m):
            print("- {0} - {1}".format(str(m), str(o)))
        print("Loan In: ")
        for p in LoanIn.objects.filter(item_id=m):
            print("- {0} - {1}".format(str(m), str(p)))
        print("Loan Out: ")
        for q in LoanOut.objects.filter(item_id=m):
            print("- {0} - {1}".format(str(m), str(q)))


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


def add_artist(name, born, died, description):
    a = Artist.objects.get_or_create(name=name)[0]
    a.born = born
    a.died = died
    a.description = description
    a.save()
    return a


def add_item(item_id, identification, production, location, usage, description):
    i = Item.objects.get_or_create(item_id=item_id)[0]
    i.identification = identification
    i.production = production
    i.location = location
    i.usage = usage
    i.description = description
    i.save()
    return i


def add_identification(title, edition, series, cat, stock=1):
    idt = Identification.objects.create(category=cat, title=title, edition=edition, series=series, stock=stock)
    idt.save()
    return idt


def add_production(artist, production_year, place, technique):
    pro = Production.objects.create(artist=artist, production_year=production_year, place=place, technique=technique)
    pro.save()
    return pro


def add_location(location, location_date):
    loc = Location.objects.create(location=location, location_date=location_date)
    loc.save()
    return loc


def add_usage(status):
    usage = Usage.objects.create(status=status)
    usage.save()
    return usage


def add_description(width, height, depth, weight, condition, subject, note):
    desc = Description.objects.create(width=width, height=height, depth=depth, weight=weight, condition=condition, subject=subject, note=note)
    desc.save()
    return desc


def add_entry(item, entry_id, entry_date, owner, entry_note):
    ent = Entry.objects.get_or_create(item=item, entry_id=entry_id)[0]
    ent.entry_date = entry_date
    ent.owner = owner
    ent.entry_note = entry_note
    ent.save()
    return ent


def add_exit(item, exit_id, exit_date, exit_destination, exit_note):
    ext = Exit.objects.get_or_create(item=item, exit_id=exit_id)[0]
    ext.exit_date = exit_date
    ext.exit_destination = exit_destination
    ext.exit_note = exit_note
    ext.save()
    return ext


def add_loan_in(item, loan_in_id, loan_in_date, lender, return_out_date, loan_in_note):
    li = LoanIn.objects.get_or_create(item=item, loan_in_id=loan_in_id)[0]
    li.loan_in_date = loan_in_date
    li.lender = lender
    li.return_out_date = return_out_date
    li.loan_in_note = loan_in_note
    li.save()
    return li


def add_loan_out(item, loan_out_id, loan_out_date, borrower, return_in_date, loan_out_note):
    lo = LoanOut.objects.get_or_create(item=item, loan_out_id=loan_out_id)[0]
    lo.loan_out_date = loan_out_date
    lo.borrower = borrower
    lo.return_in_date = return_in_date
    lo.loan_out_note = loan_out_note
    lo.save()
    return lo

# Start execution here!
if __name__ == '__main__':
    print("Starting CMS population script ...")
    populate()